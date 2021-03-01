CC	=	gcc 
CFLAGS	=  	-Wall
CFLAGS  +=      -D_GNU_SOURCE
CFLAGS  += 	-g
CFLAGS  += -pthread

CIBLES	=	interface client_dev

all: $(CIBLES) server

server: server.o 
	$(CC) -o server server.o $(CFLAGS)

server.o: server.c server.h
	$(CC) -o server.o -c server.c  $(CFLAGS)

clean: 
	$(RM) -f core *.o $(CIBLES) *~
	rm server