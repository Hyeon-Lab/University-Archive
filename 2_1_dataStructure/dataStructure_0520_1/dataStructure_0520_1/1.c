#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>

int runary[8][5];
int rcount[8] = { 0,0,0,0,0,0,0,0 };
int losertree[16];
int winnertree[16];
int max;
int endcount = 0;

void makeLoserTree() {
	for (int i = 14; i >= 2; i = i - 2) {
		if (winnertree[i] <= winnertree[i + 1]) {
			winnertree[i / 2] = winnertree[i];
		}
		else {
			winnertree[i / 2] = winnertree[i + 1];
		}
	}

	for (int i = 7; i >= 1; i--) {
		if (winnertree[i] == winnertree[2 * i]) {
			losertree[i] = winnertree[2 * i + 1];
		}
		else {
			losertree[i] = winnertree[2 * i];
		}
	}
	losertree[0] = winnertree[1];

}

void printOrder(FILE * outfile) {
	printf("%d ", losertree[0]);
	fprintf(outfile, "%d ", losertree[0]);
	int index = 0;
	for (int i = 8; i < 16; i++) {
		if (losertree[i] == losertree[0]) {
			if (rcount[i - 8] > 4) {
				losertree[i] = max;
				endcount++;
			}
			else {
				losertree[i] = runary[i - 8][rcount[i - 8]++];
			}
			index = i;
			break;
		}
	}
	int data = losertree[index];
	for (index; index > 1;) {
		if (losertree[index / 2] < data) {
			int temp = data;
			data = losertree[index / 2];
			losertree[index / 2] = temp;
			index /= 2;
		}
		else {
			index /= 2;
		}
	}
	losertree[0] = data;
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;

	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	int n, k;

	fscanf(infile, "%d", &n);
	fscanf(infile, "%d", &k);

	printf("input\n\n%d %d\n", n, k);

	int data;
	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 5; j++) {
			fscanf(infile, "%d", &data);
			if (data >= max) {
				max = data;
			}
			printf("%d ", data);
			runary[i][j] = data;
		}
		printf("\n");
	}
	max++;

	for (int i = 0; i < 8; i++) {
		losertree[i + 8] = runary[i][rcount[i]++];
		winnertree[i + 8] = runary[i][0];
	}

	printf("\noutput\n\n");

	makeLoserTree();
	

	while (endcount != 8) {
		printOrder(outfile);
	}
	fclose(infile);
	fclose(outfile);
}