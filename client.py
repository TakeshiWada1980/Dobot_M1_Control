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
TIMEOUT = 5

# dict型のオブジェクトを受け取ってJSONに変換して
# DobotStudio側の PG にソケット通信により送る送信
def send_command(command):
  try :
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      try :
        s.connect((HOST, PORT))
        s.settimeout(TIMEOUT)
        s.send(json.dumps(command,ensure_ascii=False).encode())
        log.info('"{0}"...'.format(command))
        res = s.recv(BUFFER_SIZE).decode('UTF-8')
      except socket.timeout:
        log.error(f'タイムアウトしました。コマンド送信後、{TIMEOUT}経過してもレスポンスがありませんでした。')
        return '[ERR] Timeout.'
    log.info('   -> "{0}"'.format(res))
  except ConnectionRefusedError:
    log.error(f'{HOST}:{PORT} に接続できませんでした。Dobot側のプログラムが実行状態になっているか確認してください。') 
    res = '[ERR] ConnectionRefused.'
  return res

j1 = dict(command='JUMP',x=400,y=0,z=50)
j2 = dict(command='JUMP',x=350,y=0,z=50)
j3 = dict(command='JAMP',x=350,y=0,z=50) # 誤ったコマンド
j4 = dict(command='JUMP',x=350,y=0) # 誤ったコマンド

q = dict(command='QUIT')

send_command(j1)
time.sleep(2)
send_command(j2)
time.sleep(2)
send_command(j3)
send_command(j4)

time.sleep(2)
send_command(q)