# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 02:32:08 2020

@author: Aishwarya Patange
"""

import io
import os.path
import numpy as np
import pandas as pd
from PIL import Image
import urllib.request

images_dir = 'data/images/'
parsed_movies = []

class Movie:
    movie_id = 0
    title = ''
    year = 0
    genres = []
    poster_url = ''
    
    def poster_exists(self):
        return os.path.isfile(self.poster_file_path())
    
    def download_poster(self):
        try:
            response = urllib.request.urlopen(self.poster_url)
            data = response.read()
            file = open(self.poster_file_path(), 'wb')
            file.write(bytearray(data))
            file.close()
            return data
        except:
            print('Error Downloading Poster')
            
    def poster_file_path(self, size = 100):
        return images_dir + str(size) + '/' + self.poster_file_name()
    
    def poster_file_name(self):
        return str(self.movie_id) + '.jpg'
    
    def img_to_rgb(self, poster_size):
        path = images_dir + str(poster_size) + '/' + str(self.movie_id) + '.jpg'
        data = open(path, 'rb').read()
        img = Image.open(io.BytesIO(data))
        rgb_img = img.convert('RGB')
        pixels = []
        for i in range(img.size[0]):
            row = []
            for j in range(img.size[1]):
                r, g, b = rgb_img.getpixel((i, j))
                pixel = [r / 255, g / 255, b / 255]
                row.append(pixel)
            pixels.append(row)
        return pixels
    
    def genres_to_vector(self, genres):
        if len(genres) == 1:
            has_genre = self.has_genre(genres[0])
            return [int(has_genre), int (not has_genre)]
        else:
            vector = []
            if self.has_any_genre(genres):
                for genre in genres:
                    vector.append(int(self.has_genre(genre)))
            return vector
        
    def has_genre(self, genre):
        return genre in self.genres
    
    def has_any_genre(self, genres):
        return len(set(self.genres).intersection(genres)) > 0
    
    def is_valid(self) -> bool:
        return self.poster_url.startswith('https://') and 1900 <= self.year <= 2020 and len(self.title) > 1 and len(self.genres) > 1
    
    def __str__(self):
        return str(self.title) + '(' + str(self.year) + ')'
    
def download_posters(min_year = 0):
    for movie in list_movies():
        print(str(movie))
        if movie.year >= min_year:
            if movie.poster_exists() == False:
                movie.download_poster()
                if movie.poster_exists() == True:
                    print('Downloaded')
                else:
                    print('Cannot Download')
            else:
                print('Already Downloaded')
        else:
            print('Movie Came Out Before min_year')
            
def list_movies(year = None, genres = None):
    if (len(parsed_movies) == 0):
        data = pd.read_csv('data/MovieGenre.csv', encoding = 'ISO-8859-1')
        for i, r in data.iterrows():
            movie = parse_row(r)
            if movie.is_valid():
                parsed_movies.append(movie)
        parsed_movies.sort(key = lambda m : m.movie_id)
    result = parsed_movies    
    if year != None:
        result = [movie for movie in result if movie.year == year]    
    if genres != None:
        result = [movie for movie in result if movie.has_any_genre(genres)]
    
    return result

def parse_row(row):
    movie = Movie()
    movie.movie_id = int(row['imdbId'])
    movie.title = row['Title'][:-7]
    year = row['Title'][-5 : -1]
    if year.isdigit() and len(year)==4:
        movie.year = int(year)
    url = str(row['Poster'])
    if len(url) > 0:
        movie.poster_url = url.replace('"', '')
    genre_str = str(row['Genre'])
    if (len(genre_str) > 0):
        movie.genres = genre_str.split('|')
    return movie
    
def search_movie(movie_id = None, title = None):
    movies = list_movies()
    for movie in movies:
        if movie_id is not None and movie.movie_id == movie_id:
            return movie 
        if title is not None and movie.title == title:
            return movie
        
def list_movies_external(year = None, genres = None):
    if len(parsed_movies) == 0:
        data = pd.read_csv('data/MovieGenre_external.csv', encoding='ISO-8859-1')
        for i, r in data.iterrows():
            movie = parse_row(r)
            if movie.is_valid():
                parsed_movies.append(movie)
            parsed_movies.sort(key=lambda m: m.movie_id)
    result = parsed_movies
    if year != None:
        result = [movie for movie in result if movie.year == year]
    if genres != None:
        result = [movie for movie in result if movie.has_any_genre(genres)]
    return result

def search_movie_external(movie_id=None, title=None):
	movies = list_movies_external()
	for movie in movies:
		if movie_id is not None and movie.movie_id == movie_id:
			return movie 
		if title is not None and movie.title == title:
			return movie 
