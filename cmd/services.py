"""
-------------------------------------------------
   date：          2021/11/16
   Author :        aGrass
   File Name：     services.py
   Description :   定时任务启动
-------------------------------------------------
   Change Activity:
                   2021/11/16
-------------------------------------------------
"""
from ._sched import jobs
from ._typing import Service
from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerService(Service):
    def run(self):
        scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
        scheduler.start()
        for j in jobs():
            if self.switch.closed:
                break
            scheduler.add_job(j.func, j.trigger, **j.cfg, max_instances=3)
        self._wait_close(scheduler)

    def shutdown(self):
        pass

    def _wait_close(self, scheduler: BackgroundScheduler):
        while self.switch.on:
            self.rand_sleep()
        scheduler.shutdown()
