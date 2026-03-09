#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;

	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	int n;

	fscanf(infile, "%d", &n);

	printf("input\n\n%d\n", n);

	int max = 10;
	int* equivalent = malloc(sizeof(*equivalent) * max);
	for (int i = 0; i < max; i++) {
		*(equivalent + i) = -1;
	}

	int n1, n2;
	for (int i = 0; i < n; i++) {
		fscanf(infile, "%d = %d,", &n1, &n2);
		printf("%d = %d\n", n1, n2);
		if (n1 >= max || n2 >= max) {
			realloc(equivalent, sizeof(equivalent) * max * 2);
			for (int i = max; i < 2 * max; i++) {
				*(equivalent + i) = -1;
			}
			max *= 2;
		}
		
		while (*(equivalent + n1) >= 0) {
			n1 = *(equivalent + n1);
		}

		while (*(equivalent + n2) >= 0) {
			n2 = *(equivalent + n2);
		}

		int temp = *(equivalent + n2) + *(equivalent + n1);
		if (*(equivalent + n1) <= *(equivalent + n2)) {
			*(equivalent + n2) = n1;
			*(equivalent + n1) = temp;
		}
		else {
			*(equivalent + n1) = n2;
			*(equivalent + n2) = temp;
		}
	}

	int count = 0;
	for (int i = 0; i < max; i++) {
		if (*(equivalent + i) < -1) {
			count++;
		}
	}

	
	printf("\noutput\n\nTotal # of equivalence classes = %d\nEquivalence classes : ", count);
	fprintf(outfile, "Total # of equivalence classes = %d\nEquivalence classes : ", count);
	
	int c = 0;
	for (int i = 0; i < max; i++) {
		if (*(equivalent + i) < -1) {
			if (c != 0) {
				fprintf(outfile, ", {");
				printf(", {");
			}
			else {
				fprintf(outfile, "{");
				printf("{");
				c++;
			}
			int c1 = 0;
			for (int j = 0; j < max; j++) {
				int l = j;
				while (*(equivalent + l) >= 0) {
					l = *(equivalent + l);
				}
				if (l == i) {
					if (c1 == 0) {
						printf("%d", j);
						fprintf(outfile, "%d", j);
						c1++;
					}
					else {
						printf(", %d", j);
						fprintf(outfile, ", %d", j);
					}
				}
			}
			printf("}");
			fprintf(outfile, "}");
		}
	}
	fclose(infile);
	fclose(outfile);
}