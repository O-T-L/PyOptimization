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

import mpl_toolkits.mplot3d


def create_axes(fig, dimension):
    if dimension == 0:
        pass
    elif dimension == 3:
        return mpl_toolkits.mplot3d.Axes3D(fig)
    else:
        return fig.gca()


def set_label(ax, dimension, sign):
    if dimension == 2:
        ax.set_xlabel(r'$%s_{1}$' % sign)
        ax.set_ylabel(r'$%s_{2}$' % sign)
    elif dimension == 3:
        ax.set_xlabel(r'$%s_{1}$' % sign)
        ax.set_ylabel(r'$%s_{2}$' % sign)
        ax.set_zlabel(r'$%s_{3}$' % sign)
    elif dimension > 3:
        ax.set_xticklabels([])
        ax.set_xticks(range(dimension))
        ax.set_xticklabels([r'$%s_{%u}$' % (sign, axisIndex) for axisIndex in range(1, dimension + 1)])


def sop1(fig, dataDictList):
    ax = fig.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('f')
    return ax


def sop2(fig, dataDictList):
    ax = mpl_toolkits.mplot3d.Axes3D(fig)
    ax.set_xlabel(r'$x_1$')
    ax.set_ylabel(r'$x_2$')
    ax.set_zlabel('f')
    return ax


def mop_objective(fig, dataDictList):
    dataDict = dataDictList[0]
    if 'pf' in dataDict:
        dimension = dataDict['pf'].shape[1]
        ax = create_axes(fig, dimension)
        set_label(ax, dimension, 'f')
        return ax


def mop_decision(fig, dataDictList):
    dataDict = dataDictList[0]
    if 'ps' in dataDict:
        dimension = dataDict['ps'].shape[1]
        ax = create_axes(fig, dimension)
        set_label(ax, dimension, 'x')
        return ax


def __init__(properties):
    if properties['problem'] in ['XSinX']:
        return [(properties['problem'], sop1)]
    elif properties['problem'] in ['Camel']:
        return [(properties['problem'], sop2)]
    else:
        return [('Objective Space', mop_objective), ('Decision Space', mop_decision)]
