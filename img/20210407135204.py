import binascii
import serial
import time

def Get_Txt():
    seriall = serial.Serial(port='COM6', baudrate=115200, stopbits=1,timeout=0.5)  # /dev/ttyUSB0
    if seriall.isOpen():
        print("open success")
    else:
        print("open failed")

    seriall.write('b'.encode())
    complete_info = ""
    i=0
    time_start = int(time.time())
    while True:
        data = seriall.inWaiting()
        if data:
            data = str(binascii.b2a_hex(seriall.read(data)))[2:-1]
            complete_info =complete_info + data
            if (int(time.time()) - time_start) == 5:
                break
    start_position = int(complete_info.find("c0a0")) + 2
    print(complete_info)
    while True:
        first_end_str = complete_info[start_position + 64:start_position+66]
        if first_end_str == "c0":
            break
        else:
            start_position = int(complete_info[start_position + 66:].find("c0a0"))
    with open("eye_move7.txt",'w',encoding="utf-8") as file:
        file.write("用来训练的数据!\n")
        end = False
        while not end:
            for i in range(256):
                Calculate(i,complete_info[start_position:start_position+66])
                file.write("{Order}\t{Channel1}\t{Channel2}\t{Channel3}\t{Channel4}\t{Channel5}\t{Channel6}\t{Channel7}\t{Channel8}\n".format(**brain_info))
                start_position += 66
                if len(complete_info) - start_position < 66:
                    end = True
                    break

def Calculate(i,each_info):
        brain_info["Order"] = i
        for end_num in range(8):
            substr1 = each_info[4+ 6 * end_num:6*(end_num+1)]
            decide = int(substr1,16)
            substr2 = each_info[4+ 6*end_num:10+ 6*end_num]
            convert_num = int(substr2,16)
            if decide < 127:
                brain_info["Channel{}".format(end_num+1)] = convert_num * 0.022351744455307063
            else:
                brain_info["Channel{}".format(end_num+1)] = -convert_num * 0.022351744455307063

if __name__ == "__main__":
    # 用来保存每一行的脑电波数据
    brain_info ={
        "Order":0,
        "Channel1":0.0,
        "Channel2":0.0,
        "Channel3":0.0,
        "Channel4":0.0,
        "Channel5":0.0,
        "Channel6":0.0,
        "Channel7":0.0,
        "Channel8":0.0
    }
    Get_Txt()


    