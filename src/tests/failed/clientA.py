import socket 
import cv2

msg = input("ClientA: Entrez un message ou exit pour sortir:") 




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(("127.0.0.1", 9999))
while msg != 'exit':
    #s.send(bytes(msg)) 
    s.sendto(msg.encode(),("127.0.0.1", 9999))    
    data = s.recv(2000)
    print("ClientA a reçu des données:", data)
    msg = input("Entrez un message pour continuer ou exit pour sortir:")
    
    
s.close()