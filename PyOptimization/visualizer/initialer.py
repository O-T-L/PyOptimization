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

import re
import math
import numpy
import mpl_toolkits.mplot3d
import matplotlib.patches
import pyotl.utility
import pyotl.problem.real

def flat(ax, dimension, distance, alpha = 0.2, color = 'white'):
	if dimension == 2:
		draw, = ax.plot([distance, 0], [0, distance])
		return lambda: draw.remove()
	elif dimension == 3:
		polygon = mpl_toolkits.mplot3d.art3d.Poly3DCollection([[(distance, 0, 0), (0, distance, 0), (0, 0, distance)]], facecolors = [color], alpha = alpha)
		draw = ax.add_collection3d(polygon)
		return lambda: draw.remove()

def sphere(ax, dimension, radius, resolution = 100, alpha = 0.2):
	if dimension == 2:
		u = numpy.linspace(0, numpy.pi / 2, resolution)
		x = radius * numpy.cos(u)
		y = radius * numpy.sin(u)
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		resolution = math.sqrt(resolution)
		u, v = numpy.mgrid[0 : numpy.pi / 2 : resolution * 1j, 0 : numpy.pi / 2 : resolution * 1j]
		x = radius * numpy.cos(u) * numpy.cos(v)
		y = radius * numpy.cos(u) * numpy.sin(v)
		z = radius * numpy.sin(u)
		draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
		return lambda: draw.remove()

def circle(ax, dimension, radius, resolution = 100):
	if dimension == 2:
		u = numpy.linspace(0, numpy.pi / 2, resolution)
		x = radius * numpy.cos(u)
		y = radius * numpy.sin(u)
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		v = numpy.linspace(0, numpy.pi / 2, resolution)
		z = radius * numpy.cos(v)
		r = radius * numpy.sin(v)
		alpha = math.pi / 4
		x = r * math.cos(alpha)
		y = r * math.sin(alpha)
		draw, = ax.plot(x, y, z)
		return lambda: draw.remove()

def xsinx(ax, resolution = 500):
	x = numpy.linspace(-1, 2, resolution)
	y = x * numpy.sin(10 * math.pi * x) + 2
	draw = ax.plot(x, y)
	return lambda: draw.remove()

def camel(ax, resolution = (50, 10), alpha = 0.2):
	x, y = numpy.mgrid[-100 : 100 : resolution[0] * 1j, -100 : 100 : resolution[1] * 1j]
	xSquare = x * x
	ySquare = y * y
	z = (4 - 2.1 * xSquare + xSquare * xSquare / 3) * xSquare + x * y + (-4 + 4 * ySquare) * ySquare
	draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
	return lambda: draw.remove()

def shaffer_f6(ax, resolution = 50, alpha = 0.2):
	xy = numpy.power(numpy.linspace(0, 1, resolution), 4) * 200 - 100
	x, y = numpy.meshgrid(xy, xy)
	xSquare = x * x
	ySquare = y * y
	z = 0.5 - (numpy.power(numpy.sin(numpy.sqrt(xSquare + ySquare)), 2) - 0.5) / pow(1 + 0.001 * (xSquare + ySquare), 2)
	draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
	return lambda: draw.remove()

def draw_cube_face(ax, points, **kwargs):
	p1, p2, p3, p4 = points
	x1, y1, z1 = p1
	x2, y2, z2 = p2
	x3, y3, z3 = p3
	x4, y4, z4 = p4
	x = [[x1, x2, x3, x4, x1],
		[x1, x1, x1, x1, x1]]
	y = [[y1, y2, y3, y4, y1],
		[y1, y1, y1, y1, y1]]
	z = [[z1, z2, z3, z4, z1],
		[z1, z1, z1, z1, z1]]
	ax.plot_surface(x, y, z, **kwargs)

def draw_cube(ax, p1, p2, p3, p4, p5, p6, p7, p8, **kwargs):
	draw_cube_face(ax, [p1, p2, p5, p3], **kwargs)
	draw_cube_face(ax, [p1, p3, p6, p4], **kwargs)
	draw_cube_face(ax, [p1, p2, p7, p4], **kwargs)
	draw_cube_face(ax, [p8, p6, p4, p7], **kwargs)
	draw_cube_face(ax, [p8, p5, p2, p7], **kwargs)
	draw_cube_face(ax, [p8, p5, p3, p6], **kwargs)

def rectangle(ax, dataDict, **kwargs):
	if 'boundary' in dataDict:
		boundary = dataDict['boundary']
		if len(boundary) == 2:
			x1, x2 = boundary[0]
			y1, y2 = boundary[1]
			ax.add_patch(matplotlib.patches.Rectangle((x1, y1), x2 - x1, y2 - y1, **kwargs))
		elif len(boundary) == 3:
			x1, x2 = boundary[0]
			y1, y2 = boundary[1]
			z1, z2 = boundary[2]
			draw_cube(ax,
				[x1, y1, z1],
				[x2, y1, z1],
				[x1, y2, z1],
				[x1, y1, z2],
				[x2, y2, z1],
				[x1, y2, z2],
				[x2, y1, z2],
				[x2, y2, z2],
				**kwargs)
			#_draw_cube(ax, x1, y1, z1, x2, y2, z2, **kwargs)

def rotated_rectangle(ax, dataDict, **kwargs):
	if 'boundary' in dataDict and 'direction' in dataDict:
		boundary = dataDict['boundary']
		direction = dataDict['direction']
		assert(len(direction) == len(boundary))
		_boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
		_direction = pyotl.utility.PyList2BlasVector_Real(direction.tolist())
		problem = pyotl.problem.real.RotatedRectangle(_boundary, _boundary, _direction)
		axes = numpy.array(pyotl.utility.BlasMatrix2PyListList_Real(problem.GetAxes())).T
		if len(boundary) == 2:
			x1, x2 = boundary[0]
			y1, y2 = boundary[1]
			ax.add_patch(matplotlib.patches.Polygon([axes.dot([x1, y1]), axes.dot([x2, y1]), axes.dot([x2, y2]), axes.dot([x1, y2])], **kwargs))
		elif len(boundary) == 3:
			x1, x2 = boundary[0]
			y1, y2 = boundary[1]
			z1, z2 = boundary[2]
			draw_cube(ax,
				axes.dot([x1, y1, z1]),
				axes.dot([x2, y1, z1]),
				axes.dot([x1, y2, z1]),
				axes.dot([x1, y1, z2]),
				axes.dot([x2, y2, z1]),
				axes.dot([x1, y2, z2]),
				axes.dot([x2, y1, z2]),
				axes.dot([x2, y2, z2]),
				**kwargs)

def zdt1(ax, resolution = 100):
	x = numpy.linspace(0, 1, resolution)
	y = 1 - numpy.sqrt(x)
	draw, = ax.plot(x, y)
	return lambda: draw.remove()

def zdt2(ax, resolution = 100):
	x = numpy.linspace(0, 1, resolution)
	y = 1 - x * x
	draw, = ax.plot(x, y)
	return lambda: draw.remove()

def zdt3(ax, resolution = 100):
	x = numpy.linspace(0, 1, resolution)
	y = 1 - numpy.sqrt(x) - x * numpy.sin(10 * numpy.pi * x)
	draw, = ax.plot(x, y)
	return lambda: draw.remove()

def zdt5(ax, resolution = 100):
	x = numpy.linspace(0, 1, resolution)
	y = 1 / x
	draw, = ax.plot(x, y)
	return lambda: draw.remove()

def uf5(ax, resolution = 100):
	x = numpy.linspace(0, 1, resolution)
	y = 1 - x
	draw, = ax.plot(x, y)
	return lambda: draw.remove()

def convex_dtlz2(ax, dimension, radius, resolution = 100, alpha = 0.2):
	if dimension == 2:
		u = numpy.linspace(0, numpy.pi / 2, resolution)
		x = numpy.power(radius * numpy.cos(u), 4)
		y = numpy.power(radius * numpy.sin(u), 2)
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		resolution = math.sqrt(resolution)
		u, v = numpy.mgrid[0 : numpy.pi / 2 : resolution * 1j, 0 : numpy.pi / 2 : resolution * 1j]
		x = numpy.power(radius * numpy.cos(u) * numpy.cos(v), 4)
		y = numpy.power(radius * numpy.cos(u) * numpy.sin(v), 4)
		z = numpy.power(radius * numpy.sin(u), 2)
		draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
		return lambda: draw.remove()

def scaled_dtlz2(ax, dimension, radius, resolution = 100, alpha = 0.2):
	if dimension == 2:
		u = numpy.linspace(0, numpy.pi / 2, resolution)
		x = radius * numpy.cos(u)
		y = 10 * radius * numpy.sin(u)
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		resolution = math.sqrt(resolution)
		u, v = numpy.mgrid[0 : numpy.pi / 2 : resolution * 1j, 0 : numpy.pi / 2 : resolution * 1j]
		x = radius * numpy.cos(u) * numpy.cos(v)
		y = 10 * radius * numpy.cos(u) * numpy.sin(v)
		z = 100 * radius * numpy.sin(u)
		draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
		return lambda: draw.remove()

def _dtlz7(posDecision):
	d = 2
	numberOfObjectives = len(posDecision) + 1
	return d * (numberOfObjectives - sum([(math.sin(3 * math.pi * Decision) + 1) * Decision / d for Decision in posDecision]))

def dtlz7(ax, dimension, resolution = 400, alpha = 0.7, cmap = 'jet'):
	if dimension == 2:
		x = numpy.linspace(0, 1, resolution)
		y = [_dtlz7([_x]) for _x in x]
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		resolution = math.sqrt(resolution)
		x, y = numpy.mgrid[0 : 1 : resolution * 1j, 0 : 1 : resolution * 1j]
		z = numpy.zeros(x.shape)
		z.flat = [_dtlz7([_x, _y]) for _x, _y in zip(x.flat, y.flat)]
		draw = ax.plot_surface(x, y, z, rstride = 1, cstride = 1, alpha = alpha, cmap = matplotlib.cm.get_cmap(cmap), linewidth = 0)
		return lambda: draw.remove()

def convex_concave(decision, nSegments, shape):
	assert(numpy.all(numpy.greater_equal(decision, 0)) and numpy.all(numpy.less_equal(decision, 1)))
	assert(nSegments > 0);
	assert(shape > 0);
	tmp = 2 * nSegments * math.pi;
	return numpy.power(1 - decision - numpy.cos(tmp * decision + numpy.pi / 2) / tmp, shape)

def wfg1(ax, dimension, resolution = 400, alpha = 0.2):
	nSegments = 5
	shape = 1
	if dimension == 2:
		u = numpy.linspace(0, 1, resolution)
		_u = u * numpy.pi / 2
		x = (1 - numpy.cos(_u)) * 2
		y = convex_concave(u, nSegments, shape) * 4
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		resolution = math.sqrt(resolution)
		u, v = numpy.mgrid[0 : 1 : resolution * 1j, 0 : 1 : resolution * 1j]
		_u = u * numpy.pi / 2
		_v = v * numpy.pi / 2
		x = (1 - numpy.cos(_u)) * (1 - numpy.cos(_v)) * 2
		y = (1 - numpy.cos(_u)) * (1 - numpy.sin(_v)) * 4
		z = convex_concave(u, nSegments, shape) * 6
		draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
		return lambda: draw.remove()

def disconnected(decision, nRegions, shape, location):
	assert(numpy.all(numpy.greater_equal(decision, 0)) and numpy.all(numpy.less_equal(decision, 1)))
	assert(nRegions > 0);
	assert(shape > 0);
	assert(location > 0);
	tmp = nRegions * numpy.power(decision, location) * math.pi;
	return 1 - numpy.power(decision, shape) * numpy.power(numpy.cos(tmp), 2)

def wfg2(ax, dimension, resolution = 2500, alpha = 0.2):
	nRegions = 5
	shape = 1
	location = 1
	if dimension == 2:
		u = numpy.linspace(0, 1, resolution)
		_u = u * numpy.pi / 2
		x = (1 - numpy.cos(_u)) * 2
		y = disconnected(u, nRegions, shape, location) * 4
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		resolution = math.sqrt(resolution)
		u, v = numpy.mgrid[0 : 1 : resolution * 1j, 0 : 1 : resolution * 1j]
		_u = u * numpy.pi / 2
		_v = v * numpy.pi / 2
		x = (1 - numpy.cos(_u)) * (1 - numpy.cos(_v)) * 2
		y = (1 - numpy.cos(_u)) * (1 - numpy.sin(_v)) * 4
		z = disconnected(u, nRegions, shape, location) * 6
		draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
		return lambda: draw.remove()

def wfg3(ax, dimension, alpha = 0.2, color = 'red'):
	if dimension == 2:
		draw, = ax.plot([2, 0], [0, 4])
		return lambda: draw.remove()
	elif dimension == 3:
		x, y, z = zip(*[[1, 2, 0], [0, 0, 6]])
		draw, = ax.plot(x, y, z)
		return lambda: draw.remove()

def wfg4(ax, dimension, resolution = 400, alpha = 0.2):
	if dimension == 2:
		u = numpy.linspace(0, numpy.pi / 2, resolution)
		x = numpy.sin(u) * 2
		y = numpy.cos(u) * 4
		draw, = ax.plot(x, y)
		return lambda: draw.remove()
	elif dimension == 3:
		resolution = math.sqrt(resolution)
		u, v = numpy.mgrid[0 : numpy.pi / 2 : resolution * 1j, 0 : numpy.pi / 2 : resolution * 1j]
		x = numpy.sin(u) * numpy.sin(v) * 2
		y = numpy.sin(u) * numpy.cos(v) * 4
		z = numpy.cos(u) * 6
		draw = ax.plot_surface(x, y, z, alpha = alpha, color = 'red', linewidth = 0)
		return lambda: draw.remove()

def __init__(name, properties):
	if name == 'Objective Space':
		if re.match('^ZDT[14]$|^UF[123]$', properties['problem']):
			return lambda ax, dataDictList: zdt1(ax)
		elif re.match('^ZDT[26]$|^UF[4]$', properties['problem']):
			return lambda ax, dataDictList: zdt2(ax)
		elif properties['problem'] == 'ZDT3':
			return lambda ax, dataDictList: zdt3(ax)
		elif properties['problem'] == 'ZDT5':
			return lambda ax, dataDictList: zdt5(ax)
		elif re.match('^UF[567]$|^CF1$', properties['problem']):
			return lambda ax, dataDictList: uf5(ax)
		elif properties['problem'] == 'DTLZ1':
			return lambda ax, dataDictList: flat(ax, dataDictList[0]['pf'].shape[1], 0.5)
		elif re.match('^DTLZ[2-4]$|^UF[89]$|^UF10$', properties['problem']):
			return lambda ax, dataDictList: sphere(ax, dataDictList[0]['pf'].shape[1], 1)
		elif re.match('^DTLZ[56]$', properties['problem']):
			return lambda ax, dataDictList: circle(ax, dataDictList[0]['pf'].shape[1], 1)
		elif properties['problem'] == 'DTLZ7':
			return lambda ax, dataDictList: dtlz7(ax, dataDictList[0]['pf'].shape[1])
		elif re.match('^ConvexDTLZ[2-4]$', properties['problem']):
			return lambda ax, dataDictList: convex_dtlz2(ax, dataDictList[0]['pf'].shape[1], 1)
		elif re.match('^ScaledDTLZ[2-4]$', properties['problem']):
			return lambda ax, dataDictList: scaled_dtlz2(ax, dataDictList[0]['pf'].shape[1], 1)
		elif properties['problem'] == 'WFG1':
			return lambda ax, dataDictList: wfg1(ax, dataDictList[0]['pf'].shape[1])
		elif properties['problem'] == 'WFG2':
			return lambda ax, dataDictList: wfg2(ax, dataDictList[0]['pf'].shape[1])
		elif properties['problem'] == 'WFG3':
			return lambda ax, dataDictList: wfg3(ax, dataDictList[0]['pf'].shape[1])
		elif re.match('^WFG[4-9]$', properties['problem']):
			return lambda ax, dataDictList: wfg4(ax, dataDictList[0]['pf'].shape[1])
		else:
			return None
	elif name == 'Decision Space':
		if properties['problem'] == 'Rectangle':
			return lambda ax, dataDictList: rectangle(ax, dataDictList[0], facecolor = 'grey', alpha = 0.1)
		elif properties['problem'] == 'RotatedRectangle':
			return lambda ax, dataDictList: rotated_rectangle(ax, dataDictList[0], facecolor = 'grey', alpha = 0.1)
		else:
			return None
	else:
		if properties['problem'] == 'XSinX':
			return lambda ax, dataDictList: xsinx(ax)
		elif properties['problem'] == 'Camel':
			return lambda ax, dataDictList: camel(ax)