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
import configparser
import sqlite3
import importlib
import uuid
import timeit
import pyotl.utility
import pyoptimization.optimizer.terminator


def output(config, items):
    table = config.get('database', 'table')
    columns, rowData = zip(*items)
    sql = 'INSERT INTO %s %s VALUES (%s)' % (table, str(columns), ', '.join(['?'] * len(rowData)))
    path = os.path.expandvars(config.get('database', 'file.' + platform.system()))
    conn = sqlite3.connect(path)
    conn.isolation_level = None  # Enable automatic commit
    cursor = conn.cursor()
    cursor.execute(sql, rowData)


class Optimization(pyotl.utility.Progress):
    def __call__(self, config, optimizer, fetcher):
        try:
            module, function = config.get('output', 'step').rsplit('.', 1)
            module = importlib.import_module(module)
            stepOutput = getattr(module, function)
        except configparser.NoOptionError:
            stepOutput = lambda config, optimizer, optimization: False
        try:
            module, function = config.get('optimization', 'progress').rsplit('.', 1)
            module = importlib.import_module(module)
            calculateProgress = getattr(module, function)
        except configparser.NoOptionError:
            calculateProgress = lambda config, optimizer, optimization: optimization.iteration
        stepInfo = eval(config.get('print', 'step'))
        self.uuid = str(uuid.uuid4())
        self.iteration = 0
        try:
            self.interval = optimizer.interval
        except:
            self.interval = None
        self.duration = 0
        print(eval(config.get('print', 'initial'))(optimizer, self))
        if stepOutput(config, optimizer, self):
            print(stepInfo(optimizer, self))
            output(config, [('uuid', self.uuid), ('iteration', self.iteration), ('interval', self.interval)] + fetcher(
                optimizer))
        self.progress_ = calculateProgress(config, optimizer, self)
        terminator = pyoptimization.optimizer.terminator.get_terminator(config, optimizer)
        while terminator(optimizer, self):
            timer = timeit.Timer(optimizer)
            self.interval = timer.timeit(1)
            self.duration += self.interval
            self.iteration += 1
            if stepOutput(config, optimizer, self):
                print(stepInfo(optimizer, self))
                output(config,
                       [('uuid', self.uuid), ('iteration', self.iteration), ('interval', self.interval)] + fetcher(
                           optimizer))
            self.progress_ = calculateProgress(config, optimizer, self)
        if config.getboolean('output', 'final'):
            print(eval(config.get('print', 'final'))(optimizer, self))
            output(config, [('uuid', self.uuid), ('iteration', self.iteration), ('duration', self.duration)] + fetcher(
                optimizer))
