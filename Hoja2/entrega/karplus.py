'''
    wavetable real con clase python
    para conseguir la continuidad en los chunks generados y no tener pops
    llevamos un atributo "fase" que recorre la tabla de ondas y se actualiza 
    en cada sample producido.
    La siguiente vez se solicita un chunk, la fase está en el punto correcto
    Si varia la frencia de un chunk al siguiente, se varia el "paso" (step) entre 
    muestas de la wavetable, pero la fase está donde quedo -> enlazan dos senos de
    distinta frecuencia
'''

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs


SRATE = 44100      
CHUNK = 64


class KarplusStrong:
    def __init__(self, frec, vol, size):
        self.frec = frec
        self.vol = vol
        self.size = size
        # un ciclo completo de seno en [0,2pi)
        t = np.linspace(0, 1, num=size)
        self.waveTable = np.sin(2 * np.pi * t)
        # arranca en 0
        self.fase = 0
        # paso en la wavetable en funcion de frec y RATE
        self.step = self.size/(SRATE/self.frec)

    def setFrec(self,frec): 
        self.frec = frec
        self.step = self.size/(SRATE/self.frec)

    def getFrec(self): 
        return self.frec    

    def setVol(self,vol): 
        self.vol = vol

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



# stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
# stream.start()

# kb = kbhit.KBHit()
# c = ' '

# osc = OscWaveTable(110,1,1024)


# while True:
#     samples = osc.getChunk()

#     stream.write(samples)

#     if kb.kbhit():
#         os.system('clear')
#         c = kb.getch()
#         print(c)        
#         if c =='q': break
#         elif c=='F': osc.setFrec(osc.getFrec()+1)
#         elif c=='f': osc.setFrec(osc.getFrec()-1)

#         print("Frec ",osc.getFrec())
#         print("[F/f] subir/bajar frec")
#         print("q quit")
        

# kb.set_normal_term()        
# stream.stop()
# stream.close()
