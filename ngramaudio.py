import hashlib,sys,os,urllib2,urllib
from pydub import AudioSegment

storage="/var/db/ngramradio/"

if (len(sys.argv)) < 2:
    print("Usage: " + sys.argv[0] + " [filename]")
    exit;

ourFile = open (sys.argv[1], 'r')

# directory = storage + sys.argv[1]
directory = storage + "translate_tts"
if not os.path.exists(directory):
    os.makedirs(directory)

basefilename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
manifest = open (storage + "/" + basefilename + "-manifest.txt", 'w')

contents = ourFile.read().splitlines()
ourFile.close()

# Get rid of newlines and replace them with spaces
sentences = ' '.join(str(v) for v in contents)

# Split the whole thing into sentences
sentences = sentences.split(".")
hashes = []

for sentence in sentences:
    sentence = sentence.strip()
    print sentence + "."
    md5 = hashlib.md5()
    md5.update(sentence)
    theHash = md5.hexdigest()
    hashes.append(theHash)
    print (theHash)
    ourFile = directory + "/" + theHash + ".mp3"
    if not os.path.exists(ourFile):
        quoted = urllib.quote_plus(sentence + ".")
        if len(quoted) < 200:
            url = "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=" + quoted + "&tl=En-us"
            print url
            headers = { 'User-Agent' : 'stream-mp3/mpg123/0.59r' }
            req = urllib2.Request(url, None, headers)
            response = urllib2.urlopen(req).read()
            outFile = open(ourFile, 'w')
            outFile.write(response)
        else:
            print ("too long")
            hashes.remove(theHash)


for theHash in hashes:
    manifest.write(directory + "/" + theHash + ".mp3\n")

manifest.close()

combined = AudioSegment.empty()

for theHash in hashes:

    thisSound = AudioSegment.from_mp3(directory + "/" + theHash + ".mp3")
    combined = combined + thisSound

combined.export(storage + basefilename + "-combined.mp3")
