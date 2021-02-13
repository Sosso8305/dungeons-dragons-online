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

#define SERVER "192.168.15.165"
#define PORT 5555
#define BUFLEN 2048


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
    sprintf(pos,"%d,%d",l[0],l[1]);
}

void *threaded_client(void *arg){
    char reply[BUFLEN]="\0", message[BUFLEN];
    int *liste = (int *)arg;
    int sockfd = liste[0];
    int n = liste[1];
    int position[2][2]={{liste[2],liste[3]},{liste[4],liste[5]}};

    bzero(&message,sizeof(message));
    make_pos(position[n],message);
    printf("message %s\n",message);

    if (send(sockfd, message,BUFLEN,0) < 0){
        perror("erreur send()\n");
        exit(EXIT_FAILURE);
    }
    printf("Sent!\n");

    while(1){
        bzero(&message,sizeof(message));

        if(recv(sockfd, message,BUFLEN,0) < 0){
            printf("Disconnected\n");
            break;
        }

        bzero(&position[n],sizeof(position[n]));
        read_pos(message,position[n]);

        // if(strcmp(message,"\0") == 0){
        //     printf("Disconnected\n");
        //     break;
        // }

        if(n==1){
            bzero(&reply,sizeof(reply));
            make_pos(position[0],reply);
        }
        else{
            bzero(&reply,sizeof(reply));
            make_pos(position[1],reply);
        }

        printf("Received: %s\n",message);
        printf("Sending: %s\n",reply);

        if (send(sockfd, reply,BUFLEN,0) < 0){
            perror("erreur send()\n");
            exit(EXIT_FAILURE);
        }
    }
    printf("Lost connection\n");
    close(sockfd);
}


int main(){
    int master_socket,player_n=0;
    struct sockaddr_in address;
    int position0[2] = {0,0},position1[2] ={100,100};

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
        char message[BUFLEN];

        bzero((char *)&cliaddr, sizeof(cliaddr));
        if((newsockfd = accept(master_socket, (struct sockaddr *)&cliaddr, (socklen_t *) &clilen)) < 0){
            perror("new socket error\n");
            exit(EXIT_FAILURE);
        }
        printf("Accept done!\n");
        //send(newsockfd,message,BUFLEN,0);

        pthread_t newthread;
        int args[6]={newsockfd,player_n,position0[0],position0[1],position1[0],position1[1]};
        pthread_create(&newthread, NULL, threaded_client, args);
        pthread_join(newthread,NULL);
        player_n++;
    }

    return EXIT_SUCCESS;
}