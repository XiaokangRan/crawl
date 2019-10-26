import threading
import os, sys
import pickle
##https://www.jianshu.com/p/a4aedd66af7c
#把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
lock=threading.Lock()
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def extract(self):
        lock.acquire()
        # 中间操作变量：如果不加lock，多个线程会同时访问这些变量
        lock.release()


list_thread = []
try:
    print('start...')
    for i in range(12):
        list_thread.append(MyThread())
    for th in list_thread:
        th.start()
        th.join()
except Exception as err:
    for th in list_thread:
        th.terminate()
    print('error!', sys.exc_info()[0])
finally:
    print('save state')
    # pickle.dump(paged, open('paged.bin', 'wb'))
    # fail_file.close()
