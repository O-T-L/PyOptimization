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
import numpy


def basic(problem):
    return [
        ('problem', type(problem).__name__),
        ('objectives', problem.GetNumberOfObjectives()),
        ('evaluation', problem.GetNumberOfEvaluations()),
    ]


def std(problem):
    return basic(problem) + [
        ('decisions', len(problem.GetBoundary())),
    ]


def rectangle(problem):
    boundary = [[minmax.first, minmax.second] for minmax in problem.GetBoundaryOptimal()]
    f = io.BytesIO()
    numpy.savetxt(f, boundary)
    boundary = f.getvalue()
    return std(problem) + [('boundary', boundary)]


def rotated_rectangle(problem, direction):
    f = io.BytesIO()
    numpy.savetxt(f, direction)
    direction = f.getvalue()
    return rectangle(problem) + [('direction', direction)]


def tsp(problem, city):
    return basic(problem) + [('city', city), ('cities', problem.GetNumberOfCities())]


def motsp(problem, city):
    return tsp(problem, city)


def correlation_motsp(problem, city, correlation):
    return motsp(problem, city) + [('MOTSP correlate', correlation)]


def dtlz4(problem):
    return std(problem) + [('DTLZ4 bias', problem.GetBiasFactor())]


def dtlz_i(problem):
    return std(problem) + [('DTLZ_I', problem.GetManifold() + 1)]


def wfg(problem):
    return std(problem) + [('WFG PosDec', problem.GetPosDecisions())]
