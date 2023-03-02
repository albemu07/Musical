import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100


frec = [220 * 2**((i+3)/12) for i in range(14)]

# def addDelay(sound):
#     delay = 0.2
#     zeros = np.zeros(np.int64(delay * samplerate))
#     soundDelayed = np.float32(np.concatenate((zeros, sound), axis=0))
#     return soundDelayed

# # Función para obtener el array de muestras correspondiente a una nota
# def get_note_array(note_name):
#     # Interpolar el array de muestras para obtener la nota correspondiente
#     #if frequency > samplerate:
#     xToInt = np.arange(0, len(C), pitch_table[note_name])
#     x = np.arange(0, len(C), 1)
#     note_array = np.interp(xToInt, x, C)
    
#     return np.float32(note_array)

def KarplusStrong(frec, dur):
    N = SRATE // int(frec) # la frecuencia determina el tamanio del buffer
    buf = np.random.rand(N) * 2 - 1 # buffer inicial: ruido
    nSamples = int(dur*SRATE)
    samples = np.empty(nSamples, dtype=float) # salida
    # generamos los nSamples haciendo recorrido circular por el buffer
    for i in range(nSamples):
        samples[i] = buf[i % N] # recorrido de buffer circular
        buf[i % N] = 0.5 * (buf[i % N] + buf[(1 + i) % N]) # filtrado
    return samples

def main():

    # abrimos stream de salida
    stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

    # arrancamos stream
    stream.start()
    kb = kbhit.KBHit()
    c= ' '

    vol = 1.0
    print('\n\nProcessing chunks: ',end='')

    # termina con 'q' o cuando no queden samplesz
    end = False # será true cuando el chunk esté vacio

    i = 0

    buff = []

    while c!= 'k' and not(end)>0: 
        #modificación de volumen 
        if kb.kbhit():
            note = 0
            c = kb.getch()
            if (c == 'z'): note = 0
            elif (c == 'x'): note = 1
            elif (c == 'c'): note = 2
            elif (c == 'v'): note = 3
            elif (c == 'b'): note = 4
            elif (c == 'n'): note = 5
            elif (c == 'm'): note = 6
            elif (c == 'q'): note = 7
            elif (c == 'w'): note = 8
            elif (c == 'e'): note = 9
            elif (c == 'r'): note = 10
            elif (c == 't'): note = 11
            elif (c == 'y'): note = 12
            elif (c == 'u'): note = 13

            buff = np.float32(KarplusStrong(frec[note], 3))
            # other = np.concatenate((get_note_array(note), np.zeros(np.int64(0.2 * samplerate))))
            # buff = np.float32(np.sum([other, addDelay(get_note_array(note))], axis = 0))
            #print("Vol: ",vol) 

        # lo pasamos al stream
        if (len(buff) != 0):
            stream.write(buff[:CHUNK] * vol) # escribimos al stream
            buff = buff[CHUNK:]
            if(len(buff) == 0):
                buff = []
            elif(len(buff) < CHUNK):
                zeros = CHUNK - len(buff)
                buff = np.float32(np.concatenate((buff, np.zeros(zeros)), axis=0))

    print('end')

    stream.stop()
    stream.close()
    kb.set_normal_term()

main()