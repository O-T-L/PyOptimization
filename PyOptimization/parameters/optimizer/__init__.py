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

def solutions(config, problem):
	return [100]
	if re.match('^(Convex)?DTLZ\dI?$', type(problem).__name__) and len(problem.GetBoundary()) == problem.GetNumberOfObjectives() - 1:
		return [1000]
	elif re.match('^WFG\d$', type(problem).__name__) and len(problem.GetBoundary()) == problem.GetPosDecisions():
		return [1000]
	return [100]

def step(config, optimizer, optimization):
	return True

def progress(config, optimizer, optimization):
	return optimization.iteration