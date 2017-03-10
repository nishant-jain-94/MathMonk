import os
import csv
import json

def read_corpus(fileid, extension='csv'):
	current_directory = os.path.dirname(__file__)
	data_directory = os.path.join(current_directory, 'data/')
	file_path =  os.path.join(data_directory, fileid)
	file_path += '.{}'.format(extension)
	data = None
	if os.path.exists(file_path):
		with open(file_path) as corpus:
			if extension == "csv":
				reader = csv.reader(corpus)
				data = list(reader)
			elif extension == "json":
				data = json.load(corpus)
	return data

