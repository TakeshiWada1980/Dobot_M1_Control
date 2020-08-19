import socket
import logging
import time
import json

Z_MAX_LIMIT = 250
Z_MIN_LIMIT = 10

class CommandSender:

  def __init__(self,host='127.0.0.1',port=8889):
    self.host = host
    self.port = port
    self.timeout = 5
    self.buffer_size = 1024
    self.log = logging.getLogger('DobotCommandSender')

    ret = self.ping()
    if not ret['is_sccess'] :
      self.log.error('例外を発生させて強制終了させます。')
      raise Exception

  def _send(self,cmd_dict):

    # 引数「cmd_dict」がdictオブジェクトであることを確認
    if not isinstance(cmd_dict,dict) :
      self.log.error('引数「cmd_dict」はdict型で与えてください。')
      self.log.error("  - 例：send(dict(command='QUIT'))")
      return dict(is_sccess=False, msg='TypeError(cmd_dict)')

    # 引数「cmd_dict」のキーに command が含まれていることを確認
    if 'command' not in cmd_dict :
      self.log.error('引数「cmd_dict（dict型）」のキーには「command」を含めてください。')
      self.log.error("  - 例：send(dict(command='QUIT'))")
      return dict(is_sccess=False, msg="InvalidArgError(Not found 'command' key in cmd_dict)")
      
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
          res = dict(is_sccess=False, msg='Timeout')
      return res
    except ConnectionRefusedError:
      self.log.error(f'{self.host}:{self.port} に接続できませんでした。')
      self.log.error('  - Dobot側プログラムが実行状態であることを確認してください。') 
      return dict(is_sccess=False, msg='ConnectionRefused')

  def arm_orientation(self,mode):
    '''
    ArmOrientation

    Parameters
    ----------
    mode : int
      設定値 0(Right) or 1(Left)
    '''
    if mode not in (0,1):
      msg = f'InvalidArgError : mode={mode} in arm_orientation(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg)
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

  def set_jump_pram(self,height,zlimit):
    '''
    SetCordinateSpeed

    Parameters
    ----------
    height : int
      設定値
    zlimit : int 
    　設定値
    '''
    if not( Z_MIN_LIMIT <= height <= Z_MAX_LIMIT ):
      msg = f'InvalidArgError : height={height} in set_jump_pram(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg) 
    if not( Z_MIN_LIMIT <= zlimit <= Z_MAX_LIMIT ):
      msg = f'InvalidArgError : zlimit={zlimit} in set_jump_pram(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg) 
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
      msg = f'InvalidArgError : pin={pin} in SetOutput(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg)
    if value not in (0,1) :
      msg = f'InvalidArgError : value={value} in SetOutput(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg)
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
      msg = f'InvalidArgError : pin={pin} in get_input(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg)
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
    if not( Z_MIN_LIMIT <= z <= Z_MAX_LIMIT ):
      msg = f'InvalidArgError : z={z} in jump_to(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg)    
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
    if not( Z_MIN_LIMIT <= z <= Z_MAX_LIMIT ):
      msg = f'InvalidArgError : z={z} in go_to(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg) 
    return self._send(dict(command='GoTo',x=x,y=y,z=z,r=r))

  def quit(self):
    return self._send(dict(command='Quit'))
  
  def ping(self):
    return self._send(dict(command='Ping'))

  def __repr__(self):
    return f'DobotCommandSender_{self.host}:{self.port}'
