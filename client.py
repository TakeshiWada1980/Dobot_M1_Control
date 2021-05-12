import logging
import dobot

if __name__ == '__main__':

  logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
  logging.getLogger('DobotCommandSender').setLevel(logging.DEBUG)
  cs = dobot.CommandSender('127.0.0.1',8889)

  # 初期設定系
  cs.set_cordinate_speed(velocity=20,jerk=50)
  cs.set_jump_pram(height=60,zlimit=180)

  # 初期位置にセット
  cs.jump_joint_to(j1=0,j2=0,j3=60,j4=0)
  cs.wait(1000)

  # メイン処理
  cs.arm_orientation(mode=1) # 0=Left 1=Right 
  cs.jump_to(x=150,y=250,z=60)
  cs.wait(1000)

  cs.jump_to(x=350,y=0,z=60)
  cs.wait(1000)

  cs.arm_orientation(mode=0) # 0=Left 1=Right     
  cs.jump_to(x=150,y=-200,z=60)
  cs.wait(1000)

  # 初期位置に戻る
  cs.jump_joint_to(j1=0,j2=0,j3=60,j4=0)
  cs.quit()

  # I/O系
  # cs.set_output(pin=1,value=1)
  # cs.set_output(pin=100,value=1)
  # cs.set_output(pin=1,value=-1)
  # cs.get_input(pin=1)
  # cs.wait(2000)
  