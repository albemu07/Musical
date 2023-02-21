import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100

def addDelay(sound):
    delay = 0.2
    zeros = np.zeros(np.int64(delay * SRATE))
    soundDelayed = np.float32(np.concatenate((zeros, sound), axis=0))
    return soundDelayed

def main():

    # abrimos stream de salida
    stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

    # arrancamos stream
    stream.start()

    # abrimos stream de entrada (InpuStream)
    outStream = sd.InputStream(samplerate=SRATE, blocksize=CHUNK, dtype="float32", channels=1)

    # arrancamos stream
    outStream.start()

    kb = kbhit.KBHit()
    c= ' '

    vol = 1.0
    print('\n\nProcessing chunks: ',end='')

    # termina con 'q' o cuando no queden samples
    end = False # será true cuando el chunk esté vacio

    delay = 0.5
    buff = np.zeros(np.int64(SRATE*delay))

    while c!= 'k' and not(end)>0: 
        # modificación de volumen 
        if kb.kbhit():
            c = kb.getch()
            if(c == 'd'):
                delay -= 0.1
                if(delay <= 0): delay = 0
                buff = buff[np.int64(0.1*SRATE):]
            elif(c == 'D'):
                delay += 0.1
                buff = np.float32(np.append(np.zeros(np.int64(0.1*SRATE)), buff))
            print("Delay: ",delay) 

        bloque, _check = outStream.read(CHUNK)  # recogida de samples en array numpy    
        # read devuelve un par (samples,bool)
        buff = np.float32(np.append(buff,bloque)) # en bloque[0] están los samples

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