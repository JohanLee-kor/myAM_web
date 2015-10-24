import time

def mkLog(part, msg):
        f = open("./myAMlog.jh",'a')
        log = "["+part+"] : "+str(msg)+"\t|"+str(time.asctime())+"|\n"
        f.write(log)
        f.close()