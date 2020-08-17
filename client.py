import socket
import logging
import time
import json

import math

class DobotCommandSender:

  def __init__(self,host='127.0.0.1',port=8889):
    self.host = host
    self.port = port
    self.timeout = 5
    self.buffer_size = 1024
    self.log = logging.getLogger('DobotCommandSender')

  def send(self,cmd_dict):

    # 引数「cmd_dict」がdictオブジェクトであることを確認
    if not isinstance(cmd_dict,dict) :
      self.log.error('引数「cmd_dict」はdict型で与えてください。')
      self.log.error("  - 例：send(dict(command='QUIT'))")
      return dict(status='Error')

    # 引数「cmd_dict」のキーに command が含まれていることを確認
    if 'command' not in cmd_dict :
      self.log.error('引数「cmd_dict（dict型）」のキーには「command」を含めてください。')
      self.log.error("  - 例：send(dict(command='QUIT'))")
      return dict(status='Error')
      
    try :
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try :
          s.connect((self.host, self.port))
          s.settimeout(self.timeout)
          s.send(json.dumps(cmd_dict,ensure_ascii=False).encode())
          self.log.info(f'SEND >> {cmd_dict}')
          res = json.loads(s.recv(self.buffer_size).decode('UTF-8'))
          self.log.info(f' RES >> {res}')
        except socket.timeout:
          self.log.error(f'送信後、{self.timeout}秒以内にレスポンスがありませんでした。')
          return dict(status='Error')
      return res
    except ConnectionRefusedError:
      self.log.error(f'{self.host}:{self.port} に接続できませんでした。')
      self.log.error('  - Dobot側プログラムが実行状態であることを確認してください。') 
      return dict(status='Error')

  def __repr__(self):
    return f'DobotCommandSender_{self.host}:{self.port}'


if __name__ == '__main__':

  logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
  logging.getLogger('DobotCommandSender').setLevel(logging.DEBUG)
  cs = DobotCommandSender('127.0.0.1')

  cs.send(True)
  cs.send(dict(x=10))

  cs.send(dict(command='JUMP',x=350,y=10,z=40))
  cs.send(dict(command='JUMP',x=400,y=20,z=40))
  cs.send(dict(command='JAMP',x=400,y=20,z=40)) # 誤コマンド
  cs.send(dict(command='JUMP',x=400,     z=40)) # 引数不足

  cs.send(dict(command='QUIT'))
