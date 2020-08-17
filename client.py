import socket
import logging
import time

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s')
log = logging.getLogger(__name__)
log.setLevel(level=logging.INFO)

HOST = '127.0.0.1'
PORT = 8889
BUFFER_SIZE = 1024

def send_command(command):

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(command.encode())
    log.info('"{0}"...'.format(command))
    res = s.recv(BUFFER_SIZE).decode('UTF-8')
  log.info('   -> "{0}"'.format(res))

send_command('JUMP TO 400 20 20')
time.sleep(2)
send_command('JUMP TO 350 20 20')
time.sleep(2)
send_command('JUMP TO 400 20 20')
time.sleep(2)
send_command('QUIT')