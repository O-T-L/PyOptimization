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
import fnmatch
import numpy

def main():
	for line in open(os.path.splitext(__file__)[0] + '.list', 'r').readlines():
		root = line.strip()
		for parent, _, filenames in os.walk(os.path.join(root, 'DTLZ2')):
			for filename in filenames:
				path = os.path.join(parent, filename)
				if not os.path.isdir(path) and fnmatch.fnmatch(filename, '*.csv'):
					print('Converting "%s"' % path)
					pf = numpy.loadtxt(path)
					for i, column in enumerate(pf.T):
						column *= (i + 1) * 2
					path = os.path.join(os.path.join(root, 'WFG4'), filename)
					print('Saving "%s"' % path)
					numpy.savetxt(path, pf, delimiter = '\t')

if __name__ == '__main__':
	main()