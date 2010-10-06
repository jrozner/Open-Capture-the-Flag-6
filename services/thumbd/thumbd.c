#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <pwd.h>

#define BUFF 200

void get_input(char *);
int get_uid_by_name(char *);

int main(int argc, char *argv[])
{
  char username[BUFF];

  get_input(username);

  printf("%s's uid is %d\n", username, get_uid_by_name(username));
  fflush(stdout);

  return 0;
}

void get_input(char *username)
{
  char input[BUFF];
  gets(input);
  strncpy(username, input, BUFF - 1);
}

int get_uid_by_name(char *username)
{
  struct passwd *user_info;

  if ((user_info = getpwnam(username)) == NULL)
  {
    printf("Unable to find user: %s\n", username);
    exit(1);
  }

  return user_info->pw_uid;
}
