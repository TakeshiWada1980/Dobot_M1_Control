import logging
import dobot

if __name__ == '__main__':

  logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
  logging.getLogger('DobotCommandSender').setLevel(logging.DEBUG)
  cs = dobot.CommandSender('127.0.0.1')

  # 初期設定系
  cs.arm_orientation(mode=1)
  cs.set_cordinate_speed(velocity=20,jerk=50)
  cs.set_jump_pram(height=20,zlimit=200)
  
  # I/O系
  cs.set_output(pin=1,value=1)
  cs.set_output(pin=100,value=1)
  cs.set_output(pin=1,value=-1)
  cs.get_input(pin=1)
  cs.wait(2000)

  # 移動系
  cs.jump_to(x=350,y=10,z=40)

  cs.jump_to(x=350,y=10,z=40,r=20)
  #cs.jump_to(x=350,y=10,z=1140,r=20)
  
  cs.go_to(x=350,y=10,z=40)
  cs.quit()
