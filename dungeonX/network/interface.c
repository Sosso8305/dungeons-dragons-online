#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <string.h>

#define PORT 1234
#define IP "127.0.0.1"
#define BUF_SIZE 512
#define MAXLINE 1024

void stop(char *msg)
{
    perror(msg);
    exit(EXIT_FAILURE);
}

int main(int argc, char **argv)
{

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd == -1)
        stop("socket");

    struct sockaddr_in serv_addr;
    bzero(&serv_addr, sizeof(serv_addr));
    //set ip address
    inet_pton(AF_INET, IP, &serv_addr.sin_addr);
    //set family
    serv_addr.sin_family = AF_INET;
    //set port
    serv_addr.sin_port = htons(PORT);

    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
    {
        close(sockfd);
        stop("bind");
    }
    struct sockaddr_in cli;
    int n, len = sizeof(cli);
    char buffer[BUF_SIZE];
    //char * msg_server = "";
    char ip_client[16];
    if (listen(sockfd, 5) == -1)
        stop("listen");
    printf("Server started\n");
    int client = accept(sockfd, (struct sockaddr *)&cli, (socklen_t *)&len);
    inet_ntop(AF_INET, &cli.sin_addr, ip_client, sizeof(ip_client));
    printf("New client\nip : %s\nport : %d\n\n", ip_client, ntohs(cli.sin_port));
    while(1)
    {
        n = recv(client, buffer, BUF_SIZE - 1, 0);
        if (n == -1)
        {
            close(sockfd);
            stop("recv");
        }
        if (n == 0)
        {
            printf("Connection reset by peer\n");
            break;
        }
        buffer[n] = '\0';
        printf("%s\n", buffer);
        int s = send(client, buffer, n, 0);
        if (s == -1)
        {
            close(client);
            close(sockfd);
            stop("send");
        }
    }
    close(sockfd);
    close(client);
    return 0;
}