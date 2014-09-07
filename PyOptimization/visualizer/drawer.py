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

import numpy

def relim(ax, data):
	if data.shape[1] == 3:
		x, y, z = data.T
		ax.auto_scale_xyz(x, y, z)
	else:
		ax.relim()

def plot1(ax, data):
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	assert(dimension == 1)
	data = numpy.hstack(data)
	bar = ax.bar(list(range(len(data))), data)
	return lambda: bar.remove()

def plot2(ax, data):
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	assert(dimension == 2)
	x, y = data.T
	points, = ax.plot(x, y, 'o')
	return lambda: points.remove()

def plot3(ax, data):
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	assert(dimension == 3)
	x, y, z = data.T
	points, = ax.plot(x, y, z, 'o')
	return lambda: points.remove()

def plot_parallel_coordinates(ax, data):
	def _remove(polylines):
		for polyline, in polylines:
			polyline.remove()
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	assert(dimension > 1)
	x = range(dimension)
	polylines = [ax.plot(x, point) for point in data]
	return lambda: _remove(polylines)

def plot(ax, data):
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	if dimension == 0:
		pass
	elif dimension == 1:
		return plot1(ax, data)
	elif dimension == 2:
		return plot2(ax, data)
	elif dimension == 3:
		return plot3(ax, data)
	else:
		return plot_parallel_coordinates(ax, data)

def scatter2(ax, data, *args, **kwargs):
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	assert(dimension == 2)
	x, y = data.T
	points = ax.scatter(x, y, *args, **kwargs)
	return lambda: points.remove()

def scatter3(ax, data, *args, **kwargs):
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	assert(dimension == 3)
	x, y, z = data.T
	points = ax.scatter(x, y, z, *args, **kwargs)
	return lambda: points.remove()

def scatter(ax, data, *args, **kwargs):
	assert(len(data.shape) == 2)
	dimension = data.shape[1]
	if dimension == 0:
		pass
	elif dimension == 1:
		return plot1(ax, data)
	elif dimension == 2:
		return scatter2(ax, data, *args, **kwargs)
	elif dimension == 3:
		return scatter3(ax, data, *args, **kwargs)
	else:
		return plot_parallel_coordinates(ax, data)

def draw(properties, ax, dataDict, data):
	if 'fitness' in dataDict:
		fitness = dataDict['fitness']
		removers = [scatter(ax, data, c = fitness)]
	elif 'crowdingDistance' in dataDict:
		crowdingDistance = dataDict['crowdingDistance']
		maxCD = max(crowdingDistance)
		population = numpy.hstack([data, crowdingDistance.reshape(len(crowdingDistance), 1)])
		_population = numpy.array(list(filter(lambda individual: individual[-1] < maxCD, population)))
		extreme = numpy.array(list(filter(lambda individual: individual[-1] == maxCD, population)))
		removers = []
		if len(_population) > 0:
			removers.append(scatter(ax, _population[:, :-1], c = _population[:, -1]))
		if len(extreme) > 0:
			removers.append(scatter(ax, extreme[:, :-1], marker = 'x'))
	else:
		removers = [plot(ax, data)]
	relim(ax, data)
	return removers

def __init__(name, properties):
	if name == 'Objective Space':
		return lambda ax, dataDict: draw(properties, ax, dataDict, dataDict['pf'])
	elif name == 'Decision Space':
		return lambda ax, dataDict: draw(properties, ax, dataDict, dataDict['ps'])
	else:
		return lambda ax, dataDict: draw(properties, ax, dataDict, numpy.hstack([dataDict['ps'], dataDict['pf']]))