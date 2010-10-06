// 2speed.c - t1g3r
//
// two race condition vulns exist
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
#define SAPZKEY "sapz.key"
#define SAPZTMP "sapz.tmp"
 
int main(int argc, char *argv[])
{
  FILE *fr, *fw;
  int r;
  char buf[128]={0,};
  char key[33]={0,};
 
  if(2>argc)
    return -1;
 
  //seed con tiempo
  srand(time(0));
 
  //generate random value
  //vuln#1: race condition of rand()
  r = rand();
  sprintf(buf, "%08x", r );
 
  //if user got the correct random value, create tmp file
  if (0==strcmp(buf, argv[1]))
  {
    //read the key
    fr = fopen(SAPZKEY, "r+");
    fread(key, 1, 33, fr);
 
    //write the key
    sprintf(buf, "/tmp/%s.%08x", SAPZTMP, r);
 
    fw = fopen(buf, "w+");
    fwrite(key, 1, 33, fw);
 
    fclose(fr);
    fclose(fw);
 
    //remove the tmp file
    remove(buf);
  }
 
  return 0;
}