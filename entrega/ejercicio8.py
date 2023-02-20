import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024

filename = 'piano.wav'
C, samplerate = sf.read(filename)
pitch_table = {'C': 1, 'D': 9/8, 'E': 5/4, 'F': 4/3, 'G': 3/2, 'A': 5/3, 'B': 15/8, 
    'c':2, 'd': 9/4, 'e': 5/2, 'f': 8/3, 'g': 3, 'a': 10/3, 'b': 15/4,}

# Función para obtener el array de muestras correspondiente a una nota
def get_note_array(note_name):
    # Interpolar el array de muestras para obtener la nota correspondiente
    #if frequency > samplerate:
    xToInt = np.arange(0, len(C), pitch_table[note_name])
    x = np.arange(0, len(C), 1)
    note_array = np.interp(xToInt, x, C)
    
    return np.float32(note_array)

def main():

    # abrimos stream de salida
    stream = sd.OutputStream(
    samplerate = samplerate,            # frec muestreo 
    blocksize  = len(C),            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

    # arrancamos stream
    stream.start()
    kb = kbhit.KBHit()
    c= ' '

    vol = 1.0
    print('\n\nProcessing chunks: ',end='')

    # termina con 'q' o cuando no queden samples
    end = False # será true cuando el chunk esté vacio

    i = 0

    buff = []

    while c!= 'k' and not(end)>0: 
        # modificación de volumen 
        if kb.kbhit():
            note = " "
            c = kb.getch()
            if (c=='s'): vol= max(0,vol-0.05)
            elif (c=='S'): vol= min(1,vol+0.05)
            elif (c == 'z'): note = 'C'
            elif (c == 'x'): note = 'D'
            elif (c == 'c'): note = 'E'
            elif (c == 'v'): note = 'F'
            elif (c == 'b'): note = 'G'
            elif (c == 'n'): note = 'A'
            elif (c == 'm'): note = 'B'
            elif (c == 'q'): note = 'c'
            elif (c == 'w'): note = 'd'
            elif (c == 'e'): note = 'e'
            elif (c == 'r'): note = 'f'
            elif (c == 't'): note = 'g'
            elif (c == 'y'): note = 'a'
            elif (c == 'u'): note = 'b'

            if(note != " "):
                buff = get_note_array(note)

            print("Vol: ",vol) 

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