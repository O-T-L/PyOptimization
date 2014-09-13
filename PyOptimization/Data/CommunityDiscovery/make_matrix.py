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
import numpy

def make_matrix(pathLink, pathMatrix, undigraph, delimiter = '\t'):
	links = numpy.loadtxt(pathLink, ndmin = 2)
	assert(links.shape[1] == 2)
	links -= numpy.min(links)
	count = numpy.max(links) + 1
	m = numpy.zeros([count, count], dtype = bool)
	for v1, v2 in links:
		m[v1, v2] = True
		if undigraph:
			m[v2, v1] = True
	for i in range(len(m)):
		m[i, i] = True
	numpy.savetxt(pathMatrix, m, fmt = '%i', delimiter = delimiter)

def main():
	if len(sys.argv) > 3:
		make_matrix(sys.argv[1], sys.argv[2], sys.argv[3] == 'y')
	else:
		print('Wrong number of arguments')

if __name__ == '__main__':
	main()