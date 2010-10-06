#include <stdio.h>
#include <stdlib.h>

static void readFlag(void);

void readFlag(void){
	char cat[] = "cat flag.txt";
 	system(cat);
}

int main(int argc, char *argv[]){
	static char buf[512];
	setuid(geteuid());
	fgets(buf, 512, stdin);
	printf(buf);
}
