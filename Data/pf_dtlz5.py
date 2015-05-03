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
import csv
import numpy
import pyotl.utility
import pyotl.problem.real
import pyotl.optimizer.real

def main():
	parameters = [map(int, row) for row in csv.reader(open(os.path.splitext(__file__)[0] + '.csv', 'r'), delimiter = '\t')]
	for nObjectives, nPoints in parameters:
		root = 'PF_%u' % nPoints
		if not os.path.exists(root):
			root = 'PF'
		path = os.path.join(root, 'DTLZ5', '%u.csv' % nObjectives)
		if os.path.exists(path):
			print('"%s" exists' % path)
		else:
			problem = pyotl.problem.real.DTLZ5(nObjectives, 0)
			pf = []
			for i in numpy.linspace(0, 1, nPoints):
				solution = pyotl.optimizer.real.Solution()
				assert(nObjectives > 1)
				solution.decision_ = pyotl.utility.PyList2Vector_Real([i] + [0.5] * (nObjectives - 2))
				problem(solution)
				objective = list(solution.objective_)
				assert(len(objective) == nObjectives)
				pf.append(objective)
			print(path)
			try:
				os.makedirs(os.path.dirname(path), exist_ok = True)
			except:
				pass
			numpy.savetxt(path, pf, delimiter = '\t')

if __name__ == '__main__':
	main()