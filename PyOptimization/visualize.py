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

import sys
import os
import importlib
import platform
import io
import csv
import sqlite3
import configparser
import numpy
import matplotlib.pyplot
import matplotlib.backends.backend_qt4agg
from PyQt4 import QtCore, QtGui
import pyoptimization.utility

class Visualizer(QtGui.QDialog):
	def __init__(self, parent, title, creators, initialers, drawers, progressColumns, progressTable, dataDictList):
		super(Visualizer, self).__init__(parent)
		self.setWindowTitle(title)
		assert(len(creators) == len(initialers) == len(drawers))
		self.drawers = drawers
		self.progressColumns = progressColumns
		assert(len(progressTable) == len(dataDictList))
		self.progressTable = progressTable
		self.dataDictList = dataDictList
		layout = QtGui.QVBoxLayout(self)

		self.tabMain = QtGui.QTabWidget()
		self.axes = []
		self.removers = []
		for name, creator in creators:
			panel = QtGui.QWidget()
			self.tabMain.addTab(panel, name)
			_layout = QtGui.QVBoxLayout(panel)
			fig = matplotlib.pyplot.Figure()
			canvas = matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg(fig)
			ax = creator(fig, self.dataDictList)
			self.axes.append(ax)
			_layout.addWidget(canvas)
			toolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QTAgg(canvas, panel)
			_layout.addWidget(toolbar)
			self.removers.append([])
		for ax, initialer in zip(self.axes, initialers):
			if ax and initialer:
				initialer(ax, self.dataDictList)

		self.tabMain.currentChanged[int].connect(self.on_page_changed)
		layout.addWidget(self.tabMain)
		self.progress = QtGui.QLabel()
		layout.addWidget(self.progress)
		if len(self.progressTable) > 1:
			self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
			self.slider.setRange(0, len(self.progressTable) - 1)
			self.slider.valueChanged[int].connect(self.on_progress)
			layout.addWidget(self.slider)
			
			text = self.get_progress_text(self.slider.value())
			self.progress.setText(text)
			self.draw(self.slider.value())
		else:
			text = self.get_progress_text(0)
			self.progress.setText(text)
			self.draw(0)
	
	def get_progress_text(self, progressIndex):
		return ','.join([column + '=' + str(progress) for column, progress in zip(self.progressColumns, self.progressTable[progressIndex])])
	
	def on_progress(self, index):
		text = self.get_progress_text(index)
		self.progress.setText(text)
		self.draw(index)
	
	def on_page_changed(self, index):
		if 'slider' in self.__dict__:
			self.draw(self.slider.value())
		else:
			assert(len(self.progressTable) == 1)
			self.draw(0)
	
	def draw(self, progressIndex):
		visualizeIndex = self.tabMain.currentIndex()
		ax = self.axes[visualizeIndex]
		drawer = self.drawers[visualizeIndex]
		if ax and drawer:
			for remover in self.removers[visualizeIndex]:
				remover()
			self.removers[visualizeIndex] = drawer(ax, self.dataDictList[progressIndex])
			canvas = self.tabMain.currentWidget().layout().itemAt(0).widget()
			canvas.draw()
			matplotlib.pyplot.draw()

def read_csv(path, delimiter = '\t'):
	f = open(path, 'r')
	reader = csv.reader(f, delimiter = delimiter)
	return [[cell for cell in row] for row in reader]

class DataSelector(QtGui.QWidget):
	def __init__(self, parent, config):
		super(DataSelector, self).__init__(parent)
		self.config = config
		self.configure(config)
		layout = QtGui.QVBoxLayout(self)
		
		self.tableData = QtGui.QTableWidget(0, len(self.groupColumns))
		self.tableData.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tableData.setHorizontalHeaderLabels(self.groupColumns)
		self.tableData.cellDoubleClicked.connect(self.visualize)
		layout.addWidget(self.tableData)
		
		self.buttonRefresh = QtGui.QPushButton('Refresh')
		self.buttonRefresh.clicked.connect(self.refresh)
		layout.addWidget(self.buttonRefresh)
		
		self.refresh()
	
	def configure(self, config):
		self.pathDatabase = os.path.expandvars(config.get('database', 'file.' + platform.system()))
		self.groupColumns = config.get('database', 'group_columns').split()
		self.progressColumns = config.get('database', 'progress_columns').split()
	
	def refresh(self):
		conn = sqlite3.connect(self.pathDatabase)
		cursor = conn.cursor()
		self.groupTable = self.all_groups(cursor)
		self.tableData.setRowCount(len(self.groupTable))
		for groupIndex, group in enumerate(self.groupTable):
			assert(len(group) == len(self.groupColumns))
			for itemIndex, item in enumerate(group):
				item = QtGui.QTableWidgetItem(str(item))
				item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
				self.tableData.setItem(groupIndex, itemIndex, item)
		conn.close()

	def visualize(self, row, col):
		group = self.groupTable[row]
		progressTable, dataDictList = self.query_group_data(group)
		properties = dict(zip(self.groupColumns, group))
		module, function = self.config.get('visualizer', 'creator').rsplit('.', 1)
		module = importlib.import_module(module)
		creators = getattr(module, function)(properties)
		module, function = self.config.get('visualizer', 'initialer').rsplit('.', 1)
		module = importlib.import_module(module)
		function = getattr(module, function)
		initialers = [function(name, properties) for name, _ in creators]
		module, function = self.config.get('visualizer', 'drawer').rsplit('.', 1)
		module = importlib.import_module(module)
		function = getattr(module, function)
		drawers = [function(name, properties) for name, _ in creators]
		widget = Visualizer(self, str(group), creators, initialers, drawers, self.progressColumns, progressTable, dataDictList)
		widget.show()

	def all_groups(self, cursor):
		table = self.config.get('database', 'table')
		group = ','.join(['"%s"' % column for column in self.groupColumns])
		try:
			condition = self.config.get('database', 'condition')
			sql = 'SELECT %s FROM %s WHERE %s GROUP BY %s' % (group, table, condition, group)
		except configparser.NoOptionError:
			sql = 'SELECT %s FROM %s GROUP BY %s' % (group, table, group)
		cursor.execute(sql)
		return cursor.fetchall()
	
	def query_group_data(self, group):
		dataColumns = self.config.get('database', 'data_columns').split()
		table = self.config.get('database', 'table')
		conn = sqlite3.connect(self.pathDatabase)
		cursor = conn.cursor()
		_dataColumns = ','.join(['"%s"' % column for column in dataColumns])
		_progressColumns = ','.join(['"%s"' % column for column in self.progressColumns])
		_groupColumns = ' AND '.join(['"%s"=?' % column for column in self.groupColumns])
		sql = 'SELECT %s FROM %s WHERE %s ORDER BY %s' % (_dataColumns, table, _groupColumns, _progressColumns)
		cursor.execute(sql, group)
		dataTable = cursor.fetchall()
		conn.close()
		dataDictList = [self.cache_data(dict(zip(*(dataColumns, rowData)))) for rowData in dataTable]
		progressTable = [[dataDict[column] for column in self.progressColumns] for dataDict in dataDictList]
		return progressTable, dataDictList
	
	def cache_data(self, dataDict):
		try:
			for column in self.config.get('cache', 'matrix').split():
				data = dataDict[column]
				if data:
					f = io.BytesIO(data)
					dataDict[column] = numpy.loadtxt(f, ndmin = 2)
					f.close()
				else:
					del dataDict[column]
		except configparser.NoOptionError:
			pass
		try:
			for column in self.config.get('cache', 'vector').split():
				data = dataDict[column]
				if data:
					f = io.BytesIO(data)
					dataDict[column] = numpy.loadtxt(f)
					f.close()
				else:
					del dataDict[column]
		except configparser.NoOptionError:
			pass
		return dataDict

def main():
	config = configparser.ConfigParser()
	pyoptimization.utility.read_config(config, __file__)
	app = QtGui.QApplication(sys.argv)
	main = DataSelector(None, config)
	main.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()