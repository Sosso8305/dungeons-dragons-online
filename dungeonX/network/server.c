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
#include "server.h"

#define DEFAUT_PORT_INTERNE 5133
#define IP_INTERNE "127.0.0.1"
#define DEFAUT_PORT_EXTERNE 5555
#define NUM_THREADS 3 // #0 interface  Python   #1 server Peer2Peer   #3 init to other server
#define DEBUG 0

void display_data_player(data_player player)
{ // fct for help to debug
    printf("=========================\n");
    printf("ID = %i\n", player.id);
    player.dataPython[SIZE_DATA_PY] = '\0';
    printf("name = %s\n", player.dataPython);
    printf("=========================\n\n");
}

void display_socket(socketBSD sock){
    printf("## IP--> %s     port--> %i ## \n",sock.ip,sock.port);
}

void stop(char *msg)
{
    perror(msg);
    exit(EXIT_FAILURE);
}

void sendSocketPlayerInNetwork(int sockfd,all_data * data){

    int numberPlayer = (*data).numberOtherPlayers;
    send(sockfd,&numberPlayer,sizeof(int),0);

    for (int i=0;i< numberPlayer; i++){
        send(sockfd,&((*data).AllSocketInNetwork[i]),sizeof(socketBSD),0); 
    }


}

void *RecvPython(void *StructArg)
{

    argument *arg = (argument *)StructArg;
    int number_thread = 1;
    pthread_t ID_threads[number_thread];

    char NewSocket[SIZE_DATA_PY];
    int OneConnection = 0; // flag pour déterminer si la le python a envoyer une deamnde de connection

    while (1)
    {

        int n = recv((*arg).sockfd, &((*arg).data->MyPlayer.dataPython), SIZE_DATA_PY * sizeof(char), 0);


        switch (n)
        {
        case -1:
            pthread_exit(NULL);
            break;

        case 0:
            printf("End connection by python Interface \n");
            pthread_exit(NULL);
            break;

        default:
            break;
        }

        if (!OneConnection)
        {

            //first message and init new connection with other player
            strncpy(NewSocket, (*arg).data->MyPlayer.dataPython, SIZE_DATA_PY);

            argument arg1;

            if (strncmp(NewSocket, "con", 3) == 0)
            {
                puts("\n new connexion via Python");

                char IP[16] = "";
                char char_port[6] ="";


                
                for (int i = 6; i < 21; i++)
                {
                    strncat(IP, &NewSocket[i], 1);
                }

                
                strncat(IP, "\0", 1);

                for (int i = 21; i < 26; i++)
                {
                    strncat(char_port, &NewSocket[i], 1);
                }
                strncat(char_port, "\0", 1);
                
                int port;
                sscanf(char_port, "%d", &port);
                
                printf("%s\n",IP);

                arg1.ip=malloc(16*sizeof(char));
                strncpy(arg1.ip, IP, 16);
                
                arg1.port_dest = port;
                arg1.data = (*arg).data;
                arg1.init = 1;

                if (pthread_create(&ID_threads[0], NULL, SendSructMyPlayer, &arg1) != 0)
                    OneConnection = 1;
            }
        }

        if (DEBUG)
        {
            display_data_player((*arg).data->MyPlayer);
        }
    }

    for (int t = 0; t < number_thread; t++)
    {
        pthread_join(ID_threads[t], NULL);
    }

    pthread_exit(NULL);
}

void *SendPython(void *StructArg)
{

    argument *arg = (argument *)StructArg;

    while (1)
    {

        for (int i = 0; i < (*arg).data->numberOtherPlayers; i++)
        {
            sleep(1);

            if (!(memcmp(&((*arg).data->OtherPlayers[i].dataPython), &((*arg).data->MemoryOtherPlayers[i].dataPython), SIZE_DATA_PY * sizeof(char)) == 0))
            {
                
                memcpy(&((*arg).data->MemoryOtherPlayers[i].dataPython), &((*arg).data->OtherPlayers[i].dataPython), SIZE_DATA_PY * sizeof(char));

                
                int n = send((*arg).sockfd, &((*arg).data->MemoryOtherPlayers[i].dataPython), strlen((*arg).data->MemoryOtherPlayers[i].dataPython) * sizeof(char), 0);

                if (n == -1)
                {
                    printf("problem with send python\n");
                    pthread_exit(NULL);
                }
            }
        }
    }

    pthread_exit(NULL);
}

void *interfacePython(void *Structdata)
{

    all_data *data = (all_data *)Structdata;

    int sockfd; // file descriptor for socket

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
        stop("socket");

    int enable =1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable)) < 0)
    {
        stop("socket_REUSEADDR");
    }

    struct sockaddr_in serv_addr;
    bzero(&serv_addr, sizeof(serv_addr));

    inet_pton(AF_INET, IP_INTERNE, &serv_addr.sin_addr); //set ip address
    serv_addr.sin_family = AF_INET;                      //set family
    serv_addr.sin_port = htons((*data).port_Interface);  //set port

    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
    {
        close(sockfd);
        stop("bind");
    }

    struct sockaddr_in client_python;
    int len = sizeof(client_python);
    char ip_python[16];

    if (listen(sockfd, 1) == -1)
        stop("listen");

    printf("Start network Interface Python\n");

    int pyhtonFD = accept(sockfd, (struct sockaddr *)&client_python, (socklen_t *)&len);
    inet_ntop(AF_INET, &client_python.sin_addr, ip_python, sizeof(ip_python));

    printf("Interface Python Connected  -->  ip : %s & port : %d\n\n", ip_python, ntohs(client_python.sin_port));
    data->InterfaceConnected = 1;

    argument arg;
    arg.data = data;
    arg.sockfd = pyhtonFD;

    int numberOfThread = 2;
    pthread_t thread_interface[numberOfThread]; // #0 recv python and write MyPlayer     #1 read otherPlayers and send Python

    if (pthread_create(&thread_interface[0], NULL, RecvPython, &arg) != 0)
        stop("thread_recv_Python");
    if (pthread_create(&thread_interface[1], NULL, SendPython, &arg) != 0)
        stop("thread_send_Python");

    //wait end of all thread
    for (int t = 0; t < numberOfThread; t++)
    {
        pthread_join(thread_interface[t], NULL);
    }

    close(sockfd);
    close(pyhtonFD);

    pthread_exit(NULL);
}

void *SendStructMyPlayerInit(void *StructArg)
{ // function init use with a shell for enter the IP other Player

    argument *arg = (argument *)StructArg;

    printf("enter Socket of other player :");
    char StringSocket[22];

    fflush(stdout);
    scanf("%[^\n]", StringSocket);
    fgetc(stdin);

    char *delim = ":";
    char *ptr = strtok(StringSocket, delim);
    char IP_for_new_connection[16];
    char stringPort[6];

    strcpy(IP_for_new_connection, ptr);
    ptr = strtok(NULL, delim);
    strcpy(stringPort, ptr);

    int new_port;
    sscanf(stringPort, "%d", &new_port);

    int number_thread = 1;
    pthread_t ID_threads[number_thread];

    argument arg1;
    arg1.data = (*arg).data;
    arg1.ip = IP_for_new_connection;
    arg1.port_dest = new_port;
    arg1.init = 1;

    if (pthread_create(&ID_threads[0], NULL, SendSructMyPlayer, &arg1) != 0)
        stop("thread struc player in init");

    for (int t = 0; t < number_thread; t++)
    {
        pthread_join(ID_threads[t], NULL);
    }

    pthread_exit(NULL);
}

void *SendStructMyPlayerInitARG(void *StructArg)
{ // function init use with on IP argument

    argument *arg = (argument *)StructArg;

    int number_thread = 1;
    pthread_t ID_threads[number_thread];

    argument arg1;
    arg1.data = (*arg).data;
    arg1.ip = (*arg).ip;
    arg1.init = 1;
    arg1.port_dest = (*arg).port_dest;

    if (pthread_create(&ID_threads[0], NULL, SendSructMyPlayer, &arg1) != 0)
        stop("thread struc player in init");

    for (int t = 0; t < number_thread; t++)
    {
        pthread_join(ID_threads[t], NULL);
    }

    pthread_exit(NULL);
}

void *RecevStuctOneOtherPlayer(void *StructArg)
{

    argument *arg = (argument *)StructArg;
    data_player new_player;
    int First = 1;
    int MyID;

    while (1)
    {

        int n = recv((*arg).sockfd, &new_player, sizeof(data_player), 0);


        switch (n)
        {
        case -1:
            pthread_exit(NULL);

        case 0:
            // printf("End connection by peer \n");
            // pthread_exit(NULL);
            //Somebody disconnected , get his details and print
            // getpeername((*arg).sockfd , (struct sockaddr*)&serv_addr , (socklen_t *)&len);
            // printf("Host disconnected , ip %s , port %d \n" , inet_ntoa(serv_addr.sin_addr) , ntohs(serv_addr.sin_port));    
            // close( (*arg).sockfd );

        default:
            break;
        }

        if (First)
        {
            MyID = new_player.id;
            First = 0;

            for (int i = 0; i < (*arg).data->numberOtherPlayers; i++)
            {
                if ((*arg).data->OtherPlayers[i].id == 0)
                {
                    memcpy(&((*arg).data->OtherPlayers[i]), &new_player, sizeof(data_player));
                    break;
                }
            }
        }
        else
        {
            for (int i = 0; i < (*arg).data->numberOtherPlayers; i++)
            {
                if ((*arg).data->OtherPlayers[i].id == MyID)
                {
                    memcpy(&((*arg).data->OtherPlayers[i].dataPython), &new_player.dataPython, SIZE_DATA_PY*sizeof(char));
                    break;
                }
            }
        }
    }

    pthread_exit(NULL);
}

void *SendSructMyPlayer(void *StructArg)
{

    argument *arg = (argument *)StructArg;
    char *IPserver;
    IPserver = malloc(16 * sizeof(char));

    strcpy(IPserver, (*arg).ip);
    printf("Testing connection with ip:%s and port:%d \n", IPserver, (*arg).port_dest);

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1)
        pthread_exit(NULL);

    int enable =1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable)) < 0)
    {
        pthread_exit(NULL);
    }

    struct sockaddr_in serv_OtherPlayer;
    int len = sizeof(serv_OtherPlayer);

    bzero(&serv_OtherPlayer, sizeof(serv_OtherPlayer));
    serv_OtherPlayer.sin_family = AF_INET;
    inet_aton(IPserver, &serv_OtherPlayer.sin_addr);
    serv_OtherPlayer.sin_port = htons((*arg).port_dest);

    if (connect(sockfd, (const struct sockaddr *)&serv_OtherPlayer, (socklen_t)len) < 0)
        pthread_exit(NULL);

    printf("This connection is success \n");

    int init = (*arg).init;
    int myPort = (*arg).data->port_Server;
    send(sockfd, &init, sizeof(int), 0);
    send(sockfd, &myPort, sizeof(int), 0);


    //sendSocketPlayerInNetwork(sockfd,(*arg).data); // to communicate all knowed-socket in network for to init new connection.


    data_player MyPlayer; // variable tempon pour verifier que les donner on changer
    bzero(&MyPlayer,sizeof(data_player));
    

    while (1)
    {
        sleep(1);

        if (!(memcmp(&MyPlayer, &((*arg).data->MyPlayer), sizeof(data_player)) == 0))
        {
            
            memcpy(&MyPlayer, &((*arg).data->MyPlayer), sizeof(data_player));
            send(sockfd, &MyPlayer, sizeof(data_player), 0);
        }
    }

    pthread_exit(NULL);
}

void *serverPeer(void *StrucData)
{

    all_data *data = (all_data *)StrucData;
    int enable = 1;

    int main_sockfd; // file descriptor for listening socket

    if ((main_sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
        stop("socket");

    if (setsockopt(main_sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable)) < 0)
    {
        pthread_exit(NULL);
    }

    struct sockaddr_in serv_addr;
    bzero(&serv_addr, sizeof(serv_addr));

    inet_pton(AF_INET, "0.0.0.0", &serv_addr.sin_addr); //accept all ip
    serv_addr.sin_family = AF_INET;                     //set family
    serv_addr.sin_port = htons((*data).port_Server);    //set port

    if (bind(main_sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
    {
        close(main_sockfd);
        stop("bind");
    }

    struct sockaddr_in OtherServer;
    int len = sizeof(OtherServer);
    char ip_OtherServer[16];

    if (listen(main_sockfd, 5) == -1)
        stop("listen");

    printf("Start network Server Peer2peer  with  my port %i\n", (*data).port_Server);

    int numberOfThread = 0;
    pthread_t *thread_server; // #1 recv struct data_player(Otherplayer) and add on data     #0  create new connection with other server and send MyPlayer

    while (1)
    {
        int new_playerFD = accept(main_sockfd, (struct sockaddr *)&OtherServer, (socklen_t *)&len);
        inet_ntop(AF_INET, &OtherServer.sin_addr, ip_OtherServer, sizeof(ip_OtherServer));

        printf("\n New player is connected -->  ip : %s & port : %d\n\n", ip_OtherServer, ntohs(OtherServer.sin_port));

        int init;
        int otherPort;
        //int numberSocket;
       

        int n = recv(new_playerFD, &init, sizeof(int), 0);
        if (DEBUG)
            printf("the value init is %i \n", init);

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

        n = recv(new_playerFD, &otherPort, sizeof(int), 0);
        if (DEBUG)
            printf("the new port for new is %i \n", otherPort);

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

       /*n = recv(new_playerFD, &numberSocket, sizeof(int), 0);
        if (DEBUG)
            printf("number of other player in network --> %i \n", numberSocket);

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

        //------------look all socket in network and if necessary, to create a new connection -----// 
        socketBSD OneSocketInNetwork;
        for ( int i=0; i < numberSocket ; i++){
            
            n = recv(new_playerFD, &OneSocketInNetwork, sizeof(socketBSD), 0);
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

            int MakeNewConnection = 1;
            for (int k=0; k< (*data).numberOtherPlayers; k++){

                if(memcmp(&((*data).AllSocketInNetwork[k]),&OneSocketInNetwork,sizeof(socketBSD)) == 0 )
                {
                    MakeNewConnection = 0;
                    break;   
                }
                
            }

            if (MakeNewConnection){

                numberOfThread++;
                thread_server = malloc(numberOfThread * sizeof(pthread_t));

                argument arg;
                arg.data=data;
                arg.port_dest=OneSocketInNetwork.port;
                arg.ip=malloc(16*sizeof(socketBSD));
                strncpy(arg.ip,OneSocketInNetwork.ip,16*sizeof(char));

                 if (pthread_create(&thread_server[numberOfThread-1], NULL, SendStructMyPlayerInitARG, &arg) != 0)
                    stop("thread_init_Send_Make_New_Connection_In_Network");
            }


        }

*/


        //----------init new size de Otherplayer------------//

        // data_player * tempOtherPlayer;
        // tempOtherPlayer = malloc((*data).numberOtherPlayers*sizeof(data_player));
        // memcpy(tempOtherPlayer,(*data).OtherPlayers,(*data).numberOtherPlayers*sizeof(data_player));

        data->numberOtherPlayers++;

        (*data).OtherPlayers = malloc((*data).numberOtherPlayers * sizeof(data_player));
        bzero(&((*data).OtherPlayers[(data->numberOtherPlayers) - 1]), sizeof(data_player));

        (*data).MemoryOtherPlayers = malloc((*data).numberOtherPlayers * sizeof(data_player));
        bzero(&((*data).MemoryOtherPlayers[(data->numberOtherPlayers) - 1]), sizeof(data_player));

        // memcpy((*data).OtherPlayers,tempOtherPlayer,((*data).numberOtherPlayers -1)*sizeof(data_player));

        // free(tempOtherPlayer);

        
        //------------Memory of new soket----------------//
        socketBSD socket;
        socket.ip =malloc(16* sizeof(char));
        strncpy(socket.ip,ip_OtherServer,16* sizeof(char));
        socket.port = otherPort;
        

        socketBSD * tempAllSocketInNetwork;
        if((*data).numberOtherPlayers > 1){
            tempAllSocketInNetwork = malloc((*data).numberOtherPlayers * sizeof(socketBSD));
            memcpy(tempAllSocketInNetwork,(*data).AllSocketInNetwork,((*data).numberOtherPlayers -1)*sizeof(socketBSD));
        }

        (*data).AllSocketInNetwork = malloc((*data).numberOtherPlayers * sizeof(socketBSD));
        
        if((*data).numberOtherPlayers > 1){
            memcpy((*data).AllSocketInNetwork,tempAllSocketInNetwork,((*data).numberOtherPlayers -1)*sizeof(socketBSD));
            free(tempAllSocketInNetwork);
        }

        memcpy(&((*data).AllSocketInNetwork[((*data).numberOtherPlayers-1)]),&socket,sizeof(socketBSD));


        for (int i=0; i< (*data).numberOtherPlayers; i++){
            printf("##%i",i);
            display_socket((*data).AllSocketInNetwork[i]);

        }

        argument arg;
        arg.ip = malloc(16 * sizeof(char));
        arg.data = data;
        arg.sockfd = new_playerFD;
        arg.port_dest = otherPort;
        arg.init = 0;
        strcpy(arg.ip, ip_OtherServer);

        if (init)
        {
            numberOfThread = numberOfThread + 2;
        }
        else
        {
            numberOfThread++;
        }

        thread_server = malloc(numberOfThread * sizeof(pthread_t));

        if (pthread_create(&thread_server[numberOfThread - 1], NULL, RecevStuctOneOtherPlayer, &arg) != 0)
            stop("thread_recv_one_other_player");

        if (init)
        {
            if (pthread_create(&thread_server[numberOfThread - 2], NULL, SendSructMyPlayer, &arg) != 0)
                stop("thread_send_my_player");
        }
    }

    //wait end of all thread
    for (int t = 0; t < numberOfThread; t++)
    {
        pthread_join(thread_server[t], NULL);
    }

    pthread_exit(NULL);
}

// argv[1]--> port for IntefacePython argv[2]-> port for SeverP2P  argv[3] --> for socket to other player

int main(int argc, char *argv[])
{

    if (DEBUG)
        printf("Size of struct data_player is : %ld \n", sizeof(data_player));

    pthread_t threads[NUM_THREADS]; // #0 interface  Python  #1 server Peer2Peer  #3 init to other server

    all_data data;

    data.numberOtherPlayers = 0;
    data.OtherPlayers = malloc(data.numberOtherPlayers * sizeof(data_player));

    data.MyPlayer.id = getpid();

    if (argc > 1)
        sscanf(argv[1], "%d", &(data.port_Interface));
    else
        data.port_Interface = DEFAUT_PORT_INTERNE;

    data.InterfaceConnected = 0;
    if (pthread_create(&threads[0], NULL, interfacePython, &data) != 0)
        stop("thread_interface_Python");

    while (1)
    {
        if (data.InterfaceConnected)
            break; // wait until one Interface Python is connected
    }

    if (argc > 2)
        sscanf(argv[2], "%d", &(data.port_Server));
    else
        data.port_Server = DEFAUT_PORT_EXTERNE;

    if (pthread_create(&threads[1], NULL, serverPeer, &data) != 0)
        stop("thread_Server_PeerToPeer");

    if (argc < 4)
    {
        // argument arg;
        // arg.data = &data;
        // sleep(0.5);
        // if (pthread_create(&threads[2], NULL, SendStructMyPlayerInit, &arg) != 0)
        //     stop("thread_init_Send_shell");
        puts("Shell desactiveted");
        
    }
    else
    {
        
        char *delim = ":";
        char *ptr = strtok(argv[3], delim);
        char ip[16];
        char stringPort[6];

        strcpy(ip, ptr);
        ptr = strtok(NULL, delim);
        strcpy(stringPort, ptr);

        int port;
        sscanf(stringPort, "%d", &port);

        argument arg;
        arg.data = &data;
        arg.ip = ip;
        arg.port_dest = port;
        if (pthread_create(&threads[2], NULL, SendStructMyPlayerInitARG, &arg) != 0)
            stop("thread_init_Send_ARGV");
    }

    //wait end of all thread
    for (int t = 0; t < NUM_THREADS; t++)
    {
        pthread_join(threads[t], NULL);
    }

    return EXIT_SUCCESS;
}