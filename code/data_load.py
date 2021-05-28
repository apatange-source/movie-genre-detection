# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 04:11:15 2020

@author: Aishwarya Patange
"""
import numpy as np 
import data_manage
from data_manage import list_movies, Movie

test_ratio = 7
val_ratio = 6

def load_data(min_year, max_year, genres, ratio, set_type, verbose = True):
    x = []
    y = []
    for year in reversed(range(min_year, max_year+1)):
        if verbose == True:
            print('loading', set_type, 'data, movies from year', year, '...')
        x_year, y_year = load_data_by_year(year, genres, ratio, set_type)
        add_to(x_year, x)
        add_to(y_year, y)
        
        if verbose == True:
            print('movies loaded:', len(x_year))
    return np.concatenate(x), np.concatenate(y)

def load_data_by_year(year, genres, pos_ratio, set_type):
    x = []
    y = []
    count = 1
    for movie in list_movies(year, genres):
        if movie.poster_exists() == True:
            if ((set_type == 'train') and (movie.movie_id % test_ratio != 0) and (count % val_ratio != 0)) or ((set_type == 'validate') and (movie.movie_id % test_ratio != 0) and (count % val_ratio == 0)) or ((set_type == 'test') and (movie.movie_id % test_ratio == 0)):
                x1 = movie.img_to_rgb(pos_ratio)
                y1 = movie.genres_to_vector(genres)
                x.append(x1)
                y.append(y1)
            count += 1
    x = np.array(x, dtype = 'float32')
    y = np.array(y, dtype = 'uint8')
    return x, y

def add_to(array1d, array2d):
    if len(array1d) > 0:
        array2d.append(array1d)

                
