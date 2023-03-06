import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100


frec = [220 * 2**((i+3)/12) for i in range(14)]

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

def limiter(signal, threshold):
    max_amplitude = np.max(np.abs(signal))
    if max_amplitude > threshold:
        signal = signal * threshold / max_amplitude
    return signal

def getFadeOut(dur):
    nSamples = int(dur*SRATE)
    samples = np.ones((int)(5*nSamples/6), dtype=float)
    
    # Generate a linear ramp from 1.0 to 0.0
    samplesFade = np.linspace(1.0, 0.0, (int)(nSamples/6), endpoint=False)
    samples = np.concatenate([samples, samplesFade])
    
    return np.float32(samples)

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
    noteArr = []

    buffFadeOut = getFadeOut(3)

    while c!= 'k' and not(end)>0: 
        #modificación de volumen 
        if kb.kbhit():
            note = -1
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

            if(note != -1):
                buff = np.float32(KarplusStrong(frec[note], 3))
                noteArr += [buff * buffFadeOut]

        # lo pasamos al stream
        if (len(noteArr) != 0):
            sum = 0
            erase = 0
            for i in range(len(noteArr)):
                sum += noteArr[i-erase][:CHUNK]
                noteArr[i-erase] = noteArr[i-erase][CHUNK:]
                if(len(noteArr[i-erase]) == 0):
                    noteArr.remove(noteArr[i-erase])
                    erase+=1
                elif(len(noteArr[i-erase]) < CHUNK):
                    zeros = CHUNK - len(noteArr[i-erase])
                    noteArr[i-erase] = np.float32(np.concatenate((noteArr[i-erase], np.zeros(zeros)), axis=0))
            
            #sum /= (len(noteArr) + erase)
            sum = limiter(sum, 0.99)
            
            stream.write(sum * vol) # escribimos al stream

    print('end')

    stream.stop()
    stream.close()
    kb.set_normal_term()

main()