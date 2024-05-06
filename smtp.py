import socket
import ssl
import base64
import re

host = ('smtp.yandex.ru', 465)
video = base64.b64encode(open('video.mp4', 'rb').read())
exts = {'mp4': 'video/mp4', 'png': 'image/png',
        'jpg': 'image/jpeg', 'mp3': 'audio/mpeg',
        'gif': 'image/gif'}
dotsRe = re.compile('^\.+$')


def main():
    send_msg()


def send_recv(str, s):
    str += b'\n'
    s.send(str)
    return s.recv(1024).decode(encoding='utf-8')


def create_msg(sendr, recvr, subj, text, attchmnt):
    sector = b''
    if attchmnt != '':
        ext = attchmnt.split('.')[len(attchmnt.split('.')) - 1]
        type = exts[ext]
        attchmnt_bytes = base64.b64encode(open(attchmnt, 'rb').read())
        sector = b'''
--iLoveSnacks
Content-Type: ''' + bytes(type, 'utf-8') + b'''; name="''' + bytes(attchmnt, 'utf-8') + b'''"
Content-Disposition: attachment;
Content-Transfer-Encoding: base64

''' + attchmnt_bytes

    return b'''From: ''' + bytes(sendr, 'utf-8') + b'''
To: ''' + bytes(recvr, 'utf-8') + b'''
Subject: ''' + bytes(subj, 'utf-8') + b'''
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="iLoveSnacks"

--iLoveSnacks
Content-Type: text/plain;

''' + bytes(text, 'utf-8') + b'''

''' + sector + b'''

--iLoveSnacks--
.
'''


def send_msg():
    print('Type your email')
    sendr = input('>')
    if sendr == '':
        sendr = 's.balashov.ya@yandex.ru'
    print('Type other email')
    recvr = input('>')
    if recvr == '':
        recvr = 's.balashov.ya@yandex.ru'
    print('Type subject')
    subj = input('>')
    if subj == '':
        subj = 'Interesting thing'
    text = ""
    print('Type text')
    path = input('>')
    if path == '':
        text = 'Hello, I want to tell you about one of my best idea!'
    else:
        file = open(path, 'r')
        while True:
            line = file.readline()
            if line == '':
                break
            if dotsRe.match(line):
                line = '.' + line
            text += line

    print('Type path to your attachment (supported: gif, jpg, png, mp3, mp4)')
    attchmnt = input('>')


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s = ssl.wrap_socket(s)
        s.connect(host)
        print(s.recv(1024))
        login = base64.b64encode(b's.balashov.ya@yandex.ru')
        password = base64.b64encode(b"khpopmqovhhoskkd")
        print(send_recv(b'EHLO s.balashov.ya@yandex.ru', s))
        print(send_recv(b'AUTH LOGIN', s))
        print(send_recv(login, s))
        print(send_recv(password, s))
        print(send_recv(b'MAIL FROM: ' + bytes(sendr, 'utf-8'), s))
        print(send_recv(b'RCPT TO: ' + bytes(recvr, 'utf-8'), s))
        print(send_recv(b'DATA', s))
        print(send_recv(create_msg(sendr, recvr, subj, text, attchmnt), s))


if __name__ == '__main__':
    main()
