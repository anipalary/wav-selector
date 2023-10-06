from consolemenu import *
from consolemenu.items import *
import os
import os.path
import platform

sl = "\\" if platform.system() == "Windows" else '/'

count = 0
folders = []
wavs = []

def select_folder():
    global count, folders
    count = 1

    print("Select a folder\n\n")
    
    i = 0
    list = []
    for a in os.listdir(path='.'):
        if os.path.isdir('.' + sl + a):
            i += 1
            list.append(a)
            print(str(i) + " - " + a)

    inp = input("\n >> ")

    if not str.isnumeric(inp):
        exit()
    if int(inp) > i:
        exit()
    if int(inp) < 1:
        exit()

    folders.append(list[int(inp)-1])

    select_mode()

def select_folders():
    global count, folders
    count = 2

    print("Select folders(separate with spaces: \"1 5 6 13 15\")\n\n")
    
    i = 0
    list = []
    for a in os.listdir(path='.'):
        if os.path.isdir('.' + sl + a):
            i += 1
            list.append(a)
            print(str(i) + " - " + a)

    inp = input("\n >> ")

    for a in inp.split(" "):
        if str.isnumeric(a) and int(a) <= i and int(a) > 0:
            if not int(a)-1 in list:
                folders.append(list[int(a)-1])

    select_mode()

def select_mode():
    m = ConsoleMenu("Select mode", "")
    
    mode_0 = FunctionItem("selected tracks only",             start, [0])
    mode_1 = FunctionItem("everything exept selected tracks", start, [1])
    
    m.append_item(mode_0)
    m.append_item(mode_1)
    
    m.show()

def start(mode):
    global folders, wavs, count

    if count == 0:
        for a in os.listdir(path='.'):
            if os.path.isdir('.' + sl + a):
                folders.append(a)

    print("Select tracks(separate with spaces: \"1 5 6 13 15\")\n\n")
    i = 0
    list = []
    for a in folders:
        for b in os.listdir(path='.'+sl+a):
            if ".wav" in b:
                if not b.replace(".wav", "") in list:
                    i += 1
                    list.append(b.replace(".wav", ""))

    list.sort()
    ii = 0
    for a in list:
        ii += 1
        print(str(ii) + " - " + a)
    
    inp = input("\n >> ")

    for a in inp.split(" "):
        if str.isnumeric(a) and int(a) <= i and int(a) > 0:
            if not int(a) in list:
                wavs.append(list[int(a)-1])

    name = input("Enter output folder name(it will be located one folder up): ")

    for a in folders:
        inputs = ""
        incount = 0

        for b in os.listdir(path='.'+sl+a):
            if b.replace(".wav", "") in wavs:
                if mode == 0:
                    if os.path.isfile(a+sl+b):
                        inputs += '-i "'+ a+sl+b +'" '
                        incount += 1
            else:
                if mode == 1:
                    if os.path.isfile(a+sl+b):
                        inputs += '-i "'+ a+sl+b +'" '
                        incount += 1
        
            

        if not os.path.isdir(".."+sl+name): os.makedirs(".."+sl+name)
        print(len(wavs))
        cmd = 'ffmpeg '+inputs+'-filter_complex amix=inputs='+str(incount)+':duration=longest "..'+sl+name+sl+a+'.wav"'
        print(cmd)
        os.system(cmd)

    count = 0
    folders = []
    wavs = []

    begining()

def begining():
    menu = ConsoleMenu("Wav-Selector", "Dirty script for making raw mix from multitrack wavs, that located in subfolders of this folder")

    mix_everything = FunctionItem("Mix everything", select_mode, [])
    mix_one        = FunctionItem("Mix one",        select_folder, [])
    mix_few        = FunctionItem("Mix few",        select_folders, [])

    menu.append_item(mix_everything)
    menu.append_item(mix_one)
    menu.append_item(mix_few)

    menu.show()

begining()
