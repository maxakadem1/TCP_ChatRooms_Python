## TCP_ChatRooms_Python
#Python chat rooms application using TCP for local connections

1. Open command line/power shell (at least 2 windows)

2. Use command line and write “python3 server.py” for a server launch.
Server will launch on host 127.0.0.1 and port of 4073

3. Use another command line to write “python3 client.py NICKNAME
ROOMNAMEE”. NICKNAME is your nickname. ROOMNAME is a name of
a room that you want to connect to. If room with ROOMNAME does
not exist, it will create a room with that name.

4. You can connect any number of clients to a server using separate
command lines.

5. Commands available are shown on launch of a client. Commands
include <room> <roomlist> <commands> <join ROOMNAME>
===================================================
You can connect as many users to a server as you would like. There is a
max capacity of 5 users per room. When users join another room, he is
automatically leaving the previous room.
