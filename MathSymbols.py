import json


def JSONtoDict(direction):
    with open(direction, encoding="utf-8") as JSONFile:
        # Removiendo comentarios
        JSONFile = JSONFile.readlines()
        for i in range(len(JSONFile)):
            line = JSONFile[i]
            if "//" in line:
                JSONFile[i] = line.split("//")[0]
        JSONFile = "\n".join(JSONFile)
        # Convirtiendo a diccionario
        JSONDict = json.loads(JSONFile)
    return JSONDict

symbols = JSONtoDict("Symbols/symbols.json")
subscript = JSONtoDict("Symbols/subscript.json")
superscript = JSONtoDict("Symbols/superscript.json")


def getFirstNonLetterIndex(string, begin=0):
    string = string.lower()
    Letters = "abcdefghijklmnopqrstuvwxyz"

    for i in range(begin,len(string)):
        if string[i] not in Letters:
            return i

def replaceFirstToken(string, active="\\", dictionary=symbols):
    bi = string.index(active)
    ei = getFirstNonLetterIndex(string, bi+1)

    begin = string[:bi]
    token = string[bi+1:ei]
    end = string[ei:] if ei else ''

    if token in dictionary:
        token = symbols[token]
    return begin + token + end

def replaceTokens(string, active="\\", dictionary=symbols):
    while active in string:
        string = replaceFirstToken(string, active, dictionary)
    return string


string = "Hola mundo sea x \\in B y y = \\int x dx, entonces"

A = replaceTokens(string, "\\")
print(A)

