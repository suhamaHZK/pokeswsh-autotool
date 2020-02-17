################################################################
# レイドバトルが始まり次第ホスト機をリセットします。           #
# インターネットに接続して「みんなで 挑戦！」を選ぶ直前まで    #
# 手動で進めてから、本スクリプトを起動してください。           #
#                                                              #
# Switch本体やソフトの遅延によりうまく動かない場合があります。 #
# その場合は、適宜sleepの秒数を伸ばしてください。              #
#                                                              #
# 動作確認環境                                                 #
#   Python 3.7.5                                               #
#   pyserial 3.4                                               #
#   macOS 10.14.6                                              #
################################################################

import argparse
import serial
from time import sleep

def macro():
    while True:
        # 「みんなで 挑戦！」を選ぶ直前からスタート
        if wait_enter('Enterで募集開始します'): break #Enterを待つ。何か入力された場合(空文字列じゃなかった場合)はそこで終了
        send('Button A', 0.1)#みんなで挑戦
        if wait_enter('2台目の参加を待っています...'): break

        send('HAT TOP', 0.1)# 「準備完了！」にカーソルをあわせる
        send('HAT CENTER', 0.5)
        send('Button A', 0.1)#押す
        sleep(0.5)
        send('Button A', 0.1)#「バトルを 開始する」を選択
        sleep(0.5)
        send('Button A', 0.1)#「参加人数が たりません！」
        sleep(0.5)
        send('Button A', 0.1)#「サポートのトレーナーが参加しますがよろしいですか？」→はい
        sleep(0.1)

        if wait_enter('バトル開始を待っています...'): break

        # リセットする
        send('Button HOME', 0.1)#ホームへ
        sleep(1.2)
        send('Button X', 0.1)#終了します
        sleep(1.2)
        send('Button A', 0.1)#終了を選択
        sleep(3) #終了処理待ち
        send('Button A', 0.1)#ゲーム選択
        sleep(1.2)
        send('Button A', 0.1)#ユーザ選択
        sleep(20) #起動権チェック、ゲームの起動処理、OPムービー

        send('Button A', 0.1)#ゲーム開始
        sleep(10) #セーブデータ読み込み処理待ち

        send('Button Y', 0.1)#YY通信
        sleep(2)
        send('Button START', 0.1)#インターネット接続
        sleep(10) #接続完了待ち
        send('Button B', 0.1)#「接続しました」を閉じる
        sleep(0.5)
        send('Button B', 0.1)#YY通信を閉じる
        sleep(2)

        send('Button A', 0.1)#巣穴を調べる
        sleep(5) #通信待機中
        # 「みんなで 挑戦！」を選ぶところまで戻ってきた



parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()

def send(msg, duration=0):
    print('SEND '+msg)
    ser.write(f'{msg}\r\n'.encode('utf-8'));
    sleep(duration)
    ser.write(b'RELEASE\r\n');

def hold(msg):
    print('HOLD '+msg)
    ser.write(f'{msg}\r\n'.encode('utf-8'));
    sleep(duration)
    ser.write(b'RELEASE\r\n');

def wait_enter(notice):
    print(notice)
    r = input()
    return r

ser = serial.Serial(args.port, 9600)

try:
    # First Link
    send('Button L', 0.1)
    sleep(1)

    macro()

    send('RELEASE')
    sleep(0.5)
    ser.close()
except KeyboardInterrupt:
    send('RELEASE')
    sleep(0.5)
    ser.close()
