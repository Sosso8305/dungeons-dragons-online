#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>


#define SERVER "127.0.0.1"
#define PORT 1234
#define BUFSIZE  512
#define NAMESIZE 10

void isEnd(char *msg, int * END){
    if(strcmp(msg,"exit") == 0){
        printf("[%d] End connection \n",getpid());
        *END = 1;
    }
    

}

void stop(char* msg,int FD){
	perror(msg);
    close(FD);
	exit(EXIT_FAILURE);
	
}
#define SIZE_DATA_PY 20

typedef struct   // struct for one player  
{
    int id;   //essential element 
    char dataPython[SIZE_DATA_PY];

}data_player;

void display_data_player (data_player player){    // fct for help to debug
    printf("=========================\n");
    //printf("ID = %i\n",player.id);
    player.dataPython[SIZE_DATA_PY]='\0';
    printf("Data = %s\n",player.dataPython);
    printf("=========================\n\n");

}





int main(int argc, char const *argv[])
{
    
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) stop("socket",sockfd);
    struct sockaddr_in serv_addr;
    int len=sizeof(serv_addr);

    bzero(&serv_addr,sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
    inet_aton(SERVER,&serv_addr.sin_addr);
    serv_addr.sin_port = htons(PORT);
    
   
    if (connect(sockfd,(const struct sockaddr *)&serv_addr,(socklen_t )len) < 0) stop("Connect",sockfd);

 

    data_player player ={0,"sosso"};


    if(fork() == 0){

        while (1)
        {   
            sleep(1);
            send(sockfd,&player.dataPython,sizeof(char)*SIZE_DATA_PY,0);
        }
        

    }
    else
    {
        while (1)
        {
            data_player recvPlayer;
        int n =recv(sockfd,&recvPlayer.dataPython,sizeof(char)*SIZE_DATA_PY,0);
        if (n == -1)  stop("recv",sockfd);

        display_data_player(recvPlayer);
        }
        
        
    }
    

    close(sockfd);

    return 0;
}