import pytest
import time
import subprocess
import dobot

# pytest test_dobot.py -v
# pytest test_dobot.py -v -k "jump_to"
# [Ctrl]+[Shift]+[P] Python: Run All Tests
# [Ctrl]+[Shift]+[P] Python: Show Test Output

@pytest.fixture(scope='module')
def cs():
  subprocess.Popen(['python','server.py'])
  time.sleep(1)
  cs = dobot.CommandSender(host='127.0.0.1',port=8893)
  yield cs
  cs.quit()

@pytest.mark.parametrize(('x','y','z','r','expected'), [
  (   10,    10,   60, None,  True),
  (   10,    10,   60,    0,  True),
  (   10,    10,    0,    0,  ValueError), # zの範囲異常 raises(ValueError
  (   10,  '10',    0,    0,  TypeError ), # yのses(ValueError
])
def test_jump_to(x,y,z,r,expected,cs):

  if not isinstance(expected,bool) :
    with pytest.raises(expected):
      _ = cs.jump_to(x,y,z) if ( r is None ) else cs.jump_to(x,y,z,r)
  else :
    ret = cs.jump_to(x,y,z) if ( r is None ) else cs.jump_to(x,y,z,r)
    assert ret['is_sccess'] == expected
