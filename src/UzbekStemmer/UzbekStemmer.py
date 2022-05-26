from lxml import etree
from nltk.tokenize import RegexpTokenizer
from pathlib import Path
global root
this_directory = Path(__file__).parent
tree = etree.parse(this_directory/"Suffixes.xml")
root = tree.getroot()

    #qoshimchani tekshirish
def _checkerSuffix(word, suffix):
        b = False
        if(str(suffix) == word[-len(suffix):]):
            b=True
        return b

    #qoshimchani qirqish
def _cutSuffix(word,suffix):
        if _checkerSuffix(word,suffix):
            return word[:-len(suffix)]
        else:
            return word

    #soz asosini aniqlash
def _rootWord(word, suffixesClassId, matrixFSM):

        global root
        stop = False
        minWords=['u', 'bu', 'ol','uq']

        Way = dict()
        for x in range(len(matrixFSM)):
            y = 1
            while y < len(matrixFSM[x]):
                if (type(matrixFSM[x][y]) == list):
                    for number in matrixFSM[x][y]:

                        #qoshimcha alomorfi yoq bolsa
                        if root[suffixesClassId - 1][number - 1][0].get('allomorph') == 'false':
                            suffix = root[suffixesClassId - 1][number - 1][0].text

                            if _checkerSuffix(word,suffix):
                                oldWord = word
                                word = _cutSuffix(word,suffix)

                                #pass ni tekshirish
                                mistake = False
                                for subelem in root[suffixesClassId-1][number-1][3]:
                                    if _checkerSuffix(word,subelem.text):
                                        mistake = True
                                if mistake:
                                    word = oldWord
                                    continue


                                if (len(word) > 2) | (word in minWords):
                                    OldState = matrixFSM[x][0]
                                    x = y - 1
                                    y = 0


                                    # create transition
                                    if matrixFSM[x][-1] == -2:      Final = False
                                    else: Final = True

                                    transition = {
                                        "SuffixClass": str(root[suffixesClassId-1].get('class')),
                                        #"OldState": str(OldState),
                                        "SuffixNumber": number,
                                        "Suffix": suffix,
                                        #"NewState": str(matrixFSM[x][0]),
                                        "Final": Final
                                    }
                                    Way[len(Way) + 1] = transition

                                    # join ni tekshirish
                                    for subelem in root[suffixesClassId - 1][number - 1][2]:
                                        if _checkerSuffix(word, subelem.text) and ((len(_cutSuffix(word,subelem.text)) > 2) | (_cutSuffix(word,subelem.text) in minWords)):
                                            word = _cutSuffix(word, subelem.text)
                                            Final = True

                                            transition = {
                                                "SuffixClass": "Exception",
                                                #"OldState": "null",
                                                "SuffixNumber": "null",
                                                "Suffix": subelem.text,
                                                #"NewState": "null",
                                                "Final": Final
                                            }
                                            Way[len(Way) + 1] = transition
                                    # print(elem, " --> ", A[x][0])
                                    break
                                else:
                                    word = oldWord
                                    stop = True
                                    break





                        #qoshimcha alomorfi bolsa
                        else:
                            for allomorph in root[suffixesClassId - 1][number - 1][0]:
                                suffix = allomorph.text

                                if _checkerSuffix(word, suffix):
                                    oldWord = word
                                    word = _cutSuffix(word, suffix)

                                    # pass ni tekshirish
                                    mistake = False
                                    for subelem in root[suffixesClassId - 1][number - 1][3]:
                                        if _checkerSuffix(word, subelem.text):
                                            mistake = True
                                    if mistake:
                                        word = oldWord
                                        continue


                                    if (len(word) > 2) | (word in minWords):
                                        OldState = matrixFSM[x][0]
                                        x = y - 1
                                        y = 0

                                        # create transition

                                        if matrixFSM[x][-1] == -2:
                                            Final = False
                                        else:
                                            Final = True

                                        transition = {
                                            "SuffixClass": str(root[suffixesClassId - 1].get('class')),
                                            #"OldState": str(OldState),
                                            "SuffixNumber": number,
                                            "Suffix": str(suffix),
                                            #"NewState": str(matrixFSM[x][0]),
                                            "Final": Final
                                        }
                                        Way[len(Way) + 1] = transition

                                        # join ni tekshirish
                                        for subelem in root[suffixesClassId - 1][number - 1][2]:
                                            if _checkerSuffix(word, subelem.text) and ((len(_cutSuffix(word,subelem.text)) > 2) | (_cutSuffix(word,subelem.text) in minWords)):
                                                word = _cutSuffix(word, subelem.text)
                                                Final = True

                                                transition = {
                                                    "SuffixClass": "Exception",
                                                    #"OldState": "null",
                                                    "SuffixNumber": "null",
                                                    "Suffix": subelem.text,
                                                    #"NewState": "null",
                                                    "Final": Final
                                                }
                                                Way[len(Way) + 1] = transition
                                        # print(elem, " --> ", A[x][0])
                                        break
                                    else:
                                        word = oldWord
                                        stop = True
                                        break





                # Final
                elif matrixFSM[x][y] == -1:
                    stop = True
                    break

                # Face way. Return to correct state
                elif matrixFSM[x][y] == -2:
                    i = len(Way)
                    for x in range(i, 0, -1):
                        if Way[x]["Final"] == False:
                            word = word + Way[x]["Suffix"]
                            Way.pop(x)
                        else:
                            break

                    stop = True
                    break

                y += 1

            if (stop): break

        return word, Way

def _tensePerson(word):
        matrixFSM = [
            ['A', 0, [1], [2, 14, 15, 16, 17, 20, 21], [3, 4, 6, 7], [5], [9, 10, 12, 13], [11], [22], [19], [23, 24],
             0, 0, -1],
            ['B', 0, 0, [8], 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['C', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['D', 0, 0, [1, 2], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['E', 0, [1], [2, 14, 15, 16, 17], [6, 7], 0, 0, 0, 0, [19], 0, [12, 13], 0, -2],
            ['F', 0, 0, [8, 18, 20, 21], 0, 0, 0, 0, 0, 0, [22, 23, 24], 0, 0, -2],
            ['G', 0, 0, [8], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['H', 0, [1], [2, 20, 21], [3, 4, 6, 7], 0, 0, [11], 0, [19], 0, [9, 10, 12, 13], [5], -2],
            ['I', 0, 0, [18], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['J', 0, 0, [20, 21], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['K', 0, 0, [8, 18], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['L', 0, [1], [2], [6, 7], 0, 0, 0, 0, [19], 0, [12, 13], 0, -2]
        ]
        return _rootWord(word,1,matrixFSM)

def _verb(word):
        matrixFSM = [
            ['A', 0, [1, 3, 7, 8, 9, 10, 11, 12, 13], [2, 4, 5, 6, 14, 15, 16, 17, 18, 19, 20, 21, 22], [23], -1],
            ['B', 0, 0, [19], 0, -1],
            ['C', 0, 0, 0, 0, -1],
            ['D', 0, [1, 3], [2, 4, 5, 6], 0, -2]
        ]
        return _rootWord(word,2,matrixFSM)

def _relative(word):
        matrixFSM = [
            ['A', 0, [1, 3, 4, 5, 6, 8, 10, 11, 12], [2], [7, 9], [13], 0, -1],
            ['B', 0, 0, 0, 0, 0, 0, -1],
            ['C', 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 0, 0, 0, 0, -1],
            ['D', 0, [1, 3, 4, 5, 6, 7, 8, 9, 10, 11], 0, 0, 0, [2], -1],
            ['E', 0, [1, 3, 4, 5, 6, 8, 10, 11], [2], [7, 9], 0, 0, -1],
            ['F', 0, [3, 4, 6], 0, 0, 0, 0, -1]
        ]
        return _rootWord(word,3,matrixFSM)

def _derivational(word):
        matrixFSM = [
            ['A', 0, [1], [2],
             [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 26, 27, 28, 29, 30, 31, 32, 33,
              34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60,
              61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], [21], [24, 25], [58], -1],
            ['B', 0, 0, 0,
             [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 22, 23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
              39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 0, 0, 0, -1],
            ['C', 0, 0, 0, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 0, 0, 0, -1],
            ['D', 0, 0, 0, 0, 0, 0, 0, -1],
            ['E', 0, 0, 0, [16, 17, 18, 19, 20], 0, 0, 0, -1],
            ['F', 0, 0, 0, [22, 23], 0, 0, 0, -2],
            ['G', 0, 0, 0,
             [22, 23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
              50], 0, 0, 0, -1]
        ]
        return _rootWord(word,4,matrixFSM)

def _noun(word):
        matrixFSM = [
            ['A', 0, [1, 2, 3, 4, 5, 22, 23], [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16], [17], [18, 19, 20, 21], 0,
             0, 0, 0, 0, -1],
            ['B', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['C', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, [17], 0, 0, 0, 0, -1],
            ['D', 0, [1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11, 12], 0, 0, 0, 0, [17], 0, 0, 0, 0, -1],
            ['E', 0, [1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], 0, 0, 0, [17], 0, 0, 0, 0, -1],
            ['F', 0, [1, 2, 3, 4, 5, 22, 23], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16],
             [18, 19, 20, 21], -1],
            ['G', 0, [1, 2, 3, 4, 5, 22, 23], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16], 0, -1],
            ['H', 0, [1], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['I', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['J', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], 0, 0, 0, -2],
            ['K', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], 0, 0, -1],
            ['L', 0, [1, 2, 3, 4, 5, 22, 23], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16], 0, -2]
        ]
        return _rootWord(word,5,matrixFSM)

def _number(word):
        matrixFSM = [
            ['A', 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], -1],
            ['B', 0, 0, -1]
        ]
        return _rootWord(word,7,matrixFSM)

def _prefixes(word):

        global root
        suffixesClassId=6
        Way = dict()
        A = [
            ['A', 0, [1, 2, 3, 4, 5, 6, 7], -1],
            ['B', 0, 0, -1]
        ]
        B = [1, 2, 3, 4, 5, 6, 7]
        for number in B:
            suffix = root[suffixesClassId - 1][number - 1][0].text
            if (suffix == word[:len(suffix)]) & (len(word) - len(suffix) > 1):

                oldWord = word
                word = word[len(suffix):]

                # pass ni tekshirish
                mistake = False
                for subelem in root[suffixesClassId - 1][number - 1][3]:
                    if subelem.text == word[:len(subelem.text)]:
                        mistake = True
                if mistake:
                    word = oldWord
                    continue

                transition = {
                    "SuffixClass": "Preffixes",
                    #"OldState": "A",
                    "SuffixNumber": number,
                    "Suffix": suffix,
                    #"NewState": "B",
                    "Final": True
                }
                Way[len(Way) + 1] = transition


        return word,Way

def _joinDict(dict1, dict2):
        for i in range(1, len(dict2) + 1):
            dict1[len(dict1) + 1] = dict2[i]
        return dict1


def UzStemmer(word):
        words = []
        ways = []
        tempWord = ""
        tempWay1 = dict()
        tempWay2 = dict()

        # way1 (Noun --> Number)
        tempWord = word
        tempWay1.clear()

        # Noun
        tempWord, tempWay2 = _noun(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Number
        tempWord, tempWay2 = _number(tempWord)
        tempWay1 = _joinDict(tempWay1,tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))

        # way2 (Noun --> Derivational --> Prefixes)
        tempWord = word
        tempWay1.clear()

        # Noun
        tempWord, tempWay2 = _noun(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Derivational
        tempWord, tempWay2 = _derivational(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Prefixes
        tempWord, tempWay2 = _prefixes(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))

        # way3 (Noun --> Verb --> Relative --> Derivational --> Prefixes)
        tempWord = word
        tempWay1.clear()

        # Noun
        tempWord, tempWay2 = _noun(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Verb
        tempWord, tempWay2 = _verb(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Relative
        tempWord, tempWay2 = _relative(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Derivational
        tempWord, tempWay2 = _derivational(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Prefixes
        tempWord, tempWay2 = _prefixes(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))

        # way4 (TensePerson --> Verb --> Relative --> Derivational --> Prefixes)
        tempWord = word
        tempWay1.clear()

        # TensePerson
        tempWord, tempWay2 = _tensePerson(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Verb
        tempWord, tempWay2 = _verb(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Relative
        tempWord, tempWay2 = _relative(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Derivational
        tempWord, tempWay2 = _derivational(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        # Prefixes
        tempWord, tempWay2 = _prefixes(tempWord)
        tempWay1 = _joinDict(tempWay1, tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))

        #print(words)

        min_words_id=0
        if(len(words[1])<len(words[min_words_id])):
            min_words_id=1
        if(len(words[2])<len(words[min_words_id])):
            min_words_id=2
        if(len(words[3])<len(words[min_words_id])):
            min_words_id=3

        #print(ways)
        return words[min_words_id]


def ArticleStemmer(raw):
        stemmedraw=""
        tokenize = RegexpTokenizer("[\w`'‘‘‘’‘-]+")
        tokens = tokenize.tokenize(raw)
        for token in tokens:
            stemmedraw  = stemmedraw + str(WordStemmer(token)) + "\n"

        return stemmedraw + str(len(tokens))