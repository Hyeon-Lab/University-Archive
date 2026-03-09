#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>

typedef struct adj* adjpointer;
typedef struct adj {
	int data;
	adjpointer link;
}adj;

typedef struct edge {
	int i;
	int j;
	int w;
}edge;

int n;
int e;
int t;
int cost = 0;
int e_count = 0;
int** matrix;
int** outMatrix;
adjpointer* adjlist;
edge* edgelist;
int* equivalent;
int* minheap;
int max;

void makeAdjList() {
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (matrix[i][j] != 0) {
				e++;
				adjpointer temp = malloc(sizeof(*temp));
				temp->data = j;
				if (adjlist == NULL) {
					temp->link = NULL;
					adjlist[i] = temp;
				}
				else {
					temp->link = adjlist[i];
					adjlist[i] = temp;
				}
			}
		}
	}
}
void edgelistAdd() {
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			outMatrix[i][j] = 0;
			if (matrix[i][j] != 0) {
				int check = 0;
				for (int k = 0; k < e; k++) {
					if (j == edgelist[k].i && i == edgelist[k].j) {
						check = 1;
					}
				}
				if (check == 0) {
					edgelist[e_count].i = i;
					edgelist[e_count].j = j;
					edgelist[e_count++].w = matrix[i][j];
				}
			}
		}
	}
}


void add(int i, int j) {
	if (equivalent[i] <= equivalent[j]) {
		equivalent[i] = equivalent[i] + equivalent[j];
		equivalent[j] = i;
	}
	else {
		equivalent[j] = equivalent[i] + equivalent[j];
		equivalent[i] = j;
	}
}

void search(int n1, int n2, int w) {
	int i = n1;
	int j = n2;
	while (equivalent[i] >= 0) {
		i = equivalent[i];
	}
	while (equivalent[j] >= 0) {
		j = equivalent[j];
	}
	if (i != j) {
		t++;
		add(i, j);
		outMatrix[n1][n2] = w;
		outMatrix[n2][n1] = w;
		cost += w;
	}
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;
	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	n = 0; e = 0; t = 0;
	int data;

	fscanf(infile, "%d", &n);
	printf("input\n\n%d\n", n);

	matrix = malloc(sizeof(*matrix) * n);
	outMatrix = malloc(sizeof(*outMatrix) * n);
	adjlist = malloc(sizeof(*adjlist) * n);
	equivalent = malloc(sizeof(*equivalent) * n);
	for (int i = 0; i < n; i++) {
		*(matrix + i) = malloc(sizeof(**matrix) * n);
		*(outMatrix + i) = malloc(sizeof(**outMatrix) * n);
		equivalent[i] = -1;
	}
	
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			fscanf(infile, "%d", &data);
			matrix[i][j] = data;
			printf("%d ", data);
		}
		printf("\n");
	}
	makeAdjList();
	e /= 2;
	edgelist = malloc(sizeof(*edgelist) * e);
	edgelistAdd();

	while (t < n - 1 && e != 0) {
		edge min = edgelist[0];
		int minIndex = -1;
		for (int k = 0; k < e; k++) {
			if (edgelist[k].w <= min.w) {
				min = edgelist[k];
				minIndex = k;
			}
		}

		search(min.i, min.j, min.w);

		edgelist[minIndex] = edgelist[e-1];
		e--;
	}
	printf("\noutput\n\n");
	if (t < n - 1) {
		printf("No spanning tree\n");
		fprintf(outfile, "No spanning tree\n");
	}
	else {
		printf("Adjacency matrix representation MCST = {");
		fprintf(outfile, "Adjacency matrix representation MCST = {");
		int count = 0;
		for (int i = 0; i < n; i++) {
			for (int j = i; j < n; j++) {
				if (outMatrix[i][j] != 0) {
					if (count == 0) {
						printf("(%d, %d)", i, j);
						fprintf(outfile, "(%d, %d)", i, j);
						count++;
					}
					else {
						printf(", (%d, %d)", i, j);
						fprintf(outfile, ", (%d, %d)", i, j);
					}
				}
			}
		}
		printf("}\n");
		fprintf(outfile, "}\n");
		printf("Total cost = %d\n\n", cost);
		fprintf(outfile, "Total cost = %d\n\n", cost);
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				printf("%d ", outMatrix[i][j]);
				fprintf(outfile, "%d ", outMatrix[i][j]);
			}
			printf("\n");
			fprintf(outfile, "\n");
		}
	}

	fclose(infile);
	fclose(outfile);
}