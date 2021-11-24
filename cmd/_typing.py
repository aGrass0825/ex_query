"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     _typing.py
   Description :   服务初始化
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
import os
import abc
import signal
import logging
import functools
import traceback
from multiprocessing import Event, Process
from typing import Sequence, Any, Type, NamedTuple, Callable

from ._tool import _println, _rand_sleep

__author__ = 'Memory_Leak<yuz@cnns.net>'


class Switch(object):
    def __init__(self):
        self._event = Event()

    @property
    def on(self):
        return not self._event.is_set()

    @property
    def closed(self):
        return self._event.is_set()

    def shutdown(self):
        self._event.set()


class Service(metaclass=abc.ABCMeta):
    def __init__(self, switch: Switch):
        self._switch = switch

    def println(self, message: str, *args: Any):
        if args:
            message = message.format(*args)
        _println("{}:{}", self.__class__.__name__, message)

    @staticmethod
    def rand_sleep():
        _rand_sleep()

    @property
    def switch(self):
        return self._switch

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass

    def __call__(self):
        self.start()

    def start(self):
        self.println("service {} started (pid={})", self.__class__.__name__, os.getpid())
        try:
            self.run()
        except KeyboardInterrupt as e:
            self.println("stopped with exception {}", e.__class__.__name__)
        except Exception as e:
            self.println("stopped with exception {}", e.__class__.__name__)
            traceback.print_tb(e.__traceback__)

    def wait_close(self):
        while self._switch.on:
            _rand_sleep()
        self.println("close event set, exit ... ")
        try:
            self.shutdown()
            self.println("over ...")
        except Exception as e:
            self.println("shutdown exception {}", e.__class__.__name__)
            traceback.print_tb(e.__traceback__)


class _ProcessServicePair(NamedTuple):
    service: Service
    process: Process

    @classmethod
    def new(cls, s: Type[Service], wrap: Callable[[Service], Any]) -> '_ProcessServicePair':
        service = s(Switch())
        process = Process(target=service) if not wrap else Process(target=wrap, args=(service,))
        process.start()
        return cls(service=service, process=process)


class Runner(object):
    def __init__(self, service_cls: Sequence[Type[Service]], log: dict = None):
        self._service_cls = service_cls
        self._log = log
        self.event = Event()

    def _wrapped(self, service: Service):
        if self._log:
            logging.basicConfig(**self._log)
        service.start()

    def _handle_sign(self, pairs: Sequence[_ProcessServicePair], sign, frame):
        _println("receive signal {} {}", sign, frame)
        if not self.event.is_set():
            self.event.set()
        for pair in pairs:
            _println("set service {} exit event ", pair.service.__class__.__name__)
            pair.service.switch.shutdown()

    def _waite_all(self, pairs: Sequence[_ProcessServicePair]):
        while not self.event.is_set():
            _rand_sleep()
        _println("exit event was set ,exit ...")
        for pair in pairs:
            if not pair.process.is_alive():
                _println("process {} already exit.", pair.process.pid)
                continue
            _println("wait process {}({}) exit", pair.service.__class__.__name__, pair.process.pid)
            pair.process.join()
            _println("process {}({}) exit", pair.service.__class__.__name__, pair.process.pid)

    def serve(self):
        _println("serve pid = {}", os.getpid())
        ps = tuple(map(lambda c: _ProcessServicePair.new(c, self._wrapped), self._service_cls))
        hs = functools.partial(self._handle_sign, ps)
        signal.signal(signal.SIGINT, hs)
        signal.signal(signal.SIGTERM, hs)
        self._waite_all(ps)
