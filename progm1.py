import sys
import socket
import threading
import time

QUIT = False

class ClientThread( threading.Thread ):
    # Class that implements the client threads in this server

    def __init__( self, client_sock ):
        super().__init__()
        self.client = client_sock
        self.name = "Server of Grace Ryoo"

        # Initialize the object, save the socket that this thread will use.

    def run( self ):
        ''' 
        Thread's main loop. Once this function returns, the thread is finished 
        and dies. 
        '''

        #
        # Need to declare QUIT as global, since the method can change it
        #
        global QUIT
        done = False
        cmd = self.readline()
        #
        # Read data from the socket and process it
        #
        while not done:
            if 'quit' == cmd :
                self.writeline( 'Ok, bye' )
                QUIT = True
                done = True
            elif 'bye' == cmd:
                self.writeline( 'Ok, bye' )
                done = True
            else:
                self.writeline( self.name )
            
            cmd = self.readline()

        #
        # Make sure the socket is closed once we're done with it
        #
        self.client.close()
        return

    def readline( self ):
        ''' 
        Helper function, reads up to 1024 chars from the socket, and returns 
        them as a string, all letters in lowercase, and without any end of line 
        markers '''
        try:
            result = self.client.recv( 1024 )
            if( result ):
                result = result.strip().lower()
        except Exception:
            return ""
        return ""

    def writeline( self, text ):
        ''' 
        Helper function, writes teh given string to the socket, with an end of 
        line marker appended at the end 
        '''
        try:
            self.client.send(( text.strip() + '\n' ).encode())
        except Exception:
            pass

class Server:
    ''' 
    Server class. Opens up a socket and listens for incoming connections.
    Every time a new connection arrives, it creates a new ClientThread thread
    object and defers the processing of the connection to it. 
    '''

    def __init__( self ):
        self.sock = None
        self.thread_list = []

    def run( self ):
        '''
        Server main loop. 
        Creates the server (incoming) socket, and listens on it of incoming
        connections. Once an incomming connection is deteceted, creates a 
        ClientThread to handle it, and goes back to listening mode.
        '''
        global QUIT
        all_good = False
        try_count = 0

        #
        # Attempt to open the socket
        #
        while not all_good:
            if 3 < try_count:
                #
                # Tried more than 3 times, without success... Maybe the port
                # is in use by another program
                #
                sys.exit( 1 )
            try:
                #
                # Create the socket
                #
                self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
                #
                # Bind it to the interface and port we want to listen on
                #
                self.sock.bind( ( '127.0.0.1', 5050 ) )
                #
                # Listen for incoming connections. This server can handle up to
                # 5 simultaneous connections
                #
                self.sock.listen( 5 )
                all_good = True
                break
            except socket.error as err:
                #
                # Could not bind on the interface and port, wait for 10 seconds
                #
                print ('Socket connection error... Waiting 10 seconds to retry.')
                time.sleep( 10 )
                try_count += 1

        print("Server is listening on port 5050.")
        print("Try: telnet localhost 5050")

        try:
            #
            # NOTE - No need to declare QUIT as global, since the method never 
            #    changes its value
            #
            while not QUIT:
                try:
                    #
                    # Wait for half a second for incoming connections
                    #
                    self.sock.settimeout( 0.500 )
                    client, _ = self.sock.accept()
                except socket.timeout:
                    #
                    # No connection detected, sleep for one second, then check
                    # if the global QUIT flag has been set
                    #
                    time.sleep( 1 )
                    if QUIT:
                        print ("Received quit command. Shutting down...")
                        break
                    continue
                #
                # Create the ClientThread object and let it handle the incoming
                # connection
                #
                new_thread = ClientThread( client )
                print (f"Incoming Connection. Started thread {new_thread.getName()}")
                self.thread_list.append(new_thread)
                new_thread.start()

                self.thread_list = [t for t in self.thread_list if t.is_alive()]

        except KeyboardInterrupt:
            print ("Ctrl+C pressed... Shutting Down")
        except Exception as err:
            print (f"Exception caught: {err}\nClosing...")

        #
        # Clear the list of threads, giving each thread 1 second to finish
        # NOTE: There is no guarantee that the thread has finished in the
        #    given time. You should always check if the thread isAlive() after
        #    calling join() with a timeout paramenter to detect if the thread
        #    did finish in the requested time
        #
        for thread in self.thread_list:
            thread.join( 1.0 )
        #
        # Close the socket once we're done with it
        #
        self.sock.close()

if "__main__" == __name__:
    server = Server()
    server.run()
    print ("Terminated")
