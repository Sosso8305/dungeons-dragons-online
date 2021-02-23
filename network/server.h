

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
    int InterfaceConnected;  

}all_data;

typedef struct argument
{
    all_data * data;
    int sockfd;
    char * ip;
    int init;  
    
}argument;

void display_data_player (data_player player);
void stop(char *msg);

void * RecvPython(void * StructArg);
void * SendPython(void * StructArg);
void * interfacePython(void * Structdata);

void * SendStructMyPlayerInit(void * StructArg);
void * RecevStuctOneOtherPlayer(void * StructArg);
void * SendSructMyPlayer(void * StructArg);
void * serverPeer(void * StrucData);