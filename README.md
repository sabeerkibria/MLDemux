# MLDemux
Uses ML to demux Audio Based on Samples of components

Has the following components:

1)Generates Phase and BW Spectrograms of the Data for analysis by a neural network

2)A Convolution Neural Network to detect Spectrograms of type of sound you're trying to isolate

3)Phase based Audio Reconstruction and output of ".wav" for the instrument you're trying to isolate

Please note that all data coming in needs to be in mono format. In theory you could apply this to multi-channel audio by separating out the multiple channels and feeding it back into the Demuxer individually per channel. The Spectrogram Generated is a normalized Spectrogram  
