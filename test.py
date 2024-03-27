import sys
sys.path.append("E:/Projects/Hacking/Gamingway/Source")
from gamingway import FF4Rom

patchpath = "../Resources/"

args = sys.argv
if len(args) < 2:
 inputfile = "../Resources/ff4.smc"
else:
 inputfile = args[1]
if len(args) < 3:
 outputfile = "../game.smc"
else:
 print(len(args))
 outputfile = args[2]

ff4 = FF4Rom(inputfile)
ff4.read()

ff4.write("characters")
ff4.save(outputfile)