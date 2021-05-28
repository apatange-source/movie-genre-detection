# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 05:45:21 2020

@author: Aishwarya Patange
"""
import model
import data_load
from data_load import load_data

epochs = 50
min_year = 1997
max_year = 2017
ratios = [30, 40, 50, 60, 70]
lrates = [0.001, 1e-4, 1e-5, 1e-6, 1e-7]
genres = ['Horror', 'Romance', 'Action', 'Documentary']

def main(ratios):
	'''
	Build the model across all hyper parameter settings
	'''

	for ratio in ratios:

		x_train, y_train = load_data(min_year, max_year, genres, ratio, 'train')
		x_val, y_val = load_data(min_year, max_year, genres, ratio, 'validate')

		for lr in lrates:

			model.build(1, min_year, max_year, genres, ratio, epochs, lr, x_train=x_train, x_val=x_val, y_train=y_train, y_val=y_val, verbose=True)

if __name__ == '__main__':
	main(ratios)