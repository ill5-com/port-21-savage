from ftplib import FTP
from queue import Queue
import threading
import time

numberOfThreads = 250
timeOut = 10

serversQueue = Queue()
writeQueue = Queue()

def WriteThread():
    global serversQueue
    global writeQueue

    while serversQueue.qsize() > 0:
        with open("out.txt", 'a') as f:
            while writeQueue.qsize() > 0:
                f.write(writeQueue.get() + '\n')

        time.sleep(1)

    return

def ScannerThread(threadId):
    global serversQueue
    global writeQueue

    print("Started thread #" + str(threadId))

    while serversQueue.qsize() > 0:
        try:
            currentIp = serversQueue.get()

            ftpServer = FTP(currentIp, timeout=timeOut)
            ftpServer.login()

            responseLines = []
            responseCode = ftpServer.retrlines('LIST', responseLines.append)

            if "226" in responseCode:
                print("IP: " + currentIp, "CODE: " + responseCode, '-' * 24, '\n'.join(responseLines), '-' * 24, sep='\n')
                writeQueue.put(currentIp)

            ftpServer.quit()
        except Exception as e:
            #print(e)
            continue

    return

def Main():
    global serversQueue

    for line in open("ips.txt"):
        serversQueue.put(line.strip())

    threads = []

    for i in range(numberOfThreads):
        threads.append(threading.Thread(target=ScannerThread, args=(i,)))

    writeThread = threading.Thread(target=WriteThread)
    writeThread.start()

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    writeThread.join()

    return

if __name__ == "__main__":
    Main()
