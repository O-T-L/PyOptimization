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
import math
import numpy
import fnmatch
import matplotlib.pyplot
import mpl_toolkits.mplot3d
import configparser

def dtlz7_shape(decision, distance):
	return len(decision) + 1 - sum([(math.sin(3 * math.pi * x) + 1) * x / distance for x in decision])

def draw_dtlz1_2(config, ax):
	ax.plot([0.5, 0], [0, 0.5])

def draw_dtlz2_2(config, ax, resolution = 100):
	u = numpy.linspace(0, numpy.pi / 2, resolution)
	x = numpy.cos(u)
	y = numpy.sin(u)
	ax.plot(x, y)

def draw_dtlz7_2(config, ax, resolution = 100):
	x = numpy.linspace(0, numpy.pi / 2, resolution)
	y = numpy.zeros(x.shape)
	distance = 2
	y.flat = [distance * dtlz7_shape([_x], distance) for _x in x]
	ax.plot(x, y)

def draw_dtlz1_3(config, ax):
	polygon = mpl_toolkits.mplot3d.art3d.Poly3DCollection([[
		(0.5, 0, 0),
		(0, 0.5, 0),
		(0, 0, 0.5)]], facecolors = 'white')
	ax.add_collection3d(polygon)

def draw_dtlz2_3(config, ax, resolution = 10):
	u, v = numpy.mgrid[0 : 1 : resolution * 1j, 0 : 1 : resolution * 1j] * numpy.pi / 2
	x = numpy.cos(u) * numpy.cos(v)
	y = numpy.sin(u) * numpy.cos(v)
	z = numpy.sin(v)
	ax.plot_surface(x, y, z, color = 'red', linewidth = 0, alpha = 0.2)

def draw_dtlz5_3(config, ax, resolution = 20):
	v = numpy.linspace(0, numpy.pi / 2, resolution)
	z = numpy.cos(v)
	r = numpy.sin(v)
	alpha = math.pi / 4
	x = r * math.cos(alpha)
	y = r * math.sin(alpha)
	ax.plot(x, y, z)

def draw_dtlz7_3(config, ax, resolution = 20):
	x, y = numpy.mgrid[0 : 1 : resolution * 1j, 0 : 1 : resolution * 1j]
	z = numpy.zeros(x.shape)
	distance = 2
	z.flat = [distance * dtlz7_shape([_x, _y], distance) for _x, _y in zip(x.flat, y.flat)]
	ax.plot_surface(x, y, z, cmap = matplotlib.cm.get_cmap('jet'), rstride = 1, cstride = 1, linewidth = 0, alpha = 0.2)

def draw_distribution2(config, ax, population):
	problem = config.get('pf', 'problem')
	if problem == 'DTLZ1':
		draw_dtlz1_2(config, ax)
	elif problem == 'DTLZ2':
		draw_dtlz2_2(config, ax)
	elif problem == 'DTLZ7':
		draw_dtlz7_2(config, ax)
	ax.plot(population.T[0], population.T[1], 'o')
	ax.set_xlabel(r"$f_{1}$")
	ax.set_ylabel(r"$f_{2}$")

def draw_distribution3(config, ax, population):
	problem = config.get('pf', 'problem')
	if problem == 'DTLZ1':
		draw_dtlz1_3(config, ax)
	elif problem == 'DTLZ2':
		draw_dtlz2_3(config, ax)
	elif problem == 'DTLZ5':
		draw_dtlz5_3(config, ax)
	elif problem == 'DTLZ7':
		draw_dtlz7_3(config, ax)
	ax.view_init(azim = config.getfloat('3d', 'azimuth'), elev = config.getfloat('3d', 'elevation'))
	ax.plot(population.T[0], population.T[1], population.T[2], 'o')
	ax.set_xlabel(r"$f_{1}$")
	ax.set_ylabel(r"$f_{2}$")
	ax.set_zlabel(r"$f_{3}$")

def plot_data(config, ax, data):
	dimension = len(data[0])
	x = list(range(dimension))
	for point in data:
		ax.plot(x, point)

def draw_parallel_coordinates(config, ax, data):
	dimension = len(data[0])
	plot_data(config, ax, data)
	ax.set_xticklabels([])
	ax.set_xticks(list(range(dimension)))
	ax.set_xticklabels([r'$f_{%u}$' % axis for axis in range(1, dimension + 1)])

def draw(config, population, title):
	fig = matplotlib.pyplot.figure(title)
	if len(population[0]) == 2:
		ax = fig.gca()
		draw_distribution2(config, ax, population)
	elif len(population[0]) == 3:
		ax = mpl_toolkits.mplot3d.Axes3D(fig)
		draw_distribution3(config, ax, population)
	else:
		ax = fig.gca()
		draw_parallel_coordinates(config, ax, population)
	try:
		lower, upper = map(int, config.get('limits', 'x').split())
		ax.set_xlim(lower, upper)
	except (configparser.NoSectionError, configparser.NoOptionError):
		pass
	try:
		lower, upper = map(int, config.get('limits', 'y').split())
		ax.set_ylim(lower, upper)
	except (configparser.NoSectionError, configparser.NoOptionError):
		pass
	try:
		lower, upper = map(int, config.get('limits', 'z').split())
		ax.set_zlim(lower, upper)
	except (configparser.NoSectionError, configparser.NoOptionError):
		pass
	return fig

def main():
	config = configparser.ConfigParser()
	config.read(os.path.splitext(__file__)[0] + '.ini')
	
	matplotlib.rcParams['font.size'] *= config.getfloat('config', 'fontsize')
	dataFolder = os.path.expandvars(config.get('config', 'data_folder.' + platform.system()))
	figureFolder = os.path.expandvars(config.get('config', 'figure_folder.' + platform.system()))
	pattern = config.get('config', 'data_pattern')
	figureExt = config.get('config', 'figure_ext')
	for parent, _, filenames in os.walk(dataFolder, followlinks = True):
		for filename in filenames:
			if fnmatch.fnmatch(filename, pattern):
				path = os.path.join(parent, filename)
				population = numpy.loadtxt(path, ndmin = 2)
				fig = draw(config, population, path)
				if config.getboolean('switch', 'save'):
					pathFigure = os.path.join(figureFolder, os.path.splitext(os.path.relpath(path, dataFolder))[0]) + figureExt
					print(path + ' -> ' + pathFigure)
					try:
						os.makedirs(os.path.dirname(pathFigure))
					except OSError:
						pass
					fig.savefig(pathFigure)
	if config.getboolean('switch', 'show'):
		matplotlib.pyplot.show()

if __name__ == '__main__':
	main()
