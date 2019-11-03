import os

audiofile = "audio/joachim.mp3"
os.system(f"aubio tempo {audiofile} > audio-data.txt")
os.system(f"aubio beat {audiofile} >> audio-data.txt")
i = 0
beats = list()
with open("audio-data.txt") as f:
    for line in f.readlines():
        if i == 0:
            bpm = float(line.split()[0])
        else:
            beats.append(float(line.strip()))
        i += 1

print(bpm)
print(beats)