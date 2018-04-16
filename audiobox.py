# Intelligent Audio Box.py
import usocket
import utime
import ujson
from machine import Pin

DEVICEID = 'bugaosuni'
APIKEY = 'zheshimimi'
host = 'www.bigiot.net'
port = 8181

previous_sw = Pin(25,Pin.OUT,value = 0)
next_sw = Pin(26,Pin.OUT,value = 0)
power_sw = Pin(27,Pin.OUT,value = 0)

addr_info = usocket.getaddrinfo(host,port)
addr = addr_info[0][-1]
s = usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
s.settimeout(1)
s.connect(addr)

while True:
    try:     
        data = s.recv(100)
        print(str(data, 'utf8'), end='')
        s.send(b'{\"M\":\"status\"}\n')
        break
    except:
        break

#Processing incoming messages
checkinBytes = bytes('{\"M\":\"checkin\",\"ID\":\"'+DEVICEID+'\",\"K\":\"'+APIKEY+'\"}\n','utf8')
def process(msg,s,checkinBytes):
    msg = ujson.loads(msg)
    if msg['M'] == 'connected':
        s.send(checkinBytes)
    if msg['M'] == 'login':
        say(s,msg['ID'],'Welcome! Your public ID is '+msg['ID'])
    if msg['M'] == 'say':
        say(s,msg['ID'],'You have send to me:{'+msg['C']+'}')
        if msg['C'] == "offOn":
            if power_sw.value() == 1:
                power_sw.value(0)
                say(s,msg['ID'],'Power Off!')
            else:
                power_sw.value(1)
                say(s,msg['ID'],'Power On!')
        if msg['C'] == "forward":
            next_sw.value(1)
            utime.sleep_ms(450)
            next_sw.value(0)
        if msg['C'] == "backward":
            previous_sw.value(1)
            utime.sleep_ms(450)
            previous_sw.value(0)                        
        if msg['C'] == "plus":
            next_sw.value(1)
            utime.sleep_ms(1400)
            next_sw.value(0)
        if msg['C'] == "minus":
            previous_sw.value(1)
            utime.sleep_ms(1400)
            previous_sw.value(0)
            
def say(s,id,content):
    sayBytes = bytes('{\"M\":\"say\",\"ID\":\"'+id+'\",\"C\":\"'+content+'\"}\n','utf8')
    print(sayBytes)
    s.send(sayBytes)
    
#mian loop and processing messages
data = b''
flag = 1
t = utime.time()
def keepOnline(t):
    if utime.time()-t>20:
        s.send(b'{\"M\":\"status\"}\n')
        return utime.time()
    else:
        return t
while True:
    try:
        d=s.recv(1)
        flag=True
    except:
        flag=False
        utime.sleep(2)
        t = keepOnline(t)
    if flag:
        if d!=b'\n':
            data+=d
        else:
            #do something here...
            print(str(data, 'utf8'), end='\n')     
            msg = str(data, 'utf8')  
            process(msg,s,checkinBytes)
            data=b''




