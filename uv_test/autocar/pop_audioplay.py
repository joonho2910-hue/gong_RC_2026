from pop import AudioPlay, AudioRecord
import time

with AudioRecord("my_record.wav") as record:
    record.run()
    print("start Recording...")
    
    
    for _ in range(5):
        time.sleep(1)
        record.stop()
        print("stop Recording...")
        
        
        
with AudioPlay("my_record.wav", False, True) as play:
    play.run()
    print("Start Play...")
    for _ in range(12):
        time.sleep(1)

    play.stop()
    print("Stop play...")