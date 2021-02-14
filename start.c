#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

void *start(void *tid){
    pid_t pid;

    pid = fork();
    if(pid == 0){
        execlp("python","python","-m","start",(char *)0);
        exit(EXIT_SUCCESS);
    }
}

int main(){
    pthread_t tid0,tid1;

    pthread_create(&tid0,NULL,start,NULL);
    pthread_join(tid0,NULL);
    pthread_create(&tid1,NULL,start,NULL);
    pthread_join(tid1,NULL);

    pthread_exit(NULL);
    return 0;
}