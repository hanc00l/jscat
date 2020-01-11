#!/usr/bin/env python3
# coding:utf-8
from .payload import Payload


class Job():
    CREATED = 2
    RUNNING = 3
    FINISHED = 4

    def __init__(self):
        self.PAYLOAD = Payload()
        self.JOBS = []
        self.__job_id = 1

    '''
    添加一个任务
    '''

    def add_job(self, job_type, **kwargs):
        self.__job_id += 1
        script = self.PAYLOAD.get_payload(job_type, self.__job_id, kwargs)
        job = {'id': self.__job_id, 'type': job_type, 'script': script,
               'args': kwargs, 'callback': self.PAYLOAD.payload_callback, 'status': Job.CREATED}
        self.JOBS.append(job)

    '''
    获取一个任务的执行脚本
    '''

    def load_job(self):
        if len(self.JOBS) > 0:
            self.JOBS[0]['status'] = Job.RUNNING
            return self.JOBS[0]['script']
        else:
            return b''

    '''
    根据返回的任务数据，对任务进行处理
    '''

    def check_job(self, job_id, context):
        # 检查任务ID一致，并且任务处于执行状态才处理
        if len(self.JOBS) > 0 and self.JOBS[0]['id'] == job_id and self.JOBS[0]['status'] == Job.RUNNING:
            # 任务处理
            if self.JOBS[0]['callback']:
                self.JOBS[0]['callback'](
                    context, self.JOBS[0]['type'], self.JOBS[0]['args'])
            # 移除当前任务
            self.JOBS.pop(0)
            return True
        else:
            return False

    '''
    显示JOB列表
    '''

    def list_jobs(self):
        print('{:>10}\t{:<15}{:<10}'.format('JOBID', 'JOB_TYPE', 'STATUS'))
        for job in self.JOBS:
            status = 'RUNNING' if job['status'] == Job.RUNNING else 'CREATED'
            print('{:>10}\t{:<15}{:<10}'.format(job['id'], job['type'], status))
