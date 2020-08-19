# DobotM1の制御

Dobot Studio の Pythonランタイムで実行するプログラムと、それとは別のPythonランタイムで実行するプログラムで、ソケット通信するための雛形

- server.py : Dobot Studio で実行するプログラム
- client.py : 上記とは別のPythonランタイムで実行するプログラム（dobot.pyをインポートする）
 - dobot.py : Dobot Studio 動作しているプログラミングにコマンドを送信するライブラリ
