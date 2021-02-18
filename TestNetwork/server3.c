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

#define SERVER "192.168.15.167"
#define PORT 1234
#define BUFLEN 2048


int positions[2][2] = {{100,100},{0,0}};

void read_pos(char * chaine,int *l){
    int i = 0,k=0;

    while(k < 2){
        int j=0;
        char *chaine2;
        chaine2 = malloc(strlen(chaine)*sizeof(char));
        
        while(chaine[i]!=',' & i < strlen(chaine)){
            chaine2[j] = chaine[i];
            i++;
            j++;
        }
        i++;
        l[k] = atoi(chaine2);
        k++;
    }

}

void make_pos(int *l, char *pos){
    sprintf(pos,"mv%d,%d",l[0],l[1]);
}

int compare(char *msg1, char *msg2){
    int size, identical = 1;
    if(strlen(msg1) < strlen(msg2)) size = strlen(msg1);
    else size = strlen(msg2);

    for(int i=0; i < size ; i++){
        if(msg1[i] != msg2[i]) identical = 0;
    }

    return identical;
}


int main(){
    int sd, newsockfd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char position_ini[BUFLEN]="100,200";

    if ((sd = socket(AF_INET,SOCK_STREAM,0)) == -1){
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    printf("Socket created!\n");

    address.sin_family = AF_INET;
    address.sin_port = htons(PORT);
    if(inet_aton(SERVER, &address.sin_addr) == 0){
        perror("inet aton failed");
        exit(EXIT_FAILURE);
    }

    if (bind(sd, (struct sockaddr *)&address, sizeof(address))<0) 
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
	printf("Listener on port %d \n", PORT);

    if (listen(sd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    printf("Waiting for connections...\n");

    if((newsockfd = accept(sd,(struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0){
        perror("Accept failed");
        exit(EXIT_FAILURE);
    } 
    printf("Connection established\n");

    if(send(newsockfd,position_ini,BUFLEN,0) < 0){
        perror("Send error");
        exit(EXIT_FAILURE);
    }  
    printf("First message sent!\n");

    char position_ini2[BUFLEN]; 
    if(recv(newsockfd,position_ini2,BUFLEN,0) < 0){
        perror("Recv error");
        exit(EXIT_FAILURE);
    }else{
        printf("position initiale:%s\n",position_ini2);
        read_pos(position_ini2,positions[1]);
    }

    int ok = 1;

    while (1){
        char message[BUFLEN]="\0",message_recv[BUFLEN]="\0";
        //strcpy(message,"mv12,140");
        make_pos(positions[0],message);

        if(ok < 3){
        printf("p1:%d p2:%d\n",positions[1][0],positions[1][1]);
        if(send(newsockfd,message,BUFLEN,0) < 0){
            perror("Send error");
            exit(EXIT_FAILURE);
        }
        ok ++;
        }

        bzero(&message_recv,sizeof(message_recv));
        if(recv(newsockfd,message_recv,BUFLEN,0) < 0){
            perror("Recv error");
            exit(EXIT_FAILURE);
        }

        //the host client moved so we are updating his coordinates in the positions' list
        if(compare(message_recv,"mvd")){
            char copy_recv[BUFLEN];

            for(int i = 3; i < strlen(message_recv); i++){
                copy_recv[i-3] = message_recv[i];
            }
            printf("copy: %s\n",copy_recv);
            read_pos(copy_recv,positions[0]);
            printf("p[0]: %d, p[1]: %d\n",positions[0][0],positions[0][1]);
        }

        printf("Message recvd: %s\n",message_recv);
    }

    close(newsockfd);
    close(sd);
    return 0;
}