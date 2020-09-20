# DS Lab 6 (Client)
# Student: Marko Pezer

# Import libraries
import sys
import socket
import os.path

# Set buffer size
BUFFER_SIZE = 1024

# Check arguments sent from terminal
if len(sys.argv) != 4:
        print('Usage:', sys.argv[0], 'file domain-name|ip-address port-number')
        sys.exit(1)

# Copy argv to variables 
filename, host, port = sys.argv[1:]

# Check if port is integer
try:
        port = int(port)
except:
        print('Port number must be an integer.')
        sys.exit(1)

# Check if file exist
if not os.path.isfile(filename):
        print(filename, 'does not exist.')
        sys.exit(1)

# Connect to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # Coonect
        s.connect((host, port))

        # Send filename
        s.send(os.path.basename(filename).encode())
        
        # Get saved name in server
        name_saved = s.recv(1024).decode()

        # Send file
        with open(filename, 'rb') as fs:
                
                # Set size of filename
                size = os.path.getsize(filename)
                
                # Check columns
                _, columns = os.popen('stty size', 'r').read().split()
                columns = int(columns)
                if int(columns) > 10 else 94
                
                # Initialize count to be zero
                count = 0
                
                while True:
                        
                        # Read buffer size to data and check if there is data
                        data = fs.read(BUFFER_SIZE)
                        if not data:
                            break

                        # Send data
                        s.sendall(data)

                        # Calculate progress
                        count = count + 1
                        progress = count * BUFFER_SIZE / size
                        fill_length = round(progress * (columns - 10))
                        space_length = columns - 10 - fill_length
                        
                        # Print progress
                        if progress < 1:
                                print('%s>%s %3d%%' % ('=' * fill_length, ' ' * space_length, round(progress * 100)), end='\r')
                        else:
                                print('%s  100%%' % ('=' * (columns - 10)))
                                break
                
                # Close fs
                fs.close()
        
        # Print action
        print('Uploaded', filename, 'with name', repr(name_saved))
