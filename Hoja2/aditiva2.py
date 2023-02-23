# sintesis aditiva con variacion de volumenes de armónicos y fases programables

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100  # sampling rate, Hz, must be integer
CHUNK = 1024   # tamaño del chunk

# contador de frames. se incrementa cada vez que se procesa un bloque
frame = 0

# frecuencia dada, volumen, frame inicial (para evitar pops)
def osc(frec,vol,frame):
    return vol*np.sin(2*np.pi*(np.arange(CHUNK)+frame)*frec/SRATE)

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()


frec = 440  # frec base

vols =   [0.3, 0.2, 0.15, 0.15, 0.1,  0.1,  0.2, 0.1, 0.5, 0.3 ]
delays = [0,  0.04, 0.1,  0.07, 0.03, 0.02, 0,0, 0,   0,   0 ]

kb = kbhit.KBHit()
c = ' '
   
while c!='z':
    arms = [frec*(i+1) for i in range(len(vols))]
    samples = np.zeros(CHUNK) 
   
    for i in range(len(vols)): 
        delay = delays[i]*SRATE
        samples = samples+osc(arms[i],vols[i],frame+delay)

    # Al enviar al stream convertimos a float32
    stream.write(np.float32(0.5*samples)) 

    if kb.kbhit():
        c = kb.getch()
        print(c)        
        if c =='z': break
        elif c=='Y': frec=frec+step
        elif c=='y': frec=frec-step
        elif (c>='a' and c<='x'):
            v = ord(c)-ord('a')
            if v<len(vols): vols[v] = max(0,vols[v]-0.01)
        elif (c>='A' and c<='X'):
            v = ord(c)-ord('A')
            if v<len(vols): vols[v] = min(1,vols[v]+0.01) 

        print("[Y/y] Frec: ", frec)
        print("z quit")
        for i in range(len(vols)): 
            print("["+str(chr(ord('A')+i))+"/"+str(chr(ord('a')+i))+"] ", " Frec " , arms[i],"  ",vols[i], "  delay: ",delays[i])

    frame += CHUNK


stream.stop()
