#Sound Related Imports
import soundfile as sf
from scipy import signal

#Math Related Imports
import numpy as np
import matplotlib.pyplot as plt

#OS and UI Related Imports
from tkinter import filedialog
from tkinter import *
import msvcrt as m
import os

#Creates a function that waits for User Input
def wait():
    m.getch()

#Creates Dialog to select the folder from which to import data from
print("Select a folder for Samples")
root = Tk()
root.withdraw()
datafolder = filedialog.askdirectory()
datafolder = datafolder.replace('/','\\')

print('Selected folder for Samples is '+datafolder)
wait()
#Creates a dialogue to select path for model saving and loading
print("Select a folder for Models")
root = Tk()
root.withdraw()
mdl_folder = filedialog.askdirectory()
mdl_folder = mdl_folder.replace('/','\\')
print('Selected folder for models is '+mdl_folder)
wait()

#Selects folder for output of spectrogram and phase
root = Tk()
root.withdraw()
outfolder = filedialog.askdirectory()
outfolder = outfolder.replace('/','\\')
print('Selected folder for output is '+mdl_folder)
wait()

(_, _, filenames) = next(os.walk(datafolder))
#Launches whatever python file needs to be executed next. Change execute.py with desired file
