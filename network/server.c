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
#define NUM_THREADS 2  // #0 interface  Python   #1 server Peer2Peer   
#define DEBUG 1



typedef struct   // struct for one player  
{
    int id;   //essential element 
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
    int sockfd;
    char * ip;
    
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

        int n = recv((*arg).sockfd,&((*arg).data->MyPlayer),sizeof(data_player),0);     ///modif pour prendre l'ensemble de la struct myPlayer

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


void * SendPython(void * StructArg){

    argument * arg = (argument *) StructArg;
    
    while(1){

        for(int i = 0; i<(*arg).data->numberOtherPlayers; i++){
            int n = send((*arg).sockfd,&((*arg).data->OtherPlayers[i]),sizeof(data_player),0);

            if(n==-1){
                printf("problem with send python");
                pthread_exit(NULL);
            }
        }

    }

    pthread_exit(NULL);

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
    arg.sockfd = pyhtonFD;

    int numberOfThread =2;  
    pthread_t thread_interface[numberOfThread];  // #0 recv python and write MyPlayer     #1 read otherPlayers and send Python 
    

    
    if(pthread_create(&thread_interface[0],NULL,RecvPython,&arg) != 0) stop("thread_recv_Python");
    if(pthread_create(&thread_interface[1],NULL,SendPython,&arg) != 0) stop("thread_send_Python");



    //wait end of all thread
    for(int t =0; t<numberOfThread;t++){
        pthread_join(thread_interface[t],NULL);
    }
    

    close(sockfd);
    close(pyhtonFD);

    pthread_exit(NULL);
}







void * RecevStuctOneOtherPlayer(void * StructArg){

    argument * arg = (argument *) StructArg;
    data_player new_player;
    int First = 1;
    int MyID; 

    while(1){

        int n = recv((*arg).sockfd,&new_player,sizeof(data_player),0);     

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

        if(First){
            MyID = new_player.id;
            First =0;

            for (int i=0; i<(*arg).data->numberOtherPlayers; i++){
                if((*arg).data->OtherPlayers[i].id == 0){
                    memcpy(&((*arg).data->OtherPlayers[i]),&new_player,sizeof(data_player));
                    break;
                }
            }

        }
        else
        {
            for (int i=0; i<(*arg).data->numberOtherPlayers; i++){
                if((*arg).data->OtherPlayers[i].id == MyID){
                    memcpy(&((*arg).data->OtherPlayers[i]),&new_player,sizeof(data_player));
                    break;
                }
            }
        }
        

    }
    
    pthread_exit(NULL);

    

}

void * SendSructMyPlayer(void * StructArg){

    argument * arg = (argument *) StructArg;
    char * IPserver;
    IPserver = malloc(16 *sizeof(char));

    strcpy(IPserver,(*arg).ip);

    int sockfd = socket(AF_INET,SOCK_STREAM,0);
    if (sockfd == -1) pthread_exit(NULL);

    struct sockaddr_in serv_OtherPlayer;
    int len=sizeof(serv_OtherPlayer);

    bzero(&serv_OtherPlayer,sizeof(serv_OtherPlayer));
    serv_OtherPlayer.sin_family =AF_INET;
    inet_aton(IPserver,&serv_OtherPlayer.sin_addr);
    serv_OtherPlayer.sin_port = htons(PORT_EXTERNE);

    if (connect(sockfd, (const struct sockaddr *) &serv_OtherPlayer, (socklen_t )len) < 0 ) pthread_exit(NULL);

    int init = 0; // it's not init connection
    send(sockfd,&init,sizeof(int),0);

 
    while(1){
        send(sockfd,&((*arg).data->MyPlayer),sizeof(data_player),0 );
    }


    pthread_exit(NULL);

}


void * serverPeer(void * StrucData){

    all_data * data = (all_data *) StrucData;
    int enable =1;

    int  main_sockfd;// file descriptor for listening socket

    if( (main_sockfd=socket(AF_INET,SOCK_STREAM,0))== -1 ) stop("socket");

    if( setsockopt(main_sockfd, SOL_SOCKET, SO_REUSEADDR, (char *)&enable, sizeof(enable)) < 0 ){
        pthread_exit(NULL);
    }
    

    struct sockaddr_in serv_addr;
    bzero(&serv_addr, sizeof(serv_addr));
    
    inet_pton(AF_INET, INADDR_ANY, &serv_addr.sin_addr); //accept all ip with INADDR_ANY
    serv_addr.sin_family = AF_INET;//set family
    serv_addr.sin_port = htons(PORT_EXTERNE);//set port


    if (bind(main_sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
    {
        close(main_sockfd);
        stop("bind");
    }

    struct sockaddr_in OtherServer;
    int len = sizeof(OtherServer);
    char ip_OtherServer[16];
   

    if(listen(main_sockfd,5) == -1) stop("listen");

    printf("Start network Server Peer2peer\n");


    int numberOfThread =0;
    pthread_t * thread_server;  // #1 recv struct data_player(Otherplayer) and add on data     #0  create new connection with other server ans send MyPlayer

    while(1){
        int new_playerFD = accept(main_sockfd, (struct sockaddr * ) &OtherServer, (socklen_t *) &len);
        inet_ntop(AF_INET,&OtherServer.sin_addr,ip_OtherServer,sizeof(ip_OtherServer));

        printf("New player is connected -->  ip : %s & port : %d\n\n",ip_OtherServer,ntohs(OtherServer.sin_port));

        int init;
        int n = recv(new_playerFD,&init,sizeof(int),0);     

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

        

        data->numberOtherPlayers++;

        //init new size de Otherplayer 
        (*data).OtherPlayers = malloc( (*data).numberOtherPlayers*sizeof(data_player) );
        bzero(&((*data).OtherPlayers[(data->numberOtherPlayers)-1]),sizeof(data_player));

        argument arg;
        arg.ip = malloc(16*sizeof(char));
        arg.data = data;
        arg.sockfd = new_playerFD;
        strcpy(arg.ip,ip_OtherServer);

        
        if(init){
            numberOfThread =numberOfThread + 2;
        }
        else
        {
            numberOfThread++;
        }
        


        thread_server =malloc(numberOfThread * sizeof(pthread_t));

        if(pthread_create(&thread_server[numberOfThread-1],NULL,RecevStuctOneOtherPlayer,&arg) != 0) stop("thread_recv_one_other_player");
        
        if(init){
            if(pthread_create(&thread_server[numberOfThread-2],NULL,SendSructMyPlayer,&arg) != 0) stop("thread_send_my_player");
        }



    }

    //wait end of all thread
    for(int t =0; t<numberOfThread;t++){
        pthread_join(thread_server[t],NULL);
    }

    pthread_exit(NULL);

}







int main(int argc, char *argv[]){

    if(DEBUG) printf("Size of struct data_player is : %ld \n",sizeof(data_player)); 

    pthread_t threads[NUM_THREADS];   // #0 interface  Python  #1 server Peer2Peer 

    all_data data;

    data.numberOtherPlayers = 0;
    data.OtherPlayers = malloc( data.numberOtherPlayers*sizeof(data_player) );

/* test for  fct sendPython
    for (int i =0; i<data.numberOtherPlayers;i++){
        data.OtherPlayers[i].id=i+1;
    }
 */   

    
    if(pthread_create(&threads[0],NULL,interfacePython,&data) != 0) stop("thread_interface_Python");
    if(pthread_create(&threads[1],NULL,serverPeer,&data) != 0) stop("thread_Server_PeerToPeer");



    //wait end of all thread
    for(int t =0; t<NUM_THREADS;t++){
        pthread_join(threads[t],NULL);

    }

    return EXIT_SUCCESS;
    
}