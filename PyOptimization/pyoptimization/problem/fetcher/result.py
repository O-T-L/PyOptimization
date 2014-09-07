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

import io
import copy
import numpy

def basic(config, optimizer):
	items = []
	if config.getboolean('output', 'pf'):
		solutionSet = optimizer.GetSolutionSet()
		pf = list(map(lambda solution: copy.copy(solution.objective_), solutionSet))
		problem = optimizer.GetProblem()
		for objective in pf:
			problem.Fix(objective)
		f = io.BytesIO()
		numpy.savetxt(f, pf, delimiter = '\t')
		items.append(('pf', f.getvalue()))
	if config.getboolean('output', 'inequality'):
		solutionSet = optimizer.GetSolutionSet()
		inequality = list(map(lambda solution: solution.inequality_, solutionSet))
		f = io.BytesIO()
		numpy.savetxt(f, inequality, delimiter = '\t')
		items.append(('inequality', f.getvalue()))
	if config.getboolean('output', 'equality'):
		solutionSet = optimizer.GetSolutionSet()
		equality = list(map(lambda solution: solution.equality_, solutionSet))
		f = io.BytesIO()
		numpy.savetxt(f, equality, delimiter = '\t')
		items.append(('equality', f.getvalue()))
	return items

def std(config, optimizer):
	items = basic(config, optimizer)
	if config.getboolean('output', 'ps'):
		solutionSet = optimizer.GetSolutionSet()
		ps = list(map(lambda solution: solution.decision_, solutionSet))
		f = io.BytesIO()
		numpy.savetxt(f, ps, delimiter = '\t')
		items.append(('ps', f.getvalue()))
	return items

def dynamic_bitset(config, optimizer):
	items = basic(config, optimizer)
	return items