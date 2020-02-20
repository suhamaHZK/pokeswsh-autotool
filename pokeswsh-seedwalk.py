import argparse
import serial
import datetime
from time import sleep

def setcount(today):
    print('◆ 使い方 ◆')
    print('1. 「インターネットで時刻をあわせる」を一旦ONにしたあと、OFFにしてください。')
    print('2. 作業中に日付をまたがないよう、時刻を 0:00 に設定してください。')
    print('3. レート戦を1戦行ってください。(YY通信による方法でもOKのはず)')
    print('4. ソフトをインターネットから切断してください。')
    print('5. 「現在の日付と時刻」にカーソルを合わせてください。')
    print('   (Aボタンはまだ押さないでください)')
    print('6. マクロアダプタを接続してから、本スクリプトを起動してください。')

    count = 0
    while True:
        print('===================================')
        print('現在、Switchの日付は', today, 'です')
        print('日付を進める回数を指定してください("x" または "exit" で終了)')
        print('command = ',end='')
        cmdstr = input()
        if cmdstr == 'x' or cmdstr == 'exit': exit()
        if not cmdstr.isdecimal(): continue # 整数じゃなかったら聞き直す
        count = int(cmdstr)
        if count < 1: continue # 0だったら聞き直す
        break
    return count

def macro(today,count):
    commit_rate = 100

    # First Link
    send('Button R', 0.1)
    sleep(0.3)

    # 初期設定
    send('Button A', 0.1)
    sleep(0.3)
    for i in range(5):
        send('HAT RIGHT', 0.1)
        send('HAT CENTER', 0.1)
    send('Button A', 0.1)
    sleep(0.3)

    # 本ループ
    starttime = datetime.datetime.now()
    for i in range(count):
        tomorrow = today + datetime.timedelta(days=1)
        print('============')
        print(i+1, '/', count, today)

        ui_wait = 0.1
        # 日付を変更
        send('Button A', 0.1)
        sleep(0.3)
        for j in range(3): # 左を3回押して 日 を選択
            send('HAT LEFT', ui_wait)
            send('HAT CENTER', ui_wait)
        send('HAT TOP', ui_wait) # 1日進める
        send('HAT CENTER', ui_wait)
        if tomorrow.day == 1: # 次の日が月初なら
            send('HAT LEFT', ui_wait)
            send('HAT CENTER', ui_wait)
            send('HAT TOP', ui_wait) # 月を進める
            send('HAT CENTER', ui_wait)
            if tomorrow.month == 1: # 次の日が元日なら
                send('HAT LEFT', ui_wait)
                send('HAT CENTER', ui_wait)
                send('HAT TOP', ui_wait) # 年を進める
                send('HAT CENTER', ui_wait)
                send('HAT RIGHT', ui_wait)
                send('HAT CENTER', ui_wait)
            send('HAT RIGHT', ui_wait)
            send('HAT CENTER', ui_wait)
        for j in range(3):
            send('HAT RIGHT', ui_wait)
            send('HAT CENTER', ui_wait)
        sleep(0.1)
        send('Button A', 0.1)
        sleep(0.3)

        # commit_rate 回ごとに、一旦ゲームに戻る
        if (i+1)%commit_rate == 0:
            # ゲームに戻る
            sleep(0.2)
            send('Button HOME', 0.1)
            sleep(1.5)
            send('Button HOME', 0.1)
            sleep(3)

            # 設定を開く
            send('Button HOME', 0.1)
            sleep(1)
            send('HAT BOTTOM', 0.1)
            send('HAT CENTER', 0.1)
            send('HAT RIGHT', 0.1)
            send('HAT CENTER', 0.1)
            send('HAT RIGHT', 0.1)
            send('HAT CENTER', 0.1)
            send('HAT RIGHT', 0.1)
            send('HAT CENTER', 0.1)
            send('HAT RIGHT', 0.1)
            send('HAT CENTER', 0.1)
            send('Button A', 0.1)
            sleep(1.5)

            # 本体 > 日付と時刻 を選ぶ
            for j in range(14):
                send('HAT BOTTOM', 0.1)
                send('HAT CENTER', 0.1)
            send('HAT RIGHT', 0.1)
            send('HAT CENTER', 0.5)
            for j in range(4):
                send('HAT BOTTOM', 0.1)
                send('HAT CENTER', 0.1)
            send('Button A', 0.1)
            sleep(1)

            # 日時変更を選択する
            for j in range(2):
                send('HAT BOTTOM', 0.1)
                send('HAT CENTER', 0.1)

        # increase date
        today = tomorrow
    print('========================')
    print('Finish')
    print('count:', count)
    print('today:', today)
    print(datetime.datetime.now() - starttime)





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

today = datetime.date.today()
# today = datetime.date(2020,12,30) # to debug
count = setcount(today)

ser = serial.Serial(args.port, 9600)

try:
    # # First Link
    # send('Button R', 0.1)
    # sleep(0.3)

    macro(today,count)

    send('RELEASE')
    sleep(0.5)
    ser.close()
except KeyboardInterrupt:
    send('RELEASE')
    sleep(0.5)
    ser.close()
