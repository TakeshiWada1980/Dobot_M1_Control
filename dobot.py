import socket
import logging
import time
import json

class CommandSender:

  def __init__(self,host:str='127.0.0.1', port:int=8889):
    '''
    CommandSender Constructor

    Parameters
    ----------
    host : str
      接続先IPアドレス（例 : '127.0.0.1'）
    port : int
      接続先ポート（デフォルト値 : 0）
    '''

    self.__Z_MAX_LIMIT = 185
    self.__Z_MIN_LIMIT = 60

    self.host = host
    self.port = port
    self.timeout = 8
    self.buffer_size = 1024
    self.log = logging.getLogger('DobotCommandSender')

    ret = self.ping()
    if not ret['is_sccess'] :
      self.log.error('例外を発生させて強制終了させます。')
      raise Exception

  @property
  def Z_MAX_LIMIT(self):
    return self.__Z_MAX_LIMIT

  @property
  def Z_MIN_LIMIT(self):
    return self.__Z_MIN_LIMIT

  def _send(self, cmd_dict):

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
          raw = s.recv(self.buffer_size).decode('UTF-8')
          res = json.loads(raw)
          self.log.info(f' RES >> {res}')
        except json.JSONDecodeError as e:       
          self.log.error('Dobot側でエラーが発生した可能性があるため強制終了させます。')
          self.log.error('最後に送信したコマンドの1つ前に原因がある可能性が高いです。')
          raise Exception
        except socket.timeout:
          self.log.error(f'送信後、{self.timeout}秒以内にレスポンスがありませんでした。')
          res = dict(is_sccess=False, msg='Timeout')
      return res
    except ConnectionRefusedError:
      self.log.error(f'{self.host}:{self.port} に接続できませんでした。')
      self.log.error('  - Dobot側プログラムが実行状態であることを確認してください。') 
      return dict(is_sccess=False, msg='ConnectionRefused')

  def arm_orientation(self, mode:int):
    '''
    ArmOrientation

    Parameters
    ----------
    mode : int
      設定値 0(Left) or 1(Right)
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

  def set_jump_pram(self, height:int, zlimit:int):
    '''
    SetCordinateSpeed

    Parameters
    ----------
    height : int
      設定値
    zlimit : int 
    　設定値
    '''
    if not( self.Z_MIN_LIMIT <= height <= self.Z_MAX_LIMIT ):
      msg = f'InvalidArgError : height={height} in set_jump_pram(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg) 
    if not( self.Z_MIN_LIMIT <= zlimit <= self.Z_MAX_LIMIT ):
      msg = f'InvalidArgError : zlimit={zlimit} in set_jump_pram(...)'
      self.log.error(msg)
      return dict(is_sccess=False, msg=msg) 
    return self._send(dict(command='SetJumpPram',height=height,zlimit=zlimit))

  def set_output(self, pin:int, value:int):
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

  def get_input(self, pin:int):
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

  def wait(self, ms:int):
    '''
    Wait

    Parameters
    ----------
    ms : int
      ウエイト時間（ミリ秒単位）
    '''
    return self._send(dict(command='Wait',ms=ms))

  def jump_to(self, x:int, y:int, z:int, r:int=0):
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
      回転量（デフォルト値:0）
    '''
    for t in ((x,'x'),(y,'y'),(z,'z'),(r,'r')):
      if not isinstance(t[0],int) :
        msg = f'CommandSender.jump_to(...) の 引数 {t[1]} は int型 で与えてください。'
        raise TypeError(msg)
    if not( self.Z_MIN_LIMIT <= z <= self.Z_MAX_LIMIT ):
      msg = f'CommandSender.jump_to(...) の 引数 z は {self.Z_MIN_LIMIT} 以上 {self.Z_MAX_LIMIT} 以下で与えてください。'
      raise ValueError(msg)
    return self._send(dict(command='JumpTo',x=x,y=y,z=z,r=r))

  def jump_joint_to(self, j1:int, j2:int, j3:int, j4:int=0):
    '''
    JumpTo

    Parameters
    ----------
    j1 : int
      移動先のJ1角度
    j2 : int
      移動先のJ2角度
    j3 : int
      移動先のZ座標     
    j4 : int
      回転量（デフォルト値:0）
    '''
    for t in ((j1,'j1'),(j2,'j2'),(j3,'j3'),(j4,'j4')):
      if not isinstance(t[0],int) :
        msg = f'CommandSender.jump_joint_to(...) の 引数 {t[1]} は int型 で与えてください。'
        raise TypeError(msg)
    if not( self.Z_MIN_LIMIT <= j3 <= self.Z_MAX_LIMIT ):
      msg = f'CommandSender.jump_joint_to(...) の 引数 z は {self.Z_MIN_LIMIT} 以上 {self.Z_MAX_LIMIT} 以下で与えてください。'
      raise ValueError(msg)
    return self._send(dict(command='JumpJointTo',j1=j1,j2=j2,j3=j3,j4=j4))

  def go_to(self, x:int, y:int, z:int, r:int=0):
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
    if not( self.Z_MIN_LIMIT <= z <= self.Z_MAX_LIMIT ):
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
