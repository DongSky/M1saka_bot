#encoding:utf-8
#利用command模块执行部分允许的shell
import commands
def commandline(username,command):
    if username=='DongSky':
            if command.startswith('rm'or'reboot'or'poweroff')==False:
                a,b=commands.getstatusoutput(command)
                return b
            else:
                return 'permission denied.'
    else:
        return 'permission denied.'
