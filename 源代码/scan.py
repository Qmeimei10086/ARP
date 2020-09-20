from scapy.all import *


fp = open('host.txt','w')
def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip


def worker():
    ip_list=[]

    lport = get_host_ip()
    print('你的IP:    '+str(lport))
    host = str(lport[:10])
    for ipFix in range(1,100):



        ip= host+str(ipFix)
        arpPkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
        res = srp1(arpPkt, timeout=1, verbose=False)
        if res:
            print (res.psrc)
            ip_list.append(res.psrc)
            fp.write(res.psrc + '\n')
    return ip_list

if __name__=="__main__":

    ip_list = worker()
    i = 0
    for ip in ip_list:
        i += 1
    print("扫描到的IP数:"+str(i))
    fp.close()


