//2021113411 PyoSuHyeon

#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>

int linelen;
int pagelen;

void do_more(FILE *);
int see_more(FILE *);

int main(int ac, char *av[]) {

  struct winsize wbuf;
	if(ioctl(0, TIOCGWINSZ, &wbuf) != -1){
		linelen =  wbuf.ws_col;
    pagelen =  wbuf.ws_row;
  }

  FILE *fp;
  if(ac == 2) {
    if((fp = fopen(*++av, "r")) != NULL) {
        do_more(fp);
        fclose(fp);
      }
      else {
        exit(1);
      }
  }
  else {
    fprintf(stderr, "[Usage] %s [filename]\n", av[0]);
  }
  return 0;
}

void do_more(FILE *fp) {
  char line[linelen];
  int num_of_line = 0;
  int reply = 0;
  FILE *fp_tty = fopen("/dev/tty", "r");
  if(fp_tty == NULL)
    exit(1);
  
  while(fgets(line, linelen, fp) !=NULL) {
    if(num_of_line == pagelen){
      reply = see_more(fp_tty);
      if(reply == 0) 
        break;
      num_of_line -= reply;
    }
    if(fputs(line, stdout) == EOF)
      exit(1);
    num_of_line++;
  }
}

int see_more(FILE *cmd){
  int c = 0;
  printf("\033[7m more?(%d * %d) \033[m", pagelen, linelen);
  while((c=getc(cmd)) != EOF){
    if(c=='q')
      return 0;
    if(c==' ')
      return pagelen;
    if(c=='\n')
      return 1;
  }
  return 0;
}
