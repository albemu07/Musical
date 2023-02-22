import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante
import matplotlib.pyplot as plt

SRATE = 44100
CHUNK = 1024

last = 0

def noteToFrec(note):
    if(note =="C"):
        frec = 523.251
    elif(note =="D"):
        frec = 587.33
    elif(note =="E"):
        frec = 659.255
    elif(note =="F"):
        frec = 698.456
    elif(note =="G"):
        frec = 783.991
    elif(note =="A"):
        frec = 880
    elif(note =="B"):
        frec = 987.767
    elif(note =="c"):
        frec = 1046.502
    elif(note =="d"):
        frec = 1174.66
    elif(note =="e"):
        frec = 1318.51
    elif(note =="f"):
        frec = 1396.912
    elif(note =="g"):
        frec = 1567.982
    elif (note =="a"):
        frec = 1760
    elif(note =="b"):
        frec = 1975.534
    return frec

def readSong(fileName):
    f = open(fileName + ".txt", "r")
    x = f.readlines()
    p = x[5].split(" ")

    pFinal = []
    for pI in p:
        if(pI != "|"):
            if(len(pI) == 1 or pI[-1] == "M"):
                pFinal.append((pI, 1))
            elif(pI[-1] == "L"):
                pFinal.append((pI, 2))
            elif(pI[-1] == "S"):
                pFinal.append((pI, 0.5))
            elif(pI[-1] == "F"):
                pFinal.append((pI, 0.25))
    

    return pFinal

def oscChuck(nota,dur):
    global last # var global
    frec = noteToFrec(nota)
    data = np.sin(2*np.pi*(np.arange(SRATE * dur) + last)*frec/SRATE)
    data[-np.int32(len(data)*0.01):] = 0             
    last += len(data)*0.99
    
    return np.float32(data)

def happyBirthday():
    song = [("G",0.5),("G",0.5),("A",1),("G",1),("c",1),("B",2),("G",0.5),("G",0.5),("A",1),("G",1),("d",1),("c",2),("G",0.5),
        ("G",0.5),("g",1),("e",1),("c",1),("B",1),("A",1),("f",0.5),("f",0.5),("e",1),("c",1),("d",1),("c",2)]
    return song
    
def main():
    #readSong("prueba")
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

    # termina con 'q' o cuando no queden samples
    end = False # será true cuando el chunk esté vacio

    i = 0
    partitura = happyBirthday()
    bloque = []

    while c!= 'q' and not(end)>0: 
        if(i < len(partitura)):
            nota, duración = partitura[i]

        # lo pasamos al stream
        if(len(bloque) == 0):
            i += 1
            if(i > len(partitura)):
                end = True
            else:
                bloque = oscChuck(nota, duración)
        else:
            stream.write(bloque[:CHUNK] * vol) # escribimos al stream
            bloque = bloque[CHUNK:]
            if(len(bloque) == 0):
                bloque = []
            elif(len(bloque) < CHUNK):
                zeros = CHUNK - len(bloque)
                bloque = np.float32(np.concatenate((bloque, np.zeros(zeros)), axis=0))

        # modificación de volumen 
        if kb.kbhit():
            c = kb.getch()
            if (c=='v'): vol= max(0,vol-0.05)
            elif (c=='V'): vol= min(1,vol+0.05)
            print("Vol: ",vol) 

        print('.', end = '')

    print('end')

    stream.stop()
    stream.close()
    kb.set_normal_term()

main()