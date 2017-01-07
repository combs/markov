import hashlib,sys,os,urllib2,urllib,shlex,pydub,getopt,re
from subprocess import call
from pydub import AudioSegment
try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

all_algorithms=["osx_alex","osx_bruce","osx_fiona","osx_zarvox","osx_tom","osx_ava","osx_allison","osx_susan","osx_oliver","osx_lee","osx_amelie","osx_maged","osx_ting-ting","osx_yelda","osx_jorge","osx_klara","osx_juan","osx_milena","osx_yuna","osx_otoya","translate_tts"]
algorithms=[]

storage="/var/db/ngramradio/"


def getSentence(algorithm, filename, sentence):

    quoted = urllib.quote_plus(sentence)

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

def usage():
    print ("\nUsage: " + str(sys.argv[0]) + ' -a <algorithm> filename')
    print ("\nAvailable algorithms: " + str(all_algorithms))

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"a:",["algorithm="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    # print (len(args))
    if (len(args)) == 0 :
        usage()
        sys.exit(2)
    filename = args[0]

    for o,a in opts:
        if o in ("-a","--algorithm"):
            algorithms.extend(a.split(","))
            print(type(o))
            print(type(a))
            
    if len(algorithms)==0:
        algorithms.extend(all_algorithms)

    ourFile = open (filename, 'r')

    # directory = storage + sys.argv[1]


    basefilename = os.path.splitext(os.path.basename(filename))[0]

    contents = ourFile.read().splitlines()
    ourFile.close()

    # Get rid of newlines and replace them with spaces
    sentences = ' '.join(str(v) for v in contents)

    # Split the whole thing into sentences
    sentences = re.split("([\.\?\!])",sentences)

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
            sentence = sentence.strip()
            md5 = hashlib.md5()
            md5.update(sentence)
            theHash = md5.hexdigest()
            hashes.append(theHash)

            ourFile = directory + "/" + theHash + extension
            # print ("Sentence " + str(index) + " of " + str(len(sentences)) + ": " + theHash + extension)
            # print sentence + "."

            if not os.path.exists(ourFile):
                if getSentence(algorithm, ourFile, sentence) is True:
                    manifest.write(directory + "/" + theHash + extension + "\n")
                    manifest.flush()
                    didSomething = True
                else:
                    print ("Failed to render sentence " + str(index) + " of " + str(len(sentences)) + ": " + theHash + extension + " with algorithm " + algorithm)
                    print sentence
                    # print ("Error: ", sys.exc_info()[0])
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
                print ("Combined sentence " + str(index) + " of " + str(len(hashes)) + ": " + os.path.basename(filename))
                extension = os.path.splitext(filename)[1]

                try:
                    thisSound = AudioSegment.from_file(filename,extension[1:])
                    combined = combined + thisSound
                except pydub.exceptions.CouldntDecodeError:
                    os.unlink(filename)
                    print("Removing corrupt file: " + filename)

            combined.export(combinedName)



if __name__ == "__main__":
   main(sys.argv[1:])
