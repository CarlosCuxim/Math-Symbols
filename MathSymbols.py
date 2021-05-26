import json

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkFont
from tkinter import scrolledtext as tkST

# ========== LÓGICA INTERNA ====================================================
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

def replaceSymbols(string):
    string = replaceTokens(string)
    string = replaceFromDict(string, superscript, "^")
    string = replaceFromDict(string, subscript, "_")
    string = replaceFromDict(string, miscellany)
    return string


# ========== INTERFAZ GRÁFICA ==================================================

Window = tk.Tk()
Window.minsize(500,300)

MainFrame = ttk.Frame(Window, width=400, height=300)
MainFrame.pack(pady=5)


LabelEntry = ttk.Label(MainFrame, text="Introduzca su entrada", font=tkFont.Font(weight="bold"))
LabelEntry.grid(row=0, column=0, padx=5, pady=5)

EntryText = tkST.ScrolledText(MainFrame, width=60, height=7, wrap="word")
EntryText.grid(row=1, column=0, padx=5, pady=5)

OutputText = tkST.ScrolledText(MainFrame, width=60, height=7, font=tkFont.Font(size=11), state='disabled', wrap="word")
OutputText.grid(row=2, column=0, padx=5, pady=5)


# Actualización cada vez que se agrega una letra
def UpdateText(event):
    string = EntryText.get("1.0", "end")
    string = replaceSymbols(string)
    
    OutputText.configure(state="normal")
    OutputText.delete("1.0", "end")
    OutputText.insert("1.0", string)
    OutputText.configure(state="disabled")

EntryText.bind("<KeyRelease>", UpdateText)



Window.mainloop()