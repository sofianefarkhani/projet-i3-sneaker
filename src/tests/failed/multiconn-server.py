# see https://realpython.com/python-sockets/

import selectors # module for efficient I/O multiplexing
import socket
import types

sel = selectors.DefaultSelector()

host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 65432        # Port to listen on (non-privileged ports are > 1023)


#SET UP THE LISTENING SOCKET
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
lsock.bind((host, port))                                    # give the socket a port and address
lsock.listen()                                              # give it the mission to wait and retrieve data from this port
print('listening on', (host, port))
lsock.setblocking(False)                                    # configure the socket in non-blocking mode (will not temporarily suspends the application when waiting for return value)
sel.register(lsock, selectors.EVENT_READ, data=None)        # register the socket to be monitored with sel.select(). Will only react to read events.



def accept_wrapper(sock): 
    '''How to accept a connexion without stalling the server in case heavy operations need to happen.'''
    connexion, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    connexion.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')  # ready some spaces to store data whenever the sockets communicate
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(connexion, events, data=data)

def service_connection(key, mask):
    '''What to do when a client connexion is ready'''
    sock = key.fileobj      
    data = key.data  
           
    if mask & selectors.EVENT_READ: # -> Then the socket is ready for reading
        recv_data = sock.recv(1024)  # -> we then recieve the data
        if recv_data:
            data.outb += recv_data      # Any data that’s read is appended to data.outb
        else: # -> then the client has closed their socket, so the server should too
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
            
    if mask & selectors.EVENT_WRITE: # -> Then the socket is ready for writing (sending data)
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # -> we send data to the adress of the socket.
            data.outb = data.outb[sent:] # -> We remove the bytes sent from the send buffer


while True:
    events = sel.select(timeout=None)       # blocks until there are sockets ready for I/O.
    for key, mask in events:                # key: SelectorKey, contains:
                                                # -> key.fileobj is the socket object
                                                # -> key.mask is an event mask of the operations that are ready.
                                                
        if key.data is None:    # then it’s from the listening socket (because its the only one which sends nothing) and we need to accept() the connection.
            accept_wrapper(key.fileobj)
        else:                   # its from a client socket, we need to give them something.       
            service_connection(key, mask)