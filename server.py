# DS Lab 6 (Client)
# Student: Marko Pezer

# SERVER

# Import libraries
import socket
import glob
import re
import os
from threading import Thread

# Array of clients
clients = []

# Thread to listen one client
class ClientListener(Thread):
    
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon = True)
        self.sock = sock
        self.name = name

    # Disconnect client
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        # Print that client is disconnected
        print(self.name + ' disconnected')
    
    # Run
    def run(self):
      
        # Get filename
        fullname = self.sock.recv(1024).decode()

        # Check for duplicates
        name, extension = os.path.splitext(fullname)
        names = glob.glob(name + '*' + extension)
        
        # Check if there are files with the same name
        if len(names) >= 1:
            
            # Count number of files with same name
            numbers = [int(s) for name in names for s in re.findall(r'\d+', os.path.splitext(name)[0])]
            number = max(numbers) if len(numbers) else 0 
            number = number + 1
            
            # Create new name in format [name]_copy[number_of_copy].[extension]
            fullname = name + '_copy' + str(number) + extension
        
        # Open new file
        with open(fullname, 'wb') as fs:
            # Send file name to the client
            self.sock.send(fullname.encode())

            # Write file
            while True:
                # Try to read 1024 bytes from user
                data = self.sock.recv(1024)
                
                if data:
                    fs.write(data)
                else:
                    # If we got no data client has disconnected
                    fs.close()
                    # Print that file is saved
                    print(self.name, 'saved', fullname)
                    self._close()
                    # Finish the thread
                    return

# Main function
def main():
  
    # Next name
    next_name = 1

    # AF_INET – IPv4, SOCK_STREAM – TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Listen to all interfaces at 65123 port
    sock.bind(('', 65123))
    sock.listen()
    
    # Print listening message
    print('Listening on port 65123...')
    
    while True:
        # Bloc call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        # Increase new name
        next_name = next_name + 1
        # Print message
        print(str(addr) + ' connected as ' + name)
        # Start new thread to deal with client
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
    
# Source: https://gist.github.com/gordinmitya/349f4abdc6b16dc163fa39b55544fd34
