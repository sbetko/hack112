import os

def analyzeAudiofile(audiofile, outputfile):
    analyzeTempo(audiofile, outputfile)
    analyzeBeatPositions(audiofile, outputfile)
    analyzeQuietPositions(audiofile, outputfile)
    
def extractAudioData(datafile):
    i = 0
    beats = list()
    quiet = list()
    noisy = list()
    with open(datafile) as f:
        for line in f.readlines():
            if i == 0:
                bpm = float(line.split()[0])
            elif line.split(':')[0] == 'QUIET':
                quiet.append(float(line.split(':')[1].strip()))
            elif line.split(':')[0] == 'NOISY':
                noisy.append(float(line.split(':')[1].strip()))
            else:
                beats.append(float(line.strip()))
            i += 1

    return bpm, beats, quiet, noisy

def analyzeTempo(audiofile, outputfile):
    os.system(f"aubio tempo {audiofile} > {outputfile}")

def analyzeBeatPositions(audiofile, outputfile):
    os.system(f"aubio beat {audiofile} >> {outputfile}")

def analyzeQuietPositions(audiofile, outputfile):
    os.system(f"aubio quiet {audiofile} >> {outputfile}")

if __name__ == "__main__":
    audiofile = "audio/joachim.mp3"
    outputfile = "audio-data.txt"
    analyzeAudiofile(audiofile, outputfile)
    bpm, beats, quiet, noisy = extractAudioData(outputfile)
    print(quiet)