from __future__ import print_function
from tensorflow import convert_to_tensor
from tensorflow import float32
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Convolution2D as Conv2D
from tensorflow.keras.layers import MaxPooling2D
from keras.utils.np_utils import to_categorical
from one_hot_encode_dna_update_categorical import *

import numpy
import pickle
import argparse


def parse_args():
    parser=argparse.ArgumentParser(description="running neural network")
    parser.add_argument("--dir")
    parser.add_argument("--length")
    parser.add_argument("--balanced")
    return parser.parse_args()



def main():
    numpy.set_printoptions(threshold=numpy.inf)
    args=parse_args()
    my_dir = args.dir
    length = args.length
    balanced = args.balanced
    
    seqlen = length
    
    # model parameters
    epochs = 15
    batch_size = 500 
    dropout = 0.05    
    motiflen = 100      # motif length, to be used in the conv2d layer    
    nmotif = 1000     # number of motifs (# units in the conv2d layer)
    activation = 'relu'
    
    # fraction of samples to be used for training
    fraction_train = 0.90
    
    def to_one_hot(labels, dimensions=4):
      results = numpy.zeros((len(labels), dimensions))
      for i, label in enumerate(labels):
        results[i][int(label)] = 1
      return results
    
    # load data
    inputfile = ""
    if (balanced == "true"):
        inputfile=my_dirdir + "mega_imbalanced_file"
    else: 
        inputfile=my_dir + "mega_balanced_file"
    x, y  = load_data(inputfile)
    print(x.shape[0], 'samples loaded')
    ### split data into training and test
    indices = numpy.arange(x.shape[0])
    numpy.random.shuffle(indices)
    #print(indices)
    n_train = int(x.shape[0]*fraction_train)
    x = x[indices]
    y = y[indices]
    x_train = x[:n_train]
    y_train = y[:n_train]
    x_test = x[n_train:]
    y_test = y[n_train:]
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')
    
    x_train = x_train.reshape(x_train.shape[0], 4, seqlen, 1)
    x_test = x_test.reshape(x_test.shape[0], 4, seqlen, 1)
    one_hot_train_labels = to_one_hot(y_train)
    one_hot_test_labels = to_one_hot(y_test)
    input_shape = (4, seqlen, 1)
    model = Sequential()
    # layer 1: motifs
    model.add(Conv2D(nmotif, kernel_size=(4, motiflen), activation=activation, input_shape=input_shape))
    # if using convolution
    if seqlen > motiflen:
        model.add(MaxPooling2D(pool_size=(1, seqlen-motiflen+1)))
    model.add(Dropout(dropout))
    # layer 2: motif combination
    model.add(Dense(64, activation=activation))# relu
    model.add(Dropout(dropout))
    # layer 3: output
    model.add(Flatten())
    model.add(Dense(4,activation='softmax'))
    
    #model  = multi_gpu_model(model,gpus=4)
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) # adam, Nadam, Adamax, RMSprop,sgd,Adagrad,Adadelta
    #model.fit(x_train, y_train, epochs = epochs, batch_size = batch_size)
    #history_dict = history.history
    #training_acc = history_dict[acc]
    #training_loss = history_dict[loss]
    #test_acc = history_dict[val_acc]
    #test_loss = history_dict[val_loss]
    #print('Training Accuracy:', training_acc)
    #print('Training Loss:', training_loss)
    #print('Testing Accuracy:', test_acc)
    #print('Testing Loss:', test_loss)
    model.fit(x_train, one_hot_train_labels,
                  batch_size=batch_size,
                  epochs=epochs,
                  verbose=1,
                  validation_data=(x_test, one_hot_test_labels))
    #              callbacks=[keras.callbacks.EarlyStopping(monitor='val_loss',min_delta=0,patience=3,verbose=0, mode='auto',restore_best_weights=True)])
    score = model.evaluate(x_test, one_hot_test_labels)
    print('Test loss/accuracy:', score)

if __name__=="__main__":
    main()