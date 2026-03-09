#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>

#define COMPARE(x,y) (((x) < (y)) ? -1:  ((x) == (y)) ? 0: 1)

int ary[2][20] = { 0 };
int avail = 0;
int aryD[2] = { 0 };

void padd(int sA, int fA, int sB, int fB, int avail) {
	aryD[0] = avail;
	while ((sA <= fA) && (sB <= fB)) {
		if (avail >= 20) {
			fprintf(stderr, "Too many terms in the polynomial\n");
			exit(EXIT_FAILURE);
		}
		switch (COMPARE(ary[1][sA], ary[1][sB])) {
		case 1:
			ary[0][avail] = ary[0][sA];
			ary[1][avail] = ary[1][sA];
			//printf("%d %d\n", ary[0][avail], ary[1][avail]);
			avail++, sA++;
			break;
		case 0:
			ary[0][avail] = ary[0][sA] + ary[0][sB];
			ary[1][avail] = ary[1][sA];
			//printf("%d %d\n", ary[0][avail], ary[1][avail]);
			avail++, sA++; sB++;
			break;
		case -1:
			ary[0][avail] = ary[0][sB];
			ary[1][avail] = ary[1][sB];
			//printf("%d %d\n", ary[0][avail], ary[1][avail]);
			avail++, sB++;
			break;
		}
	}
	for (; sA <= fA; sA++) {
		ary[0][avail] = ary[0][sA];
		ary[1][avail] = ary[1][sA];
		//printf("%d %d\n", ary[0][avail], ary[1][avail]);
		avail++, sA++;
	}
	for (; sB <= fB; fA++) {
		ary[0][avail] = ary[0][sB];
		ary[1][avail] = ary[1][sB];
		//printf("%d %d\n", ary[0][avail], ary[1][avail]);
		avail++, sB++;
	}
	aryD[1] = avail - 1;
	//printf("%d %d", aryD[0], aryD[1]);
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;
	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	int n, m;
	fscanf_s(infile, "%d", &n);
	fscanf_s(infile, "%d", &m);

	printf("input\n\n");
	printf("%d %d\n\n", n, m);

	int finish[2] = { 0 }, start[2] = { 0 }, k = 0;

	for (int i = 0; feof(infile) != 1; i++) {
		for (int j = 0; j < 2; j++) {
			fscanf_s(infile, "%d", &ary[j][i]);
			printf("%d ", ary[j][i]);
			if ((j == 1) && (ary[j][i] == 0)) {
				finish[k] = i;
				k++;
			}
		}
		printf("\n");
	}
	start[1] = finish[0] + 1;
	avail = finish[1] + 1;

	fclose(infile);

	printf("\n\noutput\n\n");

	padd(start[0], finish[0], start[1], finish[1], avail);

	for (int j = aryD[0]; j <= aryD[1]; j++) {
		for (int i = 0; i < 2; i++) {
			printf("%d ", ary[i][j]);
			fprintf(outfile, "%d ", ary[i][j]);
		}
		printf("\n");
		fprintf(outfile, "\n");

	}
	fclose(outfile);
}

