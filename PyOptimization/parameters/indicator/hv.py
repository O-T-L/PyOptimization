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

def reference_point(config, properties):
	if re.match('^ZDT\d$', properties['problem']):
		return [2, 2]
	elif properties['problem'] == 'DTLZ1':
		return [1] * properties['objectives']
	elif re.match('^DTLZ[23456]I?$', properties['problem']):
		return [2] * properties['objectives']
	elif properties['problem'] == 'DTLZ7':
		return {
			3:	[2] * 2 + [7],
			4:	[2] * 3 + [9],
			5:	[2] * 4 + [11],
			6:	[2] * 5 + [13],
			8:	[2] * 7 + [17],
			10:	[2] * 9 + [21],
		}[properties['objectives']]
	elif re.match('^WFG\d$', properties['problem']):
		return [1 + (i + 1) * 2 for i in range(properties['objectives'])]
	elif properties['problem'] == 'MOTSP':
		return [22] * properties['objectives']