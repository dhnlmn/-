import socket
import time
import json
import  threading
Thread_Flag=1  #死锁计时进程
qian_Flag=0  #五次签到统计一次成员个数，五次签到一次都算
New_table=[]  #新的成员列表，签到的就放里面
def sever():
    global Thread_Flag,qian_Flag,New_table
    HOST = '<broadcast>'
    #HOST = "192.168.31.255"
    ADDR = (HOST, 8884)

    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #设置可以广播
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    s.bind(("192.168.0.105", 8884))

    #列表保存所有的客户
    cli_list = []

    while True:
        if Thread_Flag:
            Thread_Flag=0
            t=threading.Thread(target=thread_func,args=(s,cli_list,ADDR))
            t.start()
        info = {}
        #接收数据
        data, addr = s.recvfrom(1024)
        #屏蔽服务端接收到自己的数据
        if addr[0] == "192.168.0.105":
            continue
        data=data.decode()
        print(qian_Flag)
        if  qian_Flag>=5:   #可能掉包无法更新，开始更新在线数
            print("开始更新成员")
            qian_Flag=0
            cli_list=New_table
            info["type"]="updata"
            info["data"]=cli_list
            New_table=[]
            s.sendto(bytes(json.dumps(info), encoding="utf8"),ADDR) #更新列表给各个客户端
            continue
        if data=="1":     #如果接受心跳包
            if addr not in New_table:  #检测是不是新成员
                New_table.append(addr)
            print("收到心跳包")
            continue
        if addr in cli_list: #老的客户端
            print("老客户端：", addr, data)
            info['type'] = "data"
        else:
            #将新的客户端添加的cli_list
            cli_list.append(addr)
            print("新的客户端：", addr, data)
            info['type'] = "member"

        info['addr'] = addr
        info['data'] = data
        #广播数据 json.dumps(info)：将字典转换成字符串

        s.sendto(bytes(json.dumps(info), encoding="utf8"),ADDR)

        time.sleep(1)
def thread_func(s,cli_list,ADDR):    #心跳检测
    global  qian_Flag
    info="签到"
    while True:
        time.sleep(5)    #睡五秒进行一次签到消息发送
        s.sendto(bytes(info, encoding="utf8"),ADDR)  #发签到消息
        qian_Flag=qian_Flag+1   #每次签到次数加1，五次更新
        #time.sleep(5)

if __name__ == '__main__':
    sever()