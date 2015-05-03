"""
Copyright (C) 2014, 申瑞珉 (Ruimin Shen)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import platform
import sqlite3
import csv
import configparser
import pyoptimization.utility

def get_data_settings(path, delimiter = '\t'):
	f = open(path, 'r')
	reader = csv.reader(f, delimiter = delimiter)
	dataSettings = {}
	for ext, column, converter in reader:
		converter = eval(converter)
		dataSettings[ext] = (column, converter)
	return dataSettings

def get_properties_settings(path, delimiter = '\t'):
	f = open(path, 'r')
	reader = csv.reader(f, delimiter = delimiter)
	propertiesSettings = []
	for column, converter in reader:
		converter = eval(converter)
		propertiesSettings.append((column, converter))
	return propertiesSettings

def full_split_path(path):
	components = []
	while True:
		path, folder = os.path.split(path)
		if folder:
			components.append(folder)
		else:
			if path:
				components.append(path)
			break
	components.reverse()
	return components

def get_properties(components, propertiesSettings):
	properties = []
	for column, converter in propertiesSettings:
		properties.append((column, converter(components)))
	return properties

def group_names(filenames):
	groups = {}
	for filename in filenames:
		name, ext = os.path.splitext(filename)
		if name in groups:
			groups[name].append(ext)
		else:
			groups[name] = [ext]
	return groups

def group_properties(name, group, dataSettings, parent):
	properties = []
	for ext in group:
		if ext in dataSettings:
			filename = name + ext
			pathData = os.path.join(parent, filename)
			if not os.path.isdir(pathData):
				column, converter = dataSettings[ext]
				f = open(pathData, 'r')
				data = f.read()
				f.close()
				data = converter(data)
				properties.append((column, data))
	return properties

def main():
	config = configparser.ConfigParser()
	pyoptimization.utility.read_config(config, __file__)
	# Database
	dataSettings = get_data_settings(os.path.expandvars(config.get('importer', 'data_settings')))
	propertiesSettings = get_properties_settings(os.path.expandvars(config.get('importer', 'properties_settings')))
	root = os.path.expandvars(config.get('importer', 'root.' + platform.system()))
	conn = sqlite3.connect(os.path.expandvars(config.get('database', 'file.' + platform.system())))
	table = config.get('database', 'table')
	cursor = conn.cursor()
	for parent, _, filenames in os.walk(root):
		groups = group_names(filenames)
		for name in groups:
			properties = group_properties(name, groups[name], dataSettings, parent)
			if properties:
				path = os.path.join(parent, name)
				pathRelative = os.path.relpath(path, root)
				print(path + '.*')
				components = full_split_path(pathRelative)
				_properties = get_properties(components, propertiesSettings)
				print (_properties)
				properties += _properties
				# Insert into database
				columns, rowData = zip(*properties)
				sql = 'INSERT INTO %s %s VALUES (%s)' % (table, str(columns), ', '.join(['?'] * len(rowData)))
				cursor.execute(sql, rowData)
	conn.commit()
	print('Finished normally')

if __name__ == '__main__':
	main()