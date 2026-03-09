#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>

int n;

void quickSort(int* ary, int left, int right) {
	int i; int j; int pivot; int temp;

	if (left < right) {
		i = left;
		j = right + 1;
		pivot = ary[left];
		do {
			do i++; while (ary[i] < pivot);
			do j--; while (ary[j] > pivot);
			if (i < j) {
				temp = ary[i];
				ary[i] = ary[j];
				ary[j] = temp;
			}
		} while (i < j);

		temp = ary[left];
		ary[left] = ary[j];
		ary[j] = temp;

		quickSort(ary, left, j - 1);
		quickSort(ary, j + 1, right);
	}
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;

	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	int data;
	fscanf(infile, "%d", &n);
	printf("input\n\n%d\n", n);

	int* ary = malloc(sizeof(*ary) * n);

	for (int i = 0; i < n; i++) {
		fscanf(infile, "%d", &data);
		ary[i] = data;
		printf("%d ", ary[i]);
	}
	printf("\n");

	quickSort(ary, 0, n-1);

	printf("\noutput\n\n");

	for (int i = 0; i < n; i++) {
		printf("%d ", ary[i]);
		fprintf(outfile, "%d ", ary[i]);
	}
	fclose(infile);
	fclose(outfile);
}