import hashlib,sys,os,urllib2,urllib,shlex
from subprocess import call
from pydub import AudioSegment
try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

algorithms=["osx_alex","osx_bruce","osx_fiona","osx_zarvox","osx_tom","osx_ava","osx_allison","osx_susan","osx_oliver","osx_lee","osx_amelie","osx_maged","osx_ting-ting","osx_yelda","osx_jorge","osx_klara","osx_juan","osx_milena","osx_yuna","osx_otoya","translate_tts"]

storage="/var/db/ngramradio/"


def getSentence(algorithm, filename, sentence):

    quoted = urllib.quote_plus(sentence + ".")

    if algorithm is "translate_tts":
        if len(quoted) < 200:
            url = "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=" + quoted + "&tl=En-us"
            headers = { 'User-Agent' : 'stream-mp3/mpg123/0.59r' }
            req = urllib2.Request(url, None, headers)
            response = urllib2.urlopen(req).read()
            outFile = open(filename, 'w')
            outFile.write(response)
            outFile.close()
            return True
        else:
            return False

    if "osx" in algorithm:
        voice = algorithm.split("_")[1]
        parameters = "say -v " + voice + " -o " + filename + " -- " + quote(sentence)
        print parameters
        theReturn = call(shlex.split(parameters), shell=False)
        if (theReturn is not 0):
            return False
        if not os.path.exists(filename):
            return False
        return True

    if algorithm is "picotts":
        parameters = "pico2wave -w " + filename + " -- " + quote(sentence)
        print parameters
        theReturn = call(shlex.split(parameters), shell=False)
        if (theReturn is not 0):
            return False
        if not os.path.exists(filename):
            return False
        return True


def getExtension(algorithm):
    if algorithm is "translate_tts":
        return ".mp3"
    if "osx" in algorithm:
        return ".m4a"
    if algorithm is "picotts":
        return ".wav"


if (len(sys.argv)) < 2:
    print("Usage: " + sys.argv[0] + " [filename]")
    exit;

ourFile = open (sys.argv[1], 'r')

# directory = storage + sys.argv[1]


basefilename = os.path.splitext(os.path.basename(sys.argv[1]))[0]

contents = ourFile.read().splitlines()
ourFile.close()

# Get rid of newlines and replace them with spaces
sentences = ' '.join(str(v) for v in contents)

# Split the whole thing into sentences
sentences = sentences.split(".")

for algorithm in algorithms:
    directory = storage + algorithm
    if not os.path.exists(directory):
        os.makedirs(directory)

    manifestFilename = storage + "/" + basefilename + "-" + algorithm + "-manifest.txt"
    manifest = open (manifestFilename, 'w')

    hashes = []
    didSomething = False
    index = 0
    extension = getExtension(algorithm)

    for sentence in sentences:
        index = index + 1
        print ("Sentence " + str(index) + " of " + str(len(sentences)))
        sentence = sentence.strip()
        print sentence + "."
        md5 = hashlib.md5()
        md5.update(sentence)
        theHash = md5.hexdigest()
        hashes.append(theHash)
        print (theHash)

        ourFile = directory + "/" + theHash + extension

        if not os.path.exists(ourFile):
            if getSentence(algorithm, ourFile, sentence) is True:
                manifest.write(directory + "/" + theHash + extension + "\n")
                manifest.flush()
                didSomething = True
            else:
                print ("error")
                hashes.remove(theHash)
        else:
            manifest.write(directory + "/" + theHash + extension + "\n")

    manifest.close()
    combinedName = storage + basefilename + "-" + algorithm + "-combined.mp3"

    if ((didSomething == True) or not os.path.exists(combinedName)) :
        combined = AudioSegment.empty()
        index = 0
        manifestLines = open (manifestFilename,'r').read().splitlines()
        for filename in manifestLines:
            index = index + 1
            print ("Combined sentence " + str(index) + " of " + str(len(hashes)))
            thisSound = AudioSegment.from_file(filename,os.path.splitext(filename)[1])
            combined = combined + thisSound
        combined.export(combinedName)
