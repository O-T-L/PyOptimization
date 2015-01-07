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

import pyotl.initial.real
import pyotl.initial.integer
import pyotl.initial.dynamic_bitset
import pyotl.initial.index
import pyoptimization.problem.coding

def get_initial(config, problem, random, solutions):
	fetcher = lambda optimizer: [('solutions', solutions)]
	coding = pyoptimization.problem.coding.get_coding(problem)
	if coding == 'real':
		return pyotl.initial.real.PopulationUniform(random, problem.GetBoundary(), solutions), fetcher
	elif coding == 'integer':
		return pyotl.initial.integer.PopulationUniform(random, problem.GetBoundary(), solutions), fetcher
	elif coding == 'dynamic_bitset':
		return pyotl.initial.dynamic_bitset.PopulationUniform(random, problem.GetNumberOfBits(), solutions), fetcher
	elif coding == 'index':
		if type(problem).__name__.endswith('TSP'):
			return pyotl.initial.index.PopulationShuffle(random, problem.GetNumberOfCities(), solutions), fetcher
		else:
			return pyotl.initial.index.PopulationUniform(random, problem.GetBoundary(), solutions), fetcher
	else:
		raise