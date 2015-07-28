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
import platform
import csv
import importlib
import numpy
import fnmatch
import matplotlib.pyplot
import mpl_toolkits.mplot3d
import configparser


def draw_distribution2(config, ax, population):
    ax.plot(population.T[0], population.T[1], 'o')
    ax.set_xlabel(r"$f_{1}$")
    ax.set_ylabel(r"$f_{2}$")


def draw_distribution3(config, ax, population):
    ax.view_init(azim=config.getfloat('3d', 'azimuth'), elev=config.getfloat('3d', 'elevation'))
    ax.plot(population.T[0], population.T[1], population.T[2], 'o')
    ax.set_xlabel(r"$f_{1}$")
    ax.set_ylabel(r"$f_{2}$")
    ax.set_zlabel(r"$f_{3}$")


def plot_data(config, ax, data):
    dimension = len(data[0])
    x = list(range(dimension))
    for point in data:
        ax.plot(x, point)


def draw_parallel_coordinates(config, ax, data):
    dimension = len(data[0])
    plot_data(config, ax, data)
    ax.set_xticklabels([])
    ax.set_xticks(list(range(dimension)))
    ax.set_xticklabels([r'$f_{%u}$' % axis for axis in range(1, dimension + 1)])


def draw(config, initialer, population, title):
    fig = matplotlib.pyplot.figure(title)
    if len(population[0]) == 2:
        ax = fig.gca()
        initialer(ax)
        draw_distribution2(config, ax, population)
    elif len(population[0]) == 3:
        ax = mpl_toolkits.mplot3d.Axes3D(fig)
        initialer(ax)
        draw_distribution3(config, ax, population)
    else:
        ax = fig.gca()
        initialer(ax)
        draw_parallel_coordinates(config, ax, population)
    try:
        lower, upper = map(int, config.get('limits', 'x').split())
        ax.set_xlim(lower, upper)
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass
    try:
        lower, upper = map(int, config.get('limits', 'y').split())
        ax.set_ylim(lower, upper)
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass
    try:
        lower, upper = map(int, config.get('limits', 'z').split())
        ax.set_zlim(lower, upper)
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass
    return fig


def get_properties_settings(path, delimiter='\t'):
    f = open(path, 'r')
    reader = csv.reader(f, delimiter=delimiter)
    propertiesSettings = []
    for column, converter in reader:
        converter = eval(converter)
        propertiesSettings.append((column, converter))
    return propertiesSettings


def full_split_path(path):
    components = []
    while True:
        path, folder = os.path.split(path)
        if folder:
            components.append(folder)
        else:
            if path:
                components.append(path)
            break
    components.reverse()
    return components


def get_properties(components, propertiesSettings):
    properties = []
    for column, converter in propertiesSettings:
        properties.append((column, converter(components)))
    return properties


def main():
    config = configparser.ConfigParser()
    config.read(os.path.splitext(__file__)[0] + '.ini')

    matplotlib.rcParams['font.size'] *= config.getfloat('scale', 'fontsize')
    dataFolder = os.path.expandvars(config.get('config', 'data_folder.' + platform.system()))
    figureFolder = os.path.expandvars(config.get('config', 'figure_folder.' + platform.system()))
    pattern = config.get('config', 'data_pattern')
    figureExt = config.get('config', 'figure_ext')
    propertiesSettings = get_properties_settings(os.path.expandvars(config.get('config', 'properties_settings')))
    module, function = config.get('visualizer', 'initialer').rsplit('.', 1)
    module = importlib.import_module(module)
    function = getattr(module, function)
    getInitialer = lambda properties: function(properties)
    for parent, _, filenames in os.walk(dataFolder, followlinks=True):
        for filename in filenames:
            if fnmatch.fnmatch(filename, pattern):
                path = os.path.join(parent, filename)
                pathFigure = os.path.join(figureFolder,
                                          os.path.splitext(os.path.relpath(path, dataFolder))[0]) + figureExt
                print(path + ' -> ' + pathFigure)
                pathRelative = os.path.relpath(path, dataFolder)
                components = full_split_path(pathRelative)
                properties = get_properties(components, propertiesSettings)
                properties = dict(properties)
                initialer = lambda ax: getInitialer(properties)(ax, [properties])
                population = numpy.loadtxt(path, ndmin=2)
                fig = draw(config, initialer, population, path)
                try:
                    os.makedirs(os.path.dirname(pathFigure))
                except OSError:
                    pass
                fig.savefig(pathFigure)
                matplotlib.pyplot.close(fig)


if __name__ == '__main__':
    main()
