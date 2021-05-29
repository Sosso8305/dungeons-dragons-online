#define SIZE_DATA_PY 43


typedef struct   // struct for one player
{
    int id;   //essential element 
    char dataPython[SIZE_DATA_PY];

}data_player;

typedef struct 
{
    char * ip;
    int port;
} socketBSD;


typedef struct 
{
    data_player MyPlayer;       //struct data myplayer
    int numberOtherPlayers;     //number other Player for tab dynamique
    data_player * OtherPlayers; //tab data of all player
    data_player * MemoryOtherPlayers; //tampon
    socketBSD * AllSocketInNetwork;
    int InterfaceConnected;
    int port_Server;
    int port_Interface;

}all_data;

typedef struct
{
    all_data * data;
    int sockfd;
    char * ip;
    int init;
    int port_dest;

}argument;



void display_data_player (data_player player);
void stop(char *msg);
void sendSocketPlayerInNetwork(int sockfd,all_data * data);

void * RecvPython(void * StructArg);
void * SendPython(void * StructArg);
void * interfacePython(void * Structdata);

void * SendStructMyPlayerInit(void * StructArg);
void * RecevStuctOneOtherPlayer(void * StructArg);
void * SendSructMyPlayer(void * StructArg);
void * serverPeer(void * StrucData);
void * SendStructMyPlayerInitARG(void * StructArg);