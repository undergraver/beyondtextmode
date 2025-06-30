Another category of applications are the servers (Apache, NGINX, Tomcat, NodeJS etc). They are the backbone of the Internet applications nowadays and they have a unique way of handling.

Key concepts:
- server - an application that can "serve" multiple clients that connect to it (example: a web server)
- client - an application that connects to a server to obtain information (example: a web browser, curl, wget, postman etc)
- socket - the base element used to represent a type of communication - you can view it like a file descriptor you can write to (send) or read from (receive)
  - in Linux there is no conceptual difference between files and sockets, they are all seen as file descriptors (which are numbers). Common file descriptors are:
    * 0 - standard input (where by default your program reads its input from - think about scanf, getchar etc)
    * 1 - standard output (where by default the program writes messges - think about printf, puts etc) - it is usually the terminal
    * 2 - standard error (where by default the program writes error messages) - it is the terminal

The same concepts apply when we're referring to almost any operating system. In the examples that we have we'll refer to the Linux OS. The way of handling between multiple clients on a server is via the socket API and mainly it boils down to a function called `select`.

Accordin to the `man 3 select` this function does the following:

```
select, pselect, FD_CLR, FD_ISSET, FD_SET, FD_ZERO - synchronous I/O multiplexing
```

It means that from a variety of sources (sockets) this function helps us chose the ones that have something possible to be sent. The socket is the mean through which communication is being made. For more details about sockets:
* https://man7.org/linux/man-pages/man7/socket.7.html
* https://linux.die.net/man/2/socket

We will not cover the network programming topic but the `event loop` and where its place is in server applications. We ask, of course, chatgpt for an example to do this:

`show me a select example of a server who listens on port 1234 and sends "bye" string to all connected clients. show me also a client code C++ code`

Server code:
```
#include <iostream>
#include <cstring>
#include <vector>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <sys/select.h>

#define PORT 1234
#define BUFFER_SIZE 1024

int main() {
    int listener = socket(AF_INET, SOCK_STREAM, 0);
    if (listener < 0) {
        perror("socket");
        return 1;
    }

    int opt = 1;
    setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);

    if (bind(listener, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        return 1;
    }

    if (listen(listener, SOMAXCONN) < 0) {
        perror("listen");
        return 1;
    }

    std::cout << "Server listening on port " << PORT << "...\n";

    fd_set master_set, read_fds;
    FD_ZERO(&master_set);
    FD_SET(listener, &master_set);
    int fd_max = listener;

    while (true) {
        read_fds = master_set;

        if (select(fd_max + 1, &read_fds, nullptr, nullptr, nullptr) < 0) {
            perror("select");
            break;
        }

        for (int i = 0; i <= fd_max; ++i) {
            if (FD_ISSET(i, &read_fds)) {
                if (i == listener) {
                    // New connection
                    sockaddr_in client_addr;
                    socklen_t client_len = sizeof(client_addr);
                    int client_fd = accept(listener, (struct sockaddr*)&client_addr, &client_len);
                    if (client_fd >= 0) {
                        FD_SET(client_fd, &master_set);
                        if (client_fd > fd_max) fd_max = client_fd;
                        std::cout << "New client connected: FD " << client_fd << "\n";
                    }
                } else {
                    // Handle existing client
                    const char* msg = "bye";
                    send(i, msg, strlen(msg), 0);
                    close(i);
                    FD_CLR(i, &master_set);
                    std::cout << "Sent 'bye' to client FD " << i << " and closed connection.\n";
                }
            }
        }
    }

    close(listener);
    return 0;
}

```

Client code:
```
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 1234
#define BUFFER_SIZE 1024

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        return 1;
    }

    char buffer[BUFFER_SIZE];
    ssize_t bytes_received = recv(sock, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received > 0) {
        buffer[bytes_received] = '\0';
        std::cout << "Received from server: " << buffer << "\n";
    }

    close(sock);
    return 0;
}

```

The client is not something very complex as it only has a simple flow. The most important part is the server code which in its main loop has something like this:
```
    while (true) {
        read_fds = master_set;

        if (select(fd_max + 1, &read_fds, nullptr, nullptr, nullptr) < 0) {
            perror("select");
            break;
        }

        for (int i = 0; i <= fd_max; ++i) {
            if (FD_ISSET(i, &read_fds)) {
                if (i == listener) {
                // handle incoming data - for the server it means new connection
                }
                else {
                // handle clients - basically send them "Bye" and close connection (socket)
                }
             }
        } // for 
    } // while
```

This is a normal flow of a single threaded server that can handle multiple clients. All is controlled in the same place, all events happen in the same place and the select demultiplexer helps us choose and handle the events that are happening.

This is a very important concept because, as we'll see other frameworks abtract this and we really need to understand properly what are the implications as for some particular cases we might need to tweak the properties of specific sockets to improve performance.

This is really, really important as this type of workflow is very much seen in various applications and online services.

# Networking via a framework

The same example now is made with a framework called ACE which provides some cross platform abstractions and also some nice design patterns when it comes to network communication, namely the ACE_Reactor which we'll use in the following example.

Server code:
```
#include "ace/Reactor.h"
#include "ace/SOCK_Acceptor.h"
#include "ace/SOCK_Stream.h"
#include "ace/INET_Addr.h"
#include "ace/Event_Handler.h"
#include "ace/Log_Msg.h"

#define PORT 1234

class ClientHandler : public ACE_Event_Handler {
public:
    ClientHandler(ACE_SOCK_Stream stream) : stream_(stream) {
        this->reactor(ACE_Reactor::instance());
    }

    virtual ACE_HANDLE get_handle() const {
        return stream_.get_handle();
    }

    virtual int handle_output(ACE_HANDLE = ACE_INVALID_HANDLE) {
        const char *msg = "bye";
        stream_.send_n(msg, ACE_OS::strlen(msg));
        stream_.close_writer();
        return -1;  // Done with this handler
    }

    virtual int handle_input(ACE_HANDLE = ACE_INVALID_HANDLE) {
        return handle_output();  // On input, just send "bye"
    }

    virtual int handle_close(ACE_HANDLE, ACE_Reactor_Mask) {
        stream_.close();
        delete this;
        return 0;
    }

private:
    ACE_SOCK_Stream stream_;
};

class Acceptor : public ACE_Event_Handler {
public:
    Acceptor(ACE_INET_Addr &addr) {
        if (acceptor_.open(addr) == -1)
            ACE_ERROR((LM_ERROR, ACE_TEXT("Failed to open acceptor\n")));
        this->reactor(ACE_Reactor::instance());
    }

    virtual ACE_HANDLE get_handle() const {
        return acceptor_.get_handle();
    }

    virtual int handle_input(ACE_HANDLE) {
        ACE_SOCK_Stream client_stream;
        if (acceptor_.accept(client_stream) == -1) {
            ACE_ERROR_RETURN((LM_ERROR, ACE_TEXT("Failed to accept connection\n")), -1);
        }

        ClientHandler *handler = new ClientHandler(client_stream);
        ACE_Reactor::instance()->register_handler(handler, ACE_Event_Handler::READ_MASK);
        return 0;
    }

private:
    ACE_SOCK_Acceptor acceptor_;
};

int main() {
    ACE_INET_Addr addr(PORT);
    Acceptor acceptor(addr);

    ACE_Reactor::instance()->register_handler(&acceptor, ACE_Event_Handler::ACCEPT_MASK);

    ACE_DEBUG((LM_DEBUG, "Reactor server listening on port %d\n", PORT));
    ACE_Reactor::instance()->run_reactor_event_loop();
    return 0;
}

```

Client code:
```
#include "ace/SOCK_Connector.h"
#include "ace/SOCK_Stream.h"
#include "ace/INET_Addr.h"
#include "ace/Log_Msg.h"

#define PORT 1234

int main() {
    ACE_INET_Addr server_addr(PORT, ACE_LOCALHOST);
    ACE_SOCK_Connector connector;
    ACE_SOCK_Stream stream;

    if (connector.connect(stream, server_addr) == -1) {
        ACE_ERROR_RETURN((LM_ERROR, ACE_TEXT("%p\n"), ACE_TEXT("connect")), 1);
    }

    char buffer[128];
    ssize_t recv_len = stream.recv(buffer, sizeof(buffer) - 1);
    if (recv_len > 0) {
        buffer[recv_len] = '\0';
        ACE_DEBUG((LM_DEBUG, ACE_TEXT("Received: %C\n"), buffer));
    }

    stream.close();
    return 0;
}

```

The most important thing is that the framework has abstracted the weird `select` calls into a framework which is simply invoke via this small code sequence:

```
int main() {
    ACE_INET_Addr addr(PORT);
    Acceptor acceptor(addr);

    ACE_Reactor::instance()->register_handler(&acceptor, ACE_Event_Handler::ACCEPT_MASK);

    ACE_DEBUG((LM_DEBUG, "Reactor server listening on port %d\n", PORT));
    ACE_Reactor::instance()->run_reactor_event_loop();
    return 0;
}
```

so that `run_reactor_event_loop` is actually doing something similar to our `select` in the previous server example. The only difference here is that we need to comply with the `ACE_Reactor`'s demands, namely the fact that it only works with `ACE_Event_Handler ` object.

This means our server will become a class instance that is registered in the reactor. We don't need to do anything but override the virtual methods `handle_input` in order to accept connections (remember that `select` also notified the server that there is input data when a connection was trying to be established.

So we are talking about the same concept but encapsulated in an `ACE_Event_Handler` class which makes it clearer as all events related to the function are handled in this fashion.

As you can see with this framework it is very similar to the wxWidgets example where we no longer see the `GetMessage` loop but instead of that we simply see a call to `MainLoop`
```
app = MyApp(False)
app.MainLoop()  
```

That could be seen as the main difference between writing your code and using a framework:

* you leverage the framework
* you lose the ability to control the low level details

This is not a good or bad thing as it depends on each application's needs.

For more information about ACE: 
* https://github.com/DOCGroup/ACE_TAO
* https://www.dre.vanderbilt.edu/~schmidt/ACE.html - see the books as they contain advanced networking concepts and a lot of valuable information
