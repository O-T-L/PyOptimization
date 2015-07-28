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

import sys
import functools
import multiprocessing
from . import producer_consumer


class ProcessPool:
    def __init__(self, capacity, onError):
        if capacity is None or capacity <= 0:
            capacity = multiprocessing.cpu_count()
        self.__producer_consumer = producer_consumer.ProducerConsumer(capacity)
        self.__pool = multiprocessing.Pool(capacity)
        self.__onError = onError
        self.__capacity = capacity

    def __call__(self, fn, *args, **kwargs):
        self.__producer_consumer.producer()
        self.__pool.apply_async(fn, args, kwargs, self.__done, self.__error)

    def capacity(self):
        return self.__capacity

    def join(self):
        self.__pool.close()
        self.__pool.join()

    def __done(self, result):
        self.__producer_consumer.consumer()

    def __error(self, exception):
        self.__onError(exception)
        self.__producer_consumer.consumer()


def executer(fn, *args, **kwargs):
    return fn(*args, **kwargs)


def make_serial_executer():
    return executer


def error_logger(exception):
    sys.stderr.write('%s\n' % str(exception))


def make_parallel_executer(parallel, onError=error_logger):
    return ProcessPool(parallel, onError)


def make_mpi_executer():
    import pyoptimization.mpi
    caller = pyoptimization.mpi.MPICaller()
    executer = lambda fn, *args, **kwargs: caller(functools.partial(fn, *args, **kwargs))
    return executer, caller


def make_executer(config):
    if config.get('common', 'executer') == 'mpi':
        executer, caller = make_mpi_executer()
        print('MPI process %u of %u' % (caller.rank + 1, caller.size))
    elif config.get('common', 'executer') == 'parallel':
        parallel = config.getint('parallel', 'parallel')
        executer = make_parallel_executer(parallel)
        print('%u parallel' % executer.capacity())
    else:
        executer = make_serial_executer()
    return executer
