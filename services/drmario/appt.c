#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char **argv) {
	char cat[] = "cat ";
	char *command;
	char buf[32];
	size_t commandLength;
	command = (char *) malloc(commandLength);

	fgets(buf, 32, stdin);
	commandLength = strlen(cat) + strlen(buf) + 1;
	strncpy(command, cat, commandLength);
	strncat(command, buf, (commandLength - strlen(cat)));
	system(command);
	return (0);
}
