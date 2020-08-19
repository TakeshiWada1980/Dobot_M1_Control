import socket
import logging
import time
import json

class DobotCommandSender:

  def __init__(self,host='127.0.0.1',port=8889):
    self.host = host
    self.port = port
    self.timeout = 5
    self.buffer_size = 1024
    self.log = logging.getLogger('DobotCommandSender')

  def _send(self,cmd_dict):

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

  def arm_orientation(self,mode):
    '''
    ArmOrientation

    Parameters
    ----------
    mode : int
      設定値 0(Right) or 1(Left)
    '''
    return self._send(dict(command='ArmOrientation',mode=mode))

  def set_cordinate_speed(self,velocity,jerk):
    '''
    SetCordinateSpeed

    Parameters
    ----------
    velocity : int
      設定値
    jerk : int 
    　設定値
    '''
    return self._send(dict(command='SetCordinateSpeed',velocity=velocity,jerk=jerk))

  def set_jump_pram(self,height=20,zlimit=200):
    '''
    SetCordinateSpeed

    Parameters
    ----------
    height : int
      設定値
    zlimit : int 
    　設定値
    '''
    return self._send(dict(command='SetJumpPram',height=height,zlimit=zlimit))

  def set_output(self,pin,value):
    '''
    SetOutput(DigitalOutput)

    Parameters
    ----------
    pin : int
      ピン番号
    value : int
      出力設定値 0 or 1
    '''
    if not( 1 <= pin <= 6 ):
      return dict(is_sccess=False, msg='')
    if value not in (0,1) :
      return dict(is_sccess=False, msg='')
    return self._send(dict(command='SetOutput',pin=pin,value=value))

  def get_input(self,pin):
    '''
    GetInput(AnalogInput)

    Parameters
    ----------
    pin : int
      ピン番号
    '''
    if not( 1 <= pin <= 6 ):
      return dict(is_sccess=False, msg='')
    return self._send(dict(command='GetInput',pin=pin))

  def wait(self,ms):
    '''
    Wait

    Parameters
    ----------
    ms : int
      ウエイト時間（ミリ秒単位）
    '''
    return self._send(dict(command='Wait',ms=ms))

  def jump_to(self,x,y,z,r=0):
    '''
    JumpTo

    Parameters
    ----------
    x : int
      移動先のX座標
    y : int
      移動先のY座標
    z : int
      移動先のZ座標     
    r : int
      回転量（デフォルト値0）
    '''
    return self._send(dict(command='JumpTo',x=x,y=y,z=z,r=r))

  def go_to(self,x,y,z,r=0):
    '''
    GoTo

    Parameters
    ----------
    x : int
      移動先のX座標
    y : int
      移動先のY座標
    z : int
      移動先のZ座標     
    r : int
      回転量（デフォルト値0）
    '''
    return self._send(dict(command='GoTo',x=x,y=y,z=z,r=r))

  def quit(self):
    return self._send(dict(command='Quit'))

  def __repr__(self):
    return f'DobotCommandSender_{self.host}:{self.port}'

if __name__ == '__main__':

  logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
  logging.getLogger('DobotCommandSender').setLevel(logging.DEBUG)
  cs = DobotCommandSender('127.0.0.1')

  # 初期設定系
  cs.arm_orientation(mode=1)
  cs.set_cordinate_speed(velocity=20,jerk=50)
  cs.set_jump_pram(height=20,zlimit=200)
  
  # I/O系
  cs.set_output(pin=1,value=1)
  cs.get_input(pin=1)
  cs.wait(2000)

  # 移動系
  cs.jump_to(x=350,y=10,z=40)
  cs.jump_to(x=350,y=10,z=40,r=20)
  cs.go_to(x=350,y=10,z=40)

  cs.quit()
