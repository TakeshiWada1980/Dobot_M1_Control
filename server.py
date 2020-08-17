import socket
import logging
import time

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(level=logging.INFO)

HOST = '127.0.0.1'
PORT = 8889
BUFFER_SIZE = 1024

def exe_command(command):
  time.sleep(0.5) # コマンド実行のダミー
  res = 'OK'
  log.info('"{0}"->"{1}"'.format(command,res))
  return res

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('127.0.0.1', PORT))
  s.listen()
  while True:
    (connection, client) = s.accept()
    log.debug('Client connected {0}'.format(client))
    try:  
      # コマンド受信
      command = connection.recv(BUFFER_SIZE).decode('UTF-8')
      # レスポンス
      res = exe_command(command)
      connection.send(res.encode())
    finally:
      connection.close()
      if command=='QUIT' :
        break