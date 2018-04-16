import machine 
rtc = machine.RTC()
rtc.init((2018, 3, 20, 11, 22, 0, 0, 0))
print(rtc.datetime())