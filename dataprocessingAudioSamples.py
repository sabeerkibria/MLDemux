#Sound Related Imports
import soundfile as sf
from scipy import signal

#Math Related Imports
import numpy as np
import matplotlib.pyplot as plt
import cmath
import png

#OS Related Functions
from os import walk
import os

#Starting Variables (Deprecated)
outputdpi=100

#Function to Transform the data if you want to change the scaling transform. This Just does a simple normalization
def TransformScaling(data):
    data=data/(np.amax(data))
    return data
#Function that Trims off all silent portions
def TrimSF(data):
    loopcomplete=False
    startpoint=0
    endpoint=0
    for x in range(len(data)):
        if data[x]!=0 and loopcomplete==False:
            startpoint=x-1
            loopcomplete=True
    loopcomplete=False
    for y in range(len(data)):
        if data[len(data)-1-y]!=0 and loopcomplete==False:
            endpoint=len(data)-y+1
            loopcomplete=True
    if endpoint<=startpoint or endpoint>=len(data)-1:
        endpoint=len(data)
    finaldata=data[startpoint:endpoint]
    return finaldata

#Generates a Grayscale Spectrogram
def GrayscaleSpectrogram(
    filepath,
    filename,
    outputdirectory,
    stepsize=1000,maxfrequency=8191,trimdata=True):
    #Grabs data from sound file
    data,fs=sf.read(filepath+'\\'+filename,dtype='float32')
    filename=filename.replace('.wav','')
    #Trims the data of silence before Generation of Spectrogram
    if trimdata==True:
        data=TrimSF(data)
    #Gets the STFT and generates Spectrogram
    f, t, Zxx = signal.stft(data, fs, nperseg=stepsize)
    #Normalizes and takes the absolute of Zxx
    ZxxPix=np.abs(Zxx)
    ZxxPix=TransformScaling(ZxxPix)
    #Discretization of Zxx into Pixel Values for 16 bit PNG
    ZxxPix=np.round(ZxxPix*65535)
    #Discretization of Frequency Values
    f_discrete=np.round(f)
    f_discrete=f_discrete.astype(int)
    #Cuts out Frequencies outside of range and discretizes data
    ZxxPix=ZxxPix[0:(np.amax(np.argwhere(f_discrete<maxfrequency))+1),:]
    ZxxPix=ZxxPix.astype(np.uint16)
    #Initializes Data Structure for Grayscale Spectrogram
    SpectrogramGS=np.zeros((maxfrequency+1,len(t)))
    SpectrogramGS=SpectrogramGS.astype(np.uint16)
    #Writes Data to the respective Frequency bin in Spectrogram
    for i in range(ZxxPix.shape[0]):
        SpectrogramGS[f_discrete[i]]=ZxxPix[i]
    #Flips the Spectrogram Data so that the low frequencies are at the bottom and writes the spectrogram to a png
    SpectrogramGS=np.flipud(SpectrogramGS)
    with open(outputdirectory+'\\'+filename+'.png', 'wb') as f:
        writer = png.Writer(width=SpectrogramGS.shape[1], height=SpectrogramGS.shape[0], bitdepth=16, greyscale=True)
        SpectrogramGSList=SpectrogramGS.tolist()
        writer.write(f, SpectrogramGSList)
    print(filename+'.png'+' Written to '+outputdirectory)

#Generates Phase Information for the Purpose of reconstruction
def GeneratePhaseGraph(
    filepath,
    filename,
    outputdirectory,
    stepsize=1000,maxfrequency=8191,trimdata=True):
    #Grabs data from sound file
    data,fs=sf.read(filepath+'//'+filename,dtype='float32')
    filename=filename.replace('.wav','')
    #Trims the data of silence before Generation of Spectrogram
    if trimdata==True:
        data=TrimSF(data)
    #Gets the STFT
    f, t, Zxx = signal.stft(data, fs, nperseg=stepsize)
    #Discretizes the Frequency Values and converts to integer values
    f_discrete=np.round(f)
    f_discrete=f_discrete.astype(int)
    #Gets array dimensions of Zxx and generates Phase Data
    ArrayShape=list(Zxx.shape)
    #Converts all Phase to be in between 0 and 2 pi
    ZxxPhase=np.zeros((ArrayShape[0],ArrayShape[1]))
    for x in range(ArrayShape[0]):
        for y in range(ArrayShape[1]):
            ZxxPhase[x,y]=cmath.phase(Zxx[x,y])
            if ZxxPhase[x,y]<0:
                ZxxPhase[x,y]=2*np.pi+ZxxPhase[x,y]
    #Compacts Phase data to only include up to the max frequency and reverses data to keep it consistent with Spectrogram
    ZxxPhase=ZxxPhase[0:(np.amax(np.argwhere(f_discrete<maxfrequency))+1),:]
    ZxxPhase=np.flipud(ZxxPhase)
    #Writes output as binary .npy file
    outputdirectory=outputdirectory.replace('//','\\')
    np.save(outputdirectory+'\\'+'Phase\\'+filename+'.npy', ZxxPhase)

#Only for Sound Samples
for i in range(len(filenames)):
    GrayscaleSpectrogram(datafolder,filenames[i],outfolder,1000)
    GeneratePhaseGraph(datafolder,filenames[i],outfolder,1000)

#Creates Training List if it doesn't exist
if os.path.exists(mdl_folder+'train.csv'):
    _,_, samples=walk(datafolder)

else:
#Creates Training List and

#Outputs a Grayscale Normalized Representation of Spectrogram in 16 bit Grayscale PNG
