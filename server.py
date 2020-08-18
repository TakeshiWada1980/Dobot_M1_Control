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

HOST = '127.0.0.1'
PORT = 8889
BUFFER_SIZE = 1024

def exec_cmd(c):

  if 'command' not in c :
    msg= 'KeyError : Not found "command" key.'
    log.error(msg)
    return dict(status='Error',msg=msg)

  try :

    # 基本的には、ここのelif節の実装を拡張していく。

    #JUMP命令 
    if c['command'] == 'JUMP' :
      log.info('JUMP TO ({0},{1},{2},{3})'.format(c['x'],c['y'],c['z'],c['r']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPCmdEx(api,0,c['x'],c['y'],c['z'],c['r'],1)
      res = dict(status='OK')

    #WAIT命令 
    elif c['command'] == 'WAIT' :
      log.info('WAIT ({0} ms)'.format(c['ms']))
      if DOBOT_STUDIO_ENV :
        dType.SetWAITCmdEx(api,c['s'],1)
      res = dict(status='OK')

    #SETOUTPUT命令 
    elif c['command'] == 'SETOUTPUT' :
      log.info('SET ({0} pin / Value {1})'.format(c['pin'],c['value']))
      if DOBOT_STUDIO_ENV :
        dType.SetIODOEx(api, c['pin'], c['value'], 1)
      res = dict(status='OK')

    #GETINPUT命令 
    elif c['command'] == 'GETINPUT' :
      if DOBOT_STUDIO_ENV :
        result=dType.GetIODI(api,c[pin])[0]
      else :
        result=334 # Dummy値
      log.info('GET ({0} pin / Value {1})'.format(c['pin'],result))
      res = dict(status='OK',ret=result)

    #ARMORIENTATION命令
    elif c['command'] == 'ARMORIENTATION' :
      log.info('ARMORIENTATION ({0} mode)'.format(c['mode']))
      if DOBOT_STUDIO_ENV :
        dType.SetArmOrientationEx(api,c['mode'], 1)
      res = dict(status='OK')

    #SETCORDINATESPEED命令 
    elif c['command'] == 'SETCORDINATESPEED' :
      log.info('SETCORDINATESPEED ({0} {1})'.format(c['velocity'],c['jerk']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPCommonParamsEx(api,c['velocity'],c['jerk'],1)
      res = dict(status='OK')

    #SETJUMPPARAM命令 
    elif c['command'] == 'SETJUMPPARAM' :
      log.info('SETJUMPPARAM (hieght = {0} zlimit = {1})'.format(c['height'],c['zlimit']))
      if DOBOT_STUDIO_ENV :
        dType.SetPTPJumpParamsEx(api,c['height'],c['zlimit'],1)
      res = dict(status='OK')

    elif c['command'] == 'QUIT' :
      log.info('QUIT')
      res = dict(status='OK')

    else :
      msg = 'Unknown commad : {0}'.format(str(c['command']))
      log.error(msg)
      res = dict(status='Error',msg=msg)

  except KeyError:
    cmd_arg = [ s for s in c.keys() if s != 'command']
    msg = 'Invalid argument : "{0}" -> {{{1}}}'.format(c['command'],", ".join(cmd_arg))
    log.error(msg)
    res = dict(status='Error',msg=msg)

  return res

#### MainLoop ###

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
        if cmd_dict['command']=='QUIT' :
          break