# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 05:10:32 2020

@author: Aishwarya Patange
"""
import os
import keras
import pickle
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dense, Dropout, Flatten


def build(style, min_year, max_year, genres, ratio, epochs, lrate = 0.001, x_train = None, x_val = None, y_train = None, y_val = None, verbose = True):
    if verbose:
        print('')
        print('x_train shape: ', x_train.shape)
        print('y_train shape: ', y_train.shape)
        print('x_val shape: ', x_val.shape)
        print('y_val shape: ', y_val.shape)
        print('train samples: ', x_train.shape[0])
        print('validation samples: ', x_val.shape[0])
        print('')
    num_classes = len(y_train[0])
    
    model = Sequential([
        
        Conv2D(32, (3, 3), input_shape = x_train.shape[1:]),
        Activation('relu'),
        MaxPooling2D(pool_size = (2, 2)),
        
        Conv2D(32, (3, 3)),
        Activation('relu'),
        MaxPooling2D(pool_size = (2, 2)),
        
        Conv2D(64, (3, 3)),
        Activation('relu'),
        MaxPooling2D(pool_size = (2, 2)),
        
        Flatten(),
        Dense(64),
        Activation('relu'),
        Dropout(0.5),
        
        Dense(32),
        Activation('relu'),
        Dropout(0.5),
        
        Dense(num_classes),
        Activation('softmax'),
        
        ])
    
    new_adam = keras.optimizers.Adam(lr = lrate, beta_1 = 0.9, beta_2 = 0.999, decay = 0.0, amsgrad = False)
    
    model.compile(
        loss = 'categorical_crossentropy',
        optimizer = new_adam,
        metrics = ['accuracy']
        )
    print(model.summary())
    h = model.fit(
        x_train,
        y_train,
        batch_size = 32,
        epochs = epochs,
        validation_data = (x_val, y_val)
        )
    save_dir = os.path.join(os.getcwd(), 'cnn_model_results/models1')
    if os.path.isdir(save_dir) == False:
        os.makedirs(save_dir)
    model_name = 'genres' + '_' + str(min_year) + '_' + str(max_year) + '_g' + str(len(genres)) + '_r' + str(ratio) + '_e' + str(epochs) + '_v' + str(style) + '_lr' + str(lrate) + '.h5'
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    
    save_dir_2 = os.path.join(os.getcwd(), 'cnn_model_results/hists1')
    if os.path.isdir(save_dir_2) == False:
        os.makedirs(save_dir_2)
    hist_name = 'hists' + '_' + str(min_year) + '_' + str(max_year) + '_g' + str(len(genres)) + '_r' + str(ratio) + '_e' + str(epochs) + '_v' + str(style) + '_lr' + str(lrate) + '.pkl'
    hist_path = os.path.join(save_dir_2, hist_name)
    
    with open(hist_path, 'wb') as f:
        pickle.dump(h.history, f)
    print('Saved trained model at %s ' % model_path)
    
    