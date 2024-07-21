
from pygame import mixer 
  
# Starting the mixer 
mixer.init() 
  
# Loading the song 
mixer.music.load("data/mp3-files/happy-pharell-williams.mp3") 
  
# Setting the volume 
vol=0.6
mixer.music.set_volume(vol) 
  
# Start playing the song 
mixer.music.play() 
  
# infinite loop 
while True: 
      
    print("Press 'p' to pause, 'r' to resume") 
    print("Press 'e' to exit the program") 
    query = input("  ") 
      
    if query == 'p': 
  
        # Pausing the music 
        mixer.music.pause()      
    elif query == 'r': 
  
        # Resuming the music 
        mixer.music.unpause() 
    elif query == 'e': 
  
        # Stop the mixer 
        mixer.music.stop() 
        break
    elif query == 'v+':
        if vol < 1:
            vol = min(vol + 0.1, 1)
            mixer.music.set_volume(vol) 
            print(vol)
    elif query == 'v-':
        if vol > 0:
            vol = max(vol - 0.1, 0)
            mixer.music.set_volume(vol) 
            print(vol)
