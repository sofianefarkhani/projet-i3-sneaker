import socket 
 
msg = input("ClientB : Entrez un message ou exit pour sortir:") 
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(("127.0.0.1", 9999))
while msg != 'exit':
    s.send(msg)     
    data = s.recv(2000)
    print("ClientB a reçu des données:", data)
    msg = input("Entrez un message pour continuer ou exit pour sortir:")
s.close()