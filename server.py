# Dobot Studio で実行するプログラム
# - Python 3.5 なので f文字列は使用できない

import socket
import logging
import time
import json

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

    if c['command'] == 'JUMP' :
      log.info('JUMP TO ({0},{1},{2})'.format(c['x'],c['y'],c['z']))
      # dType.SetPTPCmdEx(api,c['x'],c['y'],c['z'],1)
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