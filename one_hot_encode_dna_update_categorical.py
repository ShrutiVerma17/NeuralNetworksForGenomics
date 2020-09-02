# -*- coding: utf-8 -*-
"""one_hot_encode_dna_update_categorical.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SktXCMeXQQMhGeTxBN7m_9wj7EdiP9WG
"""

from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Convolution2D as Conv2D
from keras.layers import MaxPooling2D

import numpy
import random
import pickle

import os

# map letters to numbers
letter2num={'A':0,'C':1,'G':2,'T':3}

# get file length
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# encode a single sequence
def encode_seq(seq):
    d = numpy.zeros((4,len(seq)),numpy.int8)
    for i in range(len(seq)):
        d[letter2num[seq[i]],i]=1
    return d
    
def encode_seqs(seqs):
    x = numpy.zeros((len(seqs),4,len(seqs[0])),numpy.int8)
    # random sequence 
    for i in range(len(seqs)):
        x[i,:,:] = encode_seq(seqs[i])
    return x
    
def reverse_encode_seq(m):
    # convert a matrix to sequence
    ab = 'ACGT'
    seq = ''
    for i in range(m.shape[1]):
        seq = seq + ab[numpy.where(m[:,i]==1)[0][0]]
    return seq

def reverse_encode_seqs(m):
    seqs = []
    for i in range(m.shape[0]):
        seqs.append(reverse_encode_seq(m[i,:,:]))
    return seqs
    
# encoding N random sequences of length L
def random_encoded_seqs(N,L):
    x = numpy.zeros((N,4,L),numpy.int8)
    # random sequence 
    a=numpy.random.random_integers(0,3, size=(N,L))
    for i in range(N):
        for j in range(L):
            x[i,a[i,j],j] = 1
    return x
    

# encode all sequences in a file
# column 1 sequence, column 2 value
def load_data(filename):
    N=file_len(filename)
    f=open(filename)
    seq = f.readline().strip()
    x = numpy.zeros((N,4,len(seq)),numpy.int8)
    new_seq = seq.upper()
    x[0] = encode_seq(new_seq)
    y = numpy.zeros(N)
    if (seq.isupper()):
      y[0] = 1
    elif (seq.islower()):
      y[0] = 0
    elif (seq[0].isupper()):
      y[0] = 2
    elif (seq[1].isupper()):
      y[0] = 3
    i=1
    for line in f:
      seq = line.strip()
      new_seq = seq.upper()
      x[i] = encode_seq(new_seq)
      if (seq.isupper()):
        y[i] = 1
      elif (seq.islower()):
        y[i] = 0
      elif (seq[0].isupper()):
        y[i] = 2
      elif (seq[1].isupper()):
        y[i] = 3
      i=i+1
    f.close()
    return x,y
    
#### inforomation content of a pwm
# assume column sum = 1
def info(pwm):
    ic = 2.0*pwm.shape[1]
    for j in range(pwm.shape[1]): # each column
        for i in range(pwm.shape[0]):
            if pwm[i,j]>0:
                ic = ic + pwm[i,j]*numpy.log2(pwm[i,j])
    return ic/pwm.shape[1]
    
def layer1_motif_input(weights,x_train,alpha,activation_func,output_label):
    # weights=model.layers[0].get_weights()
    # used weights to score N random sequences of length L
    # use those active the neuron 70% of max activation to construct pwm
    # make motif logo using the pwm
    
    # example
    # layer1_motif(model.layers[0].get_weights(),1000000,0.7,'relu')
    
    # load weights
    # weights=pickle.load(open( "keras1-model-weights.pickle", "rb" ))
    # import pickle
    
    # length of the kernal/motif
    seqLen = weights[0].shape[1]
    
    # number of kernals
    nK = weights[0].shape[3]
    
    # scoring short sequences using the first layer
    model2 = Sequential()
    
    # layer 1
    model2.add(Conv2D(nK, kernel_size=(4, seqLen), activation=activation_func, input_shape=(4, seqLen, 1), weights=weights))
    # get output on input sequences
    activations=model2.predict(x_train)
    # find the max across sequences
    ma = numpy.amax(activations,axis=0)
    # normalize
    nw = activations/ma
    # for each filter, generate pwm for activation > 0.7
    for i in range(nK): # for each filter
        pwm = numpy.sum(x_train[nw[:,0,0,i]>alpha,:,:],axis=0)
        pwm = pwm[:,:,0]
        num = numpy.sum(pwm[:,0])
        if num < 50:
            continue
        pwm = pwm/float(num)
        ic = info(pwm)
        filename='-'.join([output_label,str(i),str(num),str(ic)])
        numpy.savetxt(filename,pwm,fmt='%f',delimiter='\t')
        # generate logo
        os.system('kpLogo '+filename+' -pwm -o '+filename) 
    os.system('tar zcvf '+output_label+'-pwm.tar.gz '+output_label+'*.info.png')  
    os.system('rm '+output_label+'*.pdf') 
    os.system('rm '+output_label+'*.eps')
    os.system('rm '+output_label+'*.png')
    
def layer1_motif(weights,N,alpha,activation_func,output_label):
    # weights=model.layers[0].get_weights()
    # used weights to score N random sequences of length L
    # use those active the neuron 70% of max activation to construct pwm
    # make motif logo using the pwm
    
    # example
    # layer1_motif(model.layers[0].get_weights(),1000000,0.7,'relu')
    
    # load weights
    # weights=pickle.load(open( "keras1-model-weights.pickle", "rb" ))
    # import pickle
    
    # length of the kernal/motif
    seqLen = weights[0].shape[1]
    
    # number of kernals
    nK = weights[0].shape[3]
    print(seqLen,nK)
    print("generate large number of random sequences...")
    rndseqs=random_encoded_seqs(N,seqLen)
    rndseqs_shape=(4,seqLen,1)
    rndseqs = rndseqs.reshape(rndseqs.shape[0], 4, seqLen, 1)
    
    # scoring short sequences using the first layer
    model2 = Sequential()
    
    # layer 1
    model2.add(Conv2D(nK, kernel_size=(4, seqLen), activation=activation_func, input_shape=rndseqs_shape, weights=weights))
    # get output on input sequences
    activations=model2.predict(rndseqs)
    # find the max across sequences
    ma = numpy.amax(activations,axis=0)
    # normalize
    nw = activations/ma
    # for each filter, generate pwm for activation > 0.7
    for i in range(nK): # for each filter
        pwm = numpy.sum(rndseqs[nw[:,0,0,i]>alpha,:,:],axis=0)
        pwm = pwm[:,:,0]
        num = numpy.sum(pwm[:,0])
        if num < 20:
            continue
        pwm = pwm/float(num)
        ic = info(pwm)
        filename='-'.join([output_label,str(ic),str(i),str(num)])
        numpy.savetxt(filename,pwm,fmt='%f',delimiter='\t')
        # generate logo
        os.system('kpLogo '+filename+' -pwm -o '+filename) 
    #os.system('rm '+output_label+'*.pdf') 
    os.system('rm '+output_label+'*.eps')
    os.system('rm '+output_label+'*freq*')
    os.system('tar zcvf '+output_label+'.tar.gz '+output_label+'*')
    os.system('rm '+output_label+"-*")