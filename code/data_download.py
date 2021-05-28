# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 03:56:13 2020

@author: Aishwarya Patange
"""
import os 
import sys
import data_manage as dm

def download(min_year, ratios, images_dir, original_images_dir):
    if os.path.isdir(original_images_dir) == False:
        os.makedirs(original_images_dir)
    dm.download_posters(min_year = min_year)
    for r in ratios:
        path = images_dir + str(r)
        if os.path.isdir(path) == False:
            os.makedirs(path)
            command = 'mogrify -path "' + path + '/" -resize ' + str(r) + '% "' + original_images_dir + '*.jpg"'
            print(command)
            os.system(command)
    return True

def main():
    min_year = 1990
    resizes = [30, 40, 50, 60, 70]
    images_dir = 'data/images/'
    original_images_dir = 'data/images/100/'
    status = download(min_year, resizes, images_dir, original_images_dir)
    return status

if __name__ == '__main__':
    main()
