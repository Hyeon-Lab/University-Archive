//2021113411 PyoSuHyeon

#include <stdio.h>
#include <utmp.h>
#include <time.h>
#include <stdlib.h>

extern int utmp_open(char *filename);
extern struct utmp *utmp_next();
extern void utmp_close();
void show_info(struct utmp *);
void showtime(time_t);

int main() {
	struct utmp *utbufp = NULL;
	if (utmp_open("/var/run/utmp") == -1){
		perror("/var/run/utmp");
		exit(-1);
	}

	while((utbufp = utmp_next()) != NULL){
		show_info(utbufp);
	}
	utmp_close();
	return 0;
}

void show_time(int seconds){
	time_t sec = (time_t)seconds;
	char *cp = ctime(&sec);
	printf("%12.12s ", cp + 4);
}

void show_info(struct utmp *ut_buf_p){
	if(ut_buf_p -> ut_type != USER_PROCESS){
		return;
	}

	printf("%-8.8s", ut_buf_p -> ut_user);
	printf(" ");
	printf("%-8.8s", ut_buf_p -> ut_line);
	printf(" ");
	show_time(ut_buf_p -> ut_tv.tv_sec);

	if(ut_buf_p -> ut_host[0] != '\0'){
		printf("(%s)", ut_buf_p -> ut_host);
	}
	printf("\n");
}