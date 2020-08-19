import pytest
import time
import subprocess
import dobot

# pytest test_dobot.py -v
# pytest test_dobot.py -v -k "jump_to"

@pytest.fixture(scope='module')
def cs():
  subprocess.Popen(['python','server.py'])
  time.sleep(1)
  cs = dobot.CommandSender(host='127.0.0.1')
  yield cs
  cs.quit()

@pytest.mark.parametrize(('x','y','z','r','expected'), [
  (10,10,20,None,  True),
  (10,10,20,0,     True),
  (10,10, 0,0,     False),  # z の範囲異常
])
def test_jump_to(x,y,z,r,expected,cs):
  if r == None :
    ret = cs.jump_to(x,y,z)
  else :
    ret = cs.jump_to(x,y,z,r)
  assert ret['is_sccess'] == expected