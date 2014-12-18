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

def nbi_original(config, count, dimension):
	if dimension == 2:
		return pyotl.utility.NormalBoundaryIntersection_Real(dimension, count)
	if count == 100:
		if dimension == 3:
			return pyotl.utility.NormalBoundaryIntersection_Real(dimension, 12)
		elif dimension == 5:
			return pyotl.utility.NormalBoundaryIntersection_Real(dimension, 6)
		elif dimension == 8:
			return pyotl.optimizer.nsga_iii.NBI2_Real(dimension, 3, 2)
		elif dimension == 10:
			return pyotl.optimizer.nsga_iii.NBI2_Real(dimension, 3, 2)
		elif dimension == 15:
			return pyotl.optimizer.nsga_iii.NBI2_Real(dimension, 2, 1)
	raise

def nbi(config, count, dimension):
	if dimension == 2:
		return pyotl.utility.NormalBoundaryIntersection_Real(dimension, count)
	if count == 100:
		if dimension == 5:
			return pyotl.optimizer.nsga_iii.NBI2_Real(dimension, 4, 3)
		elif dimension == 10:
			return pyotl.optimizer.nsga_iii.NBI2_Real(dimension, 2, 1)
		elif dimension == 15:
			return pyotl.utility.NormalBoundaryIntersection_Real(dimension, 2)
	raise