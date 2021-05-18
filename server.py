# Dobot Studio で実行するプログラム
# - Python 3.5 なので f文字列は使用できない

import socket
import logging
import time
import json

# Dobot Studio で実行する場合は True に設定
DOBOT_STUDIO_ENV = False

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)

#HOST = '192.168.33.40'
HOST = '127.0.0.1'
PORT = 8893
BUFFER_SIZE = 1024

def exec_cmd(c):

  if 'command' not in c :
    msg= 'KeyError : Not found "command" key.'
    log.error(msg)
    return dict(status='Error',msg=msg)

  try :

    # 基本的には、ここのelif節の実装を拡張していく。

    #JumpTo命令 
    if c['command'] == 'JumpTo' :
      log.info('JumpTo ({0},{1},{2},{3})'.format(c['x'],c['y'],c['z'],c['r']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPCmdEx(api,0,c['x'],c['y'],c['z'],c['r'],1)
      res = dict(is_sccess=True)

    #JumpJointTo命令 
    elif c['command'] == 'JumpJointTo' :
      log.info('JumpJointTo ({0},{1},{2},{3})'.format(c['j1'],c['j2'],c['j3'],c['j4']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPCmdEx(api,3,c['j1'],c['j2'],c['j3'],c['j4'],1)
      res = dict(is_sccess=True)

    #GoTo命令 
    elif c['command'] == 'GoTo' :
      log.info('GoTo ({0},{1},{2},{3})'.format(c['x'],c['y'],c['z'],c['r']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPCmdEx(api,2,c['x'],c['y'],c['z'],c['r'],1)
      res = dict(is_sccess=True)

    #Wait命令 
    elif c['command'] == 'Wait' :
      log.info('Wait ({0} ms)'.format(c['ms']))
      if DOBOT_STUDIO_ENV :
        dType.SetWAITCmdEx(api,c['ms'],1)
      res = dict(is_sccess=True)

    #SetOutput命令 
    elif c['command'] == 'SetOutput' :
      log.info('SetOutput ({0} pin / Value {1})'.format(c['pin'],c['value']))
      if DOBOT_STUDIO_ENV :
        dType.SetIODOEx(api, c['pin'], c['value'], 1)
      res = dict(is_sccess=True)

    #Get(Analog)Input命令
    elif c['command'] == 'GetInput' :
      if DOBOT_STUDIO_ENV :
        result=dType.GetIODI(api,c[pin])[0]
      else :
        result=334 # Dummy値
      log.info('GetInput ({0} pin / Value {1})'.format(c['pin'],result))
      res = dict(status='OK',value=result)

    #ArmOrientation命令
    elif c['command'] == 'ArmOrientation' :
      log.info('ArmOrientation ({0} mode)'.format(c['mode']))
      if DOBOT_STUDIO_ENV :
        dType.SetArmOrientationEx(api,c['mode'], 1)
      res = dict(is_sccess=True)

    #SetCordinateSpeed命令 
    elif c['command'] == 'SetCordinateSpeed' :
      log.info('SetCordinateSpeed ({0} {1})'.format(c['velocity'],c['jerk']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPCommonParamsEx(api,c['velocity'],c['jerk'],1)
      res = dict(is_sccess=True)

    #SetJumpPram命令 
    elif c['command'] == 'SetJumpPram' :
      log.info('SetJumpPram (hieght = {0} zlimit = {1})'.format(c['height'],c['zlimit']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPJumpParamsEx(api,c['height'],c['zlimit'],1)
      res = dict(is_sccess=True)

    elif c['command'] == 'Ping' :
      log.info('Ping')
      res = dict(is_sccess=True)

    elif c['command'] == 'Quit' :
      log.info('Quit')
      res = dict(is_sccess=True)

    else :
      msg = 'Unknown commad : {0}'.format(str(c['command']))
      log.error(msg)
      res = dict(is_sccess=False,msg=msg)

  except KeyError:
    cmd_arg = [ s for s in c.keys() if s != 'command']
    msg = 'Invalid argument : "{0}" -> {{{1}}}'.format(c['command'],", ".join(cmd_arg))
    log.error(msg)
    res = dict(is_sccess=False,msg=msg)

  return res

#### MainLoop ###

try:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True :
      c, client = s.accept()
      log.debug('Client connected {0}'.format(client))
      try:  
        cmd_dict = json.loads(c.recv(BUFFER_SIZE).decode('UTF-8'))
        res = exec_cmd(cmd_dict)
        c.send(json.dumps(res,ensure_ascii=False).encode())
      finally:
        c.close()
        if 'command' in cmd_dict :
          if cmd_dict['command']=='Quit' :
            break
finally:
  s.close()