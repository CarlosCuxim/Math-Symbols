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
miscellany = JSONtoDict("Symbols/miscellany.json")


def getFirstNonLetterIndex(string, begin=0):
    Letters = "abcdefghijklmnopqrstuvwxyz"
    # Conversión de strings a minúsculas
    string = string.lower()
    # Busqueda del primer carácter no letra
    for i in range(begin,len(string)):
        if string[i] not in Letters:
            return i

def replaceFirstToken(string, active="\\", dictionary=symbols):
    # Obtención de index del inicio y fin del token
    bi = string.index(active)
    ei = getFirstNonLetterIndex(string, bi+1)
    # Partición del string de antes y despues del token
    begin = string[:bi]
    token = string[bi+1:ei]
    end = string[ei:] if ei else ''
    # Remplazo del token usando el diccionario
    if token in dictionary:
        token = symbols[token]
    else:
        token = active + token

    return begin + token + end

def replaceTokens(string, active="\\", dictionary=symbols):
    # Busqueda del tokens por cada 
    for i in range(len(string)):
        subString = string[i:]
        if active in subString:
            subString = replaceFirstToken(subString, active, dictionary)
        string = string[:i] + subString
    return string

def replaceFromDict(string, dictionary, prefix=""):
    for i in dictionary:
        string = string.replace(prefix+i, dictionary[i])
    return string

def ReplaceSymbols(string):
    string = replaceTokens(string)
    string = replaceFromDict(string, superscript, "^")
    string = replaceFromDict(string, subscript, "_")
    string = replaceFromDict(string, miscellany)
    return string

string = r"Sea Nx \in G/N, <<dado que>> (Nx)^2 = Nx^2 y x^2 \in N ``entonces'' (Nx)^2 = Ne, mostrando así que Nx tiene orden 2"

A = ReplaceSymbols(string)

print("\n", "Entrada:", string, "\n")
print("\n", "Salida", A, "\n")

