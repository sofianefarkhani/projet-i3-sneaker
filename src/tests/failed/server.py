import socket 
from threading import Thread 
from socketserver import ThreadingMixIn 
import cv2
import numpy


class myThread(Thread): 
    img = cv2.imread('../../img/test/1.png')
    
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print ("[+] Nouveau thread démarré pour " + ip + ":" + str(port))
 
    def run(self): 
        while True : 
            data = con.recv(2048) 
            print("Le serveur a reçu des données:", data) 
            msg = input("Entrez la réponse du serveur ou exit pour sortir:")
            if msg == 'exit':
                break
            nuImage = numpy.asarray(myThread.img)
            #imgencode = cv2.imencode('.png', nuImage)
            #data = numpy.array(imgencode)
            stringData = nuImage.tostring()
            con.send(stringData)
            
            
            
            
# Programme du serveur TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind(('127.0.0.1', 9999))
mythreads = [] 
 
while True: 
    s.listen(5) 
    print("Serveur: en attente de connexions des clients TCP ...")  
    (con, (ip,port)) = s.accept() 
    mythread = myThread(ip,port) 
    mythread.start() 
    mythreads.append(mythread) 
    
    
for t in mythreads: 
    t.join()