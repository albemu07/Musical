'''
simple reproductor con filtro de agudos
'''


import sounddevice as sd
import soundfile as sf
import sys
import kbhit
import numpy as np


CHUNK = 1204


if len(sys.argv) < 2:
    #print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    #sys.exit(-1)
    wav = 'tormenta.wav'
else:
    wav = sys.argv[1]



data, SRATE = sf.read(wav,dtype="float32")

stream = sd.OutputStream(samplerate = SRATE, blocksize = CHUNK, channels = len(data.shape))  
stream.start()

kb = kbhit.KBHit()
c= ' '
frame = 0 # contador de frames

print("[a] activar/desactivar filtro")
# memoria del filtro (sample anterior)
memo = 0

act = False
while c!= 'q':
    # ojo: bloque referencia a data -> modificamos data!
    bloque = data[frame*CHUNK:(frame+1)*CHUNK]
    # si no queremos tocar data habría que hacer copia con
    # bloque = np.copy(data[frame*CHUNK:(frame+1)*CHUNK])
    if len(bloque)==0: break

    ultSample=bloque[-1] # guardamos ultima muestra para siguiente frame antes de modificar bloque
    if act:
        # procesamos. OJO: evitar bucles para recorrer arrays!!
        bloque[1:]=0.5*(bloque[0:-1]+bloque[1:]) # media entre cada muestra y la siguiente
        bloque[0] = 0.5*(mem+bloque[0])        # la primera muestra se calcula aparte
                                                # con la última muestra del bloque anterior y la primera del actual
    mem = ultSample # actualizamos memo con ultima muestra

    stream.write(bloque)    
    
    if kb.kbhit():
        c = kb.getch()
        print(c)
        if c =='q': break
        elif c=='a': act = not(act)
        print("Activo: ",act)
    frame += 1

stream.stop()       
stream.close()
kb.set_normal_term()
