#!/usr/bin/env python3
# coding:utf-8
from .color import _BOLD, _RESET
import sys
import logging


class Log():
    '''
    日志类型
    '''
    CMD = 'CMD'
    JOB_RES = 'JOB_RESPONSE'
    SERVER = 'SERVER'
    logging.basicConfig(filename='log.txt', level=logging.INFO,
                        format='%(asctime)s %(message)s')

    '''
    记录一条日志信息
    '''
    @classmethod
    def log_message(cls, text, log_type, output=True, log=True):
        if output:
            cls.output_message(text)
        if log:
            if 'win32' not in sys.platform:
                text = text.replace(_BOLD, '').replace(_RESET, '')
            if log_type == Log.SERVER:
                text = text.strip()

            logging.info('[{}]{}'.format(log_type, text))

    '''
    输出消息
    '''
    @classmethod
    def output_message(cls, text):
        print(text)
