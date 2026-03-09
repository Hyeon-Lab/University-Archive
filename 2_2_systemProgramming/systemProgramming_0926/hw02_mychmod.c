//2021113411 PyoSuHyeon

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string.h>

int do_chmod(char *permission, char *filename);
void current_mode(char *filename);
void print_mod(char *filename, int order);
void reset_mode(char *filename);
void change_mode(char *permission, char *filename);
char path[100] = "./";


int main(int ac, char *av[]){
	
	if(ac != 3) {
		fprintf(stderr, "Usage: mychmod [permission] [filename]\n");
		exit(-1);
	}

	do_chmod(av[1], av[2]);
}

int do_chmod(char *permission, char *filename) {
	strcat(path, filename);
	current_mode(filename);
	reset_mode(filename);
	change_mode(permission, filename);
	return 0;
}

void current_mode(char *filename){
	print_mod(filename, 1);
}

void print_mod(char *filename, int order){
	struct stat buf;
	if(stat(filename, &buf) == -1){
		perror("Error");
		exit(-1);
	}
	else{
		switch(order){
			case 1: printf("1. current mode: "); break;
			case 2: printf(" -> 2. reset mode: "); break;
			case 3: printf(" -> 3. changed mode: "); break;
		}
		printf("%o", buf.st_mode);
	}
}

void reset_mode(char *filename){
	chmod(path, S_IXUSR & S_IXGRP);
	print_mod(filename, 2);
}

void change_mode(char *permission, char *filename){
	
	int mode = 00;

	switch(permission[0]){
		case '1': mode += S_IXUSR; break;
		case '2': mode += S_IWUSR; break;
		case '3': mode += S_IXUSR | S_IWUSR; break;
		case '4': mode += S_IRUSR; break;
		case '5': mode += S_IXUSR | S_IRUSR; break;
		case '6': mode += S_IWUSR | S_IRUSR; break;
		case '7': mode += S_IXUSR | S_IWUSR | S_IRUSR; break;
	}

	switch(permission[1]){
		case '1': mode += S_IXGRP; break;
		case '2': mode += S_IWGRP; break;
		case '3': mode += S_IXGRP | S_IWGRP; break;
		case '4': mode += S_IRGRP; break;
		case '5': mode += S_IXGRP | S_IRGRP; break;
		case '6': mode += S_IWGRP | S_IRGRP; break;
		case '7': mode += S_IXGRP | S_IWGRP | S_IRGRP; break;
	}

	switch(permission[2]){
		case '1': mode += S_IXOTH; break;
		case '2': mode += S_IWOTH; break;
		case '3': mode += S_IXOTH | S_IWOTH; break;
		case '4': mode += S_IROTH; break;
		case '5': mode += S_IXOTH | S_IROTH; break;
		case '6': mode += S_IWOTH | S_IROTH; break;
		case '7': mode += S_IXOTH | S_IWOTH | S_IROTH; break;
	}

	chmod(path, mode);
	print_mod(filename, 3);
	printf("\n");
}
