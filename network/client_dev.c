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

typedef struct   // struct for one player  
{
    int id;
    int x;
    int y;
    char name[5];

}data_player;





int main(int argc, char const *argv[])
{
    char buff[BUFSIZ];
    //char name[NAMESIZE];
    int END = 0;
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) stop("socket",sockfd);
    struct sockaddr_in serv_addr;
    int len=sizeof(serv_addr);

    bzero(&serv_addr,sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
    inet_aton(SERVER,&serv_addr.sin_addr);
    serv_addr.sin_port = htons(PORT);
    
   
    if (connect(sockfd,(const struct sockaddr *)&serv_addr,(socklen_t )len) < 0) stop("Connect",sockfd);

    // printf("Name (max %d lettre):",NAMESIZE-1);
    // fflush(stdout);
    // scanf("%[^\n]",name);
    // fgetc( stdin );

    data_player player ={1,50,70,"toto"};



while(1){
    printf("Msg a envoyé :");
    fflush(stdout);
    scanf("%[^\n]",buff);
    send(sockfd,&player,sizeof(data_player),0);
    fgetc( stdin );


    // int n =recv(sockfd,buff,BUFSIZ,0);
    // if (n == -1)  stop("recv",sockfd);
    // buff[n]='\0';
    // printf("Server : %s \n",buff);
    isEnd(buff,&END);

    if (END == 1) break;

}
    close(sockfd);

    return 0;
}