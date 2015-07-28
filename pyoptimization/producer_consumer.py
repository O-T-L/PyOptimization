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

import threading


class Producer:
    def __init__(self, lock, full, empty):
        self.__lock = lock
        self.__full = full
        self.__empty = empty

        self.__empty.acquire()
        self.__lock.acquire()

    def __del__(self):
        self.__lock.release()
        self.__full.release()


class Consumer:
    def __init__(self, lock, full, empty):
        self.__lock = lock
        self.__full = full
        self.__empty = empty

        self.__full.acquire()
        self.__lock.acquire()

    def __del__(self):
        self.__lock.release()
        self.__empty.release()


class ProducerConsumer:
    def __init__(self, capacity, count=0):
        assert (capacity > 0)
        assert (count <= capacity)
        self.__lock = threading.Lock()
        self.__full = threading.Semaphore(count)
        self.__empty = threading.Semaphore(capacity - count)

    def producer(self):
        return Producer(self.__lock, self.__full, self.__empty)

    def consumer(self):
        return Consumer(self.__lock, self.__full, self.__empty)
