import json
import uuid
import codecs
import sys


inputFile = 'translate.json'
outputFile = "translate.txt"
lang = "en"

nextIsInput = False
nextIsOutput = False
nextIsLang = False

for arg in sys.argv:
  if nextIsInput:
    inputFile = arg
    nextIsInput = False
  if nextIsOutput:
    outputFile = arg
    nextIsOutput = False
  if nextIsLang:
    lang = arg
    nextIsLang = False
  if arg == "-i":
    nextIsInput = True
  if arg == "-o":
    nextIsOutput = True
  if arg == "-l":
    nextIsLang = True


def createTableRecors(jsonTree, records, root):
    if (len(jsonTree) == 0):
        return records
    jsonTreeKeys = jsonTree.keys()
    leafs = filter(lambda k: isinstance(jsonTree[k], str), jsonTreeKeys)
    for l in leafs:
      records.append(f'{uuid.uuid4()};{root}.{l};{jsonTree[l]};{lang}')

    nonleafs = filter(lambda k: not isinstance(jsonTree[k], str), jsonTreeKeys)
    for nl in nonleafs:
      innerObjects = jsonTree[nl]
      if len(root) == 0:
        innerRoot = nl
      else:
        innerRoot = f'{root}.{nl}'
      createTableRecors(innerObjects, records, innerRoot)

text = ''

with codecs.open(inputFile, encoding='utf-8') as f:
    for line in f:
        text += (line)

config = json.loads(text)

records = []

createTableRecors(config, records, "")

f = codecs.open(outputFile, "w", "utf-8")
for r in records:
  f.write(r + "\n")
f.close()





