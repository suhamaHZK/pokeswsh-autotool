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

# memo
# バックアップあか始めるオプションをつけたい -b
#   →同時押しができない！

import argparse
import serial
from time import sleep

def macro(load_backup = False, pin=''):
    if pin != '':
        if wait_enter('パスワード '+pin+' を設定します。Enterを押してください...'): break
    while True:
        if pin != '':
            set_pin(pin)
            print('パスワードは '+pin+' です。')
        # 「みんなで 挑戦！」を選ぶ直前からスタート
        if wait_enter('Enterで募集開始します...'): break #Enterを待つ。何か入力された場合(空文字列じゃなかった場合)はそこで終了
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
        sleep(2)
        send('Button A', 0.1)#ユーザ選択
        sleep(20) #起動権チェック、ゲームの起動処理、OPムービー

        if load_backup:
            wait_enter('上とBを押しながらXを押してください。ロード画面になったらEnter')
            # hold('HAT TOP', 0.1)
            # hold('Button B', 0.1)
            # hold('Button X', 0.1)
            # send('HAT CENTER', 0.1)
            # send('RELEASE')# ↑+B+Xでバックアップからゲーム開始
            # sleep(3)
            send('Button A', 0.1)#確認画面で「はじめる」を押す
            sleep(3)
            send('Button A', 0.1)#注意書き
            sleep(10) #セーブデータ読み込み処理待ち
        else:
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

def set_pin(pin):
    pinpad=[           # [x,y] で表記。横がx 縦がy
          [1,3],       #   0
    [0,0],[1,0],[2,0], # 1 2 3
    [0,1],[1,1],[2,1], # 4 5 6
    [0,2],[1,2],[2,2]  # 7 8 9
    ]
    pos = [0,0] # 初期位置は "1" (左上)

    send('Button START', 0.1)#PIN入力画面へ
    sleep(1)
    for i in range(4):
        pindigit = int(pin[i])
        nextpos = pinpad[pindigit]
        xmove = nextpos[0] - pos[0]
        ymove = nextpos[1] - pos[1]

        if pindigit == 0: # 0に移動
            # 横移動
            if xmove > 0: # 正なら右に動く
                for j in range(xmove):
                    send('HAT RIGHT', 0.1)
                    send('HAT CENTER', 0.1)
            else:
                for j in range(xmove * -1):
                    send('HAT LEFT', 0.1)
                    send('HAT CENTER', 0.1)
            # 縦移動
            if ymove > 0: # 正なら下に動く
                for j in range(ymove):
                    send('HAT BOTTOM', 0.1)
                    send('HAT CENTER', 0.1)
            else:
                for j in range(ymove * -1):
                    send('HAT TOP', 0.1)
                    send('HAT CENTER', 0.1)
        else: # 0以外に移動
            # 縦移動
            if ymove > 0: # 正なら下に動く
                for j in range(ymove):
                    send('HAT BOTTOM', 0.1)
                    send('HAT CENTER', 0.1)
            else:
                for j in range(ymove * -1):
                    send('HAT TOP', 0.1)
                    send('HAT CENTER', 0.1)
            # 横移動
            if xmove > 0: # 正なら右に動く
                for j in range(xmove):
                    send('HAT RIGHT', 0.1)
                    send('HAT CENTER', 0.1)
            else:
                for j in range(xmove * -1):
                    send('HAT LEFT', 0.1)
                    send('HAT CENTER', 0.1)
        pos = nextpos

        send('Button A', 0.1)#入力
        sleep(0.2)

    send('Button START', 0.1)#確定
    sleep(1)
    send('Button A', 0.1)#よろしいですか？ →A (言語によって注意書きの長さ=Aボタン回数がちがうかも)
    sleep(0.5)


parser = argparse.ArgumentParser()
parser.add_argument('port')
parser.add_argument('-b','--backup', action='store_true')
parser.add_argument('-p','--pin', default='')

args = parser.parse_args()

def send(msg, duration=0):
    print('SEND '+msg)
    ser.write(f'{msg}\r\n'.encode('utf-8'));
    sleep(duration)
    ser.write(b'RELEASE\r\n');

def hold(msg, duration=0):
    print('HOLD '+msg)
    ser.write(f'{msg}\r\n'.encode('utf-8'));
    sleep(duration)

def wait_enter(notice):
    print(notice)
    r = input()
    return r

ser = serial.Serial(args.port, 9600)

try:
    # First Link
    send('Button L', 0.1)
    sleep(1)

    macro(load_backup=args.backup,pin=args.pin)

    send('RELEASE')
    sleep(0.5)
    ser.close()
except KeyboardInterrupt:
    send('RELEASE')
    sleep(0.5)
    ser.close()
