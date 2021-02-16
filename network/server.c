#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <string.h>
#include <pthread.h>



#define PORT_INTERNE 1234
#define IP_INTERNE "127.0.0.1"
#define PORT_EXTERNE 5555
#define BUF_SIZE 512
#define NUM_THREADS 1  // #0 interface  Python    
#define DEBUG 1



typedef struct   // struct for one player  
{
    int id;
    int x;
    int y;
    char name[5];

}data_player;


typedef struct 
{
    data_player MyPlayer;       //struct data myplayer
    int numberOtherPlayers;     //number other Player for tab dynamique
    data_player * OtherPlayers; //tab data of all player

}all_data;

typedef struct argument
{
    all_data * data;
    int pythonFD;
    
}argument;

void display_data_player (data_player player){    // fct for help to debug
    printf("=========================\n");
    printf("ID = %i\n",player.id);
    printf("X = %i\n",player.x);
    printf("Y = %i\n",player.y);
    player.name[5]='\0';
    printf("name = %s\n",player.name);
    printf("=========================\n\n");

}


void stop(char *msg)
{
    perror(msg);
    exit(EXIT_FAILURE);
}



/*    // fct de reallocation  
void alloc_OtherPlayer(all_data * data){
    data_player * tmp = realloc(data->OtherPlayers,data->numberOtherPlayers * sizeof(data_player));
    
    if(!tmp){
        free(data->OtherPlayers);
        stop("realloc is null\n");
    }
    else
    {
        data->OtherPlayers=tmp;
    }
    
    
}
*/


void * RecvPython(void * StructArg){

    argument * arg = (argument *) StructArg;
    

    while(1){

        int n = recv((*arg).pythonFD,&((*arg).data->MyPlayer),sizeof(data_player),0);     ///modif pour prendre l'ensemble de la struct myPlayer

        switch (n)
        {
        case -1:
            pthread_exit(NULL);
        
        case 0:
            printf("End connection by peer \n");
            pthread_exit(NULL);
        
        default:
            break;
        }

        if(DEBUG){
            display_data_player((*arg).data->MyPlayer);
            
        }    
    }


}


void * interfacePython(void * Structdata){

    all_data * data = (all_data *) Structdata; 

    int sockfd;// file descriptor for socket

    if( (sockfd=socket(AF_INET,SOCK_STREAM,0))== -1 ) stop("socket");

    struct sockaddr_in serv_addr;
    bzero(&serv_addr, sizeof(serv_addr));
    
    inet_pton(AF_INET, IP_INTERNE, &serv_addr.sin_addr); //set ip address
    serv_addr.sin_family = AF_INET;//set family
    serv_addr.sin_port = htons(PORT_INTERNE);//set port


    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
    {
        close(sockfd);
        stop("bind");
    }

    struct sockaddr_in client_python;
    int len = sizeof(client_python);
    char ip_python[16];

    if(listen(sockfd,1)==-1) stop("listen");

    printf("Start network Interface Python\n");

    int pyhtonFD = accept(sockfd, (struct sockaddr *) &client_python, (socklen_t *)&len );
    inet_ntop(AF_INET,&client_python.sin_addr,ip_python,sizeof(ip_python));

    printf("Interface Python Connected  -->  ip : %s & port : %d\n\n", ip_python, ntohs(client_python.sin_port));

    argument arg;
    arg.data = data;
    arg.pythonFD = pyhtonFD;

    int numberOfThread =1;  
    pthread_t thread_interface[numberOfThread];  // #0 recv python and write MyPlayer     #1 read otherPlayers and send Python 
    

    
    if(pthread_create(&thread_interface[0],NULL,RecvPython,&arg) != 0) stop("thread_send_Python");



    //wait end of all thread
    for(int t =0; t<numberOfThread;t++){
        pthread_join(thread_interface[t],NULL);
    }
    

    close(sockfd);
    close(pyhtonFD);

    pthread_exit(NULL);
}








int main(int argc, char *argv[]){

    if(DEBUG) printf("Size of struct data_player is : %ld \n",sizeof(data_player)); 

    pthread_t threads[NUM_THREADS];   // #0 interface  Python  

    all_data data;

    data.numberOtherPlayers = 0;
    data.OtherPlayers = malloc( data.numberOtherPlayers*sizeof(data_player) );

    
    
    
    if(pthread_create(&threads[0],NULL,interfacePython,&data) != 0) stop("thread_interface_Python");



    //wait end of all thread
    for(int t =0; t<NUM_THREADS;t++){
        pthread_join(threads[t],NULL);

    }

    return EXIT_SUCCESS;
    
}