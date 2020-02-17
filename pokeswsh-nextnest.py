import argparse
import serial
from time import sleep
import datetime

default_count = 1000
default_date = '2000-01-01'

def macro(count,today):
    # ui_wait = 0.07
    ui_wait = 0.07
    # today = datetime.date(year,month,day)
    for i in range(count):
        tomorrow = today + datetime.timedelta(days=1)
        starttime = datetime.datetime.now()

        print('============')
        print(i+1, '/', count)
        print('today:',today)

        # ワット収穫
        send('Button A', 0.1)
        sleep(0.5)
        send('Button B', 0.1)
        sleep(0.5)
        send('Button B', 0.1)
        sleep(0.5)
        send('Button B', 0.1)
        sleep(0.5)
        send('Button B', 0.1)
        sleep(1.3)

        # 穴を調べる
        send('Button A', 0.1)
        sleep(0.5)
        send('Button A', 0.1)
        sleep(3) #通信待機中
        send('Button HOME', 0.1)
        sleep(1)

        # 設定を開く
        send('HAT BOTTOM', ui_wait)
        send('HAT CENTER', ui_wait)
        send('HAT RIGHT', ui_wait)
        send('HAT CENTER', ui_wait)
        send('HAT RIGHT', ui_wait)
        send('HAT CENTER', ui_wait)
        send('HAT RIGHT', ui_wait)
        send('HAT CENTER', ui_wait)
        send('HAT RIGHT', ui_wait)
        send('HAT CENTER', ui_wait)
        send('Button A', ui_wait)
        sleep(1.5)

        # 本体 > 日付と時刻 を選ぶ
        for j in range(14):
            send('HAT BOTTOM', ui_wait)
            send('HAT CENTER', ui_wait)
        send('HAT RIGHT', ui_wait)
        send('HAT CENTER', 0.2)
        for j in range(4):
            send('HAT BOTTOM', ui_wait)
            send('HAT CENTER', ui_wait)
        send('Button A', ui_wait)
        sleep(1)

        # 現在の日付と時刻 を選ぶ
        for j in range(2):
            send('HAT BOTTOM', ui_wait)
            send('HAT CENTER', ui_wait)
        send('Button A', ui_wait)
        sleep(0.5)
        print('')

        print('set date from', today, 'to', tomorrow)

        # 時刻を変更
        for j in range(2): # 右を2回押して 日 を選択
            send('HAT RIGHT', ui_wait)
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
        send('Button A', ui_wait)
        sleep(0.5)

        # Returm to the Game
        send('Button HOME', 0.1)
        sleep(1)
        send('Button HOME', 0.1)
        sleep(1)
        send('Button B', 0.1)
        # sleep(0.6)
        sleep(1)
        send('Button A', 0.1)
        sleep(4)
        print('')

        print('Date has changed', i+1, 'times.')

        # increase date
        today = tomorrow
        print(datetime.datetime.now() - starttime)
    print('\a')

def init_macro(isauto='ask', isend=False):
    ui_wait = 0.07
    print('\a')

    # 設定を開く
    send('Button HOME', 0.1)
    sleep(1)
    send('HAT BOTTOM', ui_wait)
    send('HAT CENTER', ui_wait)
    send('HAT RIGHT', ui_wait)
    send('HAT CENTER', ui_wait)
    send('HAT RIGHT', ui_wait)
    send('HAT CENTER', ui_wait)
    send('HAT RIGHT', ui_wait)
    send('HAT CENTER', ui_wait)
    send('HAT RIGHT', ui_wait)
    send('HAT CENTER', ui_wait)
    send('Button A', ui_wait)
    sleep(1.5)

    # 本体 > 日付と時刻 を選ぶ
    for j in range(14):
        send('HAT BOTTOM', ui_wait)
        send('HAT CENTER', ui_wait)
    send('HAT RIGHT', ui_wait)
    send('HAT CENTER', 0.5)
    for j in range(4):
        send('HAT BOTTOM', ui_wait)
        send('HAT CENTER', ui_wait)
    send('Button A', ui_wait)
    sleep(1)
    print('')

    while isauto == 'ask':
        print('')
        print('"インターネットで時刻をあわせる"はONになっていますか？')
        print('Y/N [Y]: ',end='')
        yesno = input().lower()
        if yesno == 'yes' or yesno == 'y' or yesno == '':
            isauto = True
            break
        elif yesno == 'no' or yesno == 'n':
            isauto = False
            break
        # 変な入力だった場合は聞き直す

    if not isauto: # 自動時刻合わせがOFFなら、まずはONにする
        send('Button A', ui_wait)
        sleep(0.5)
    send('Button A', ui_wait)
    sleep(0.5)

    if not isend:
        # 日時変更を選択する
        for j in range(2):
            send('HAT BOTTOM', ui_wait)
            send('HAT CENTER', ui_wait)
        send('Button A', ui_wait)
        sleep(0.5)

        # 時刻を変更
        nowhour = datetime.datetime.now().hour
        for j in range(3): # 右を3回押して 時 を選択
            send('HAT RIGHT', ui_wait)
            send('HAT CENTER', ui_wait)
        if nowhour >= 12:      # 12時以降なら
            for j in range(5): # 5時間くらい戻しておく
                send('HAT BOTTOM', ui_wait)
                send('HAT CENTER', ui_wait)
        for j in range(2):
            send('HAT RIGHT', ui_wait)
            send('HAT CENTER', ui_wait)
        send('Button A', ui_wait)
        sleep(0.5)

    # Returm to the Game
    send('Button HOME', 0.1)
    sleep(1)
    send('Button HOME', 0.1)
    print('\n')
    return isauto

def wizard():
    today = datetime.date.today()
    totalcount = 0
    while True:
        print('====================================================================')
        print('現在、Switchの日付は', today, '、日付変更回数は', totalcount, '回です')
        print('日付を進める回数を指定してください(自然数以外を指定すると終了します)')
        print('command = ',end='')
        cmdstr = input()
        if cmdstr == 'reset' or cmdstr == 'r':
            totalcount = 0
            continue
        if not cmdstr.isdecimal(): break
        count = int(cmdstr)
        if count < 1: break
        macro(count, today)
        today = today + datetime.timedelta(days=count)
        totalcount += count
    print('自然数以外が指定されたため、終了します')

parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()

def send(msg, duration=0):
    print(msg.split(' ')[-1], end=' ', flush=True)
    ser.write(f'{msg}\r\n'.encode('utf-8'));
    sleep(duration)
    ser.write(b'RELEASE\r\n');

ser = serial.Serial(args.port, 9600)

try:
    # First Link
    # send('Button CAPTURE', 0.1)
    send('Button R', 0.1)
    sleep(0.1)
    print('')

    isauto = init_macro()

    wizard()

    print('')
    print('初期状態に戻します。')
    init_macro(isauto=isauto, isend=True)
    sleep(0.1)
    send('RELEASE')
    print('')
    sleep(0.5)
    ser.close()
except KeyboardInterrupt:
    print('')
    print('KeyboardInterruptにより処理が中断されました。')
    print('日時設定は手動でもとに戻しておいてください。')
    sleep(0.1)
    send('RELEASE')
    print('')
    sleep(0.5)
    ser.close()
