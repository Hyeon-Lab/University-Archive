#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char** dictionary;

int findprime(int n) {
	int temp = n;
	while (1) {
		int check = 0;
		for (int i = 2; i < temp; i++) {
			if (temp % i == 0) {
				check = 1;
			}
		}
		if (check == 0) {
			return temp;
		}
		else {
			temp++;
		}
	}
}

int StringToInt(char* data) {
	int n = 0;
	while (*data) {
		n += *data++;
	}
	return n;
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;

	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	int n;
	fscanf(infile, "%d", &n);

	printf("input\n\n%d\n", n);

	int d = findprime(n);
	
	dictionary = malloc(sizeof(*dictionary) * d);
	int* check_dictionary = malloc(sizeof(*check_dictionary) * d);
	for (int i = 0; i < d; i++) {
		dictionary[i] = malloc(sizeof(**dictionary) * 100);
		check_dictionary[i] = 0;
	}

	char* data;
	data = malloc(sizeof(*data) * 100);
	for (int i = 0; i < n; i++) {
		if (i % 4 == 0) printf("\n");
		fscanf(infile, "%s", data);
		if (data != NULL) {
			printf("%s ", data);
			int index = StringToInt(data) % d;
			if (check_dictionary[index] == 0) {
				check_dictionary[index] = 1;
				strcpy(dictionary[index], data);
			}
			else {
				for (int j = 0; j < d - 1; j++) {
					if (check_dictionary[((index + j) % d)] == 0) {
						check_dictionary[((index + j) % d)] = 1;
						strcpy(dictionary[((index + j) % d)], data);
						break;
					}
				}
			}
		}
	}

	printf("\n\noutput\n");
	char* search = malloc(sizeof(*search)*100);
	while (1) {
		printf("\n> 검색할 키워드를 입력하시오...\n");
		fprintf(outfile, "\n> 검색할 키워드를 입력하시오...\n");
		printf("> ");
		fprintf(outfile, "> ");
		scanf("%s", search);
		fprintf(outfile, "%s\n", search);
		if (strcmp(search,"quit") == 0) {
			break;
		}
		else {
			int check = 0;
			for (int i = 0; i < d; i++) {
				if (dictionary[i] != NULL && search != NULL) {
					if (strcmp(dictionary[i], search) == 0) {
						printf("\n> 버킷 주소 %d에 저장된 키워드 입니다.\n", i);
						fprintf(outfile, "\n> 버킷 주소 %d에 저장된 키워드 입니다.\n", i);
						check = 1;
					}
				}
			}

			if (check == 0) {
				printf("\n> 키워드가 존재하지 않습니다\n");
				fprintf(outfile, "\n> 키워드가 존재하지 않습니다\n");
			}
		}
	}
	fclose(infile);
	fclose(outfile);
}