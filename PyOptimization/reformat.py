import os
import numpy
import platform
import fnmatch
import sqlite3
import configparser
import pyoptimization.utility

def reformat(cursor, table, path, reformat, delimiter = '\t'):
	data = numpy.loadtxt(path, dtype = bytes, ndmin = 2).astype(str)
	pathBase = os.path.splitext(path)[0]
	for ext, _data in reformat(data):
		_path = pathBase + ext
		numpy.savetxt(_path, _data, fmt = '%s', delimiter = delimiter)

def main():
	config = configparser.ConfigParser()
	pyoptimization.utility.read_config(config, __file__)
	name = os.path.splitext(os.path.basename(__file__))[0]
	pathRoot = config.get(name, 'root.' + platform.system())
	pattern = config.get(name, 'pattern')
	reformat = eval(config.get(name, 'reformat'))
	conn = sqlite3.connect(os.path.expandvars(config.get('database', 'file.' + platform.system())))
	table = config.get('database', 'table')
	cursor = conn.cursor()
	paths = []
	for pathParent, _, fileNames in os.walk(pathRoot):
		for fileName in fileNames:
			if fnmatch.fnmatch(fileName, pattern):
				path = os.path.join(pathParent, fileName)
				paths.append(path)
	for path in paths:
		print(path)
		reformat(cursor, table, path, reformat)
	conn.commit()
	print('Finished normally')

if __name__ == '__main__':
	main()