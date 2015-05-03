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

import pyotl.utility
import pyotl.optimizer.nsga_iii

def nbi(config, count, dimension):
	if dimension == 2:
		return [
			pyotl.utility.NormalBoundaryIntersection_Real(dimension, count),
		]
	if count == 100:
		if dimension == 3:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 13), # 105
			]
		elif dimension == 4:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 7), # 120
			]
		elif dimension == 5:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 5), # 126
			]
		elif dimension == 6:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 4), # 126
			]
		elif dimension == 8:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 3), # 120
			]
		elif dimension == 10:
			return [
				pyotl.optimizer.nsga_iii.NBI2_Real(dimension, 2, 2), # 55 + 55 = 110
			]
		elif dimension == 10:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 2), # 55
			]
		elif dimension == 10:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 3), # 220
			]
		elif dimension == 15:
			return [
				pyotl.utility.NormalBoundaryIntersection_Real(dimension, 2), # 120
			]
	raise Exception(count, dimension)