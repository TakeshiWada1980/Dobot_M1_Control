import socket
import logging
import time
import json

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(level=logging.INFO)

HOST = '127.0.0.1'
PORT = 8889
BUFFER_SIZE = 1024

def exe_command(c):

  if 'command' not in c :
    msg= 'KeyError : Not found "command" key.'
    log.error(msg)
    return '[ERR] ' + msg 

  try :
    if c['command'] == 'JUMP' :
      log.info('JUMP TO ({0},{1},{2})'.format(c['x'],c['y'],c['z']))
      # dType.SetPTPCmdEx(api,c['x'],c['y'],c['z'],1)
      res = '[OK]'
    elif c['command'] == 'QUIT' :
      log.info('QUIT')
      res = '[OK]'
    else :
      msg = 'Unknown commad : {0}'.format(str(c['command']))
      log.error(msg)
      res = '[ERR] ' + msg
  except KeyError:
    msg = 'ArgError in "{0}". ({1})'.format(c['command'],c.keys())
    log.error(msg)
    res = '[ERR] ' + msg

  return res

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('127.0.0.1', PORT))
  s.listen()
  while True:
    (connection, client) = s.accept()
    log.debug('Client connected {0}'.format(client))
    try:  
      command = json.loads(connection.recv(BUFFER_SIZE).decode('UTF-8'))
      res = exe_command(command)
      connection.send(res.encode())
    finally:
      connection.close()
      if command['command']=='QUIT' :
        break