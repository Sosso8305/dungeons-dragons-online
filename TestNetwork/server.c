#include <stdio.h>
#include <string.h>  
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>   
#include <arpa/inet.h>   
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h>
#include <sys/stat.h> 
#include <fcntl.h> 
#include <pthread.h>

#define SERVER "192.168.15.162"
#define PORT 5555
#define BUFLEN 2048


void *threaded_client(void *arg){
    char reply[BUFLEN]="\0", message[BUFLEN]="Connected";
    int *sockfd = (int *) arg;


    if (send(*sockfd, message,BUFLEN,0) < 0){
        perror("erreur send()\n");
        exit(EXIT_FAILURE);
    }
    printf("Sent!\n");

    while(1){
        bzero(&message,sizeof(message));

        if(recv(*sockfd, message,BUFLEN,0) < 0){
            printf("Disconnected\n");
            break;
        }

        // if(strcmp(message,"\0") == 0){
        //     printf("Disconnected\n");
        //     break;
        // }

        bzero(&reply,sizeof(reply));
        strcpy(reply,message);

        printf("Received: %s\n",reply);
        printf("Sending: %s\n",reply);

        if (send(*sockfd, reply,BUFLEN,0) < 0){
            perror("erreur send()\n");
            exit(EXIT_FAILURE);
        }
    }
    printf("Lost connection\n");
    close(*sockfd);
}


int main(){
    int master_socket;
    struct sockaddr_in address;

    if( (master_socket = socket(AF_INET , SOCK_STREAM , 0)) == -1) 
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
    printf("Socket created\n");

    address.sin_family = AF_INET;
    address.sin_port = htons( PORT );
    if(inet_aton(SERVER, &address.sin_addr) == 0){
        perror("inet aton failed");
        exit(EXIT_FAILURE);
    }

    if (bind(master_socket, (struct sockaddr *)&address, sizeof(address))<0) 
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
	printf("Listener on port %d \n", PORT);

    if (listen(master_socket, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    printf("Waiting for connections...\n");

    while(1){
        struct sockaddr_in cliaddr;
        int newmaster_socket,clilen=sizeof(cliaddr),newsockfd;
        char message[BUFLEN]="Welcome";

        bzero((char *)&cliaddr, sizeof(cliaddr));
        if((newsockfd = accept(master_socket, (struct sockaddr *)&cliaddr, (socklen_t *) &clilen)) < 0){
            perror("new socket error\n");
            exit(EXIT_FAILURE);
        }
        printf("Accept done!\n");
        send(newsockfd,message,BUFLEN,0);

        pthread_t newthread;
        pthread_create(&newthread, NULL, threaded_client, &newsockfd);
        pthread_join(newthread,NULL);
    }

    return EXIT_SUCCESS;
}