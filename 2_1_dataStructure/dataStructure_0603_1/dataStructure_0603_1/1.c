#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>

typedef struct adjList* adjPointer;
typedef struct adjList {
	int data;
	int weight;
	adjPointer link;
}adjList;

typedef struct edge {
	int i;
	int j;
	int weight;
}edge;

int** matrix;
adjPointer *adjLists;
int n;
int eNum;
edge *eList;
edge* prims;
edge *selectedEdge;
int s = 0;
int cost = 0;

void makeMatrix(int i, int j, int data) {
	matrix[i][j] = data;
}

void addAdjList(int i, int j, int data) {
	if (data != 0) {
		adjPointer temp = malloc(sizeof(*temp));
		temp->data = j;
		temp->link = adjLists[i];
		temp->weight = data;
		adjLists[i] = temp;
		eNum++;
	}
}

void printAdjList() {
	for (int i = 0; i < n; i++) {
		adjPointer temp = adjLists[i];
		while (temp != NULL) {
			printf("node %d data %d weight %d\n",i , temp->data, temp->weight);
			temp = temp->link;
		}
	}
}

void eListAdd() {
	eList = malloc(sizeof(*eList) * eNum);
	int e = 0;
	for (int i = 0; i < n; i++) {
		for (int j = i; j < n; j++) {
			if (matrix[i][j] != 0) {
				eList[e].i = i;
				eList[e].j = j;
				eList[e++].weight = matrix[i][j];
			}
		}
	}
	/*for (int i = 0; i < e; i++) {
		printf("eList %d i %d j %d weight %d\n", i, eList[i].i, eList[i].j, eList[i].weight);
	}*/
}

void prims_algorithm(int v) {
	
	if (s != n-1) {

		if (eNum == 0) return;

		for (int i = 0; i < eNum; i++) {
			if (eList[i].i == v) {
				int j = eList[i].j;
				/*printf("edge %d %d %d\n", eList[i].i, eList[i].j, eList[i].weight);*/
				if (prims[j].weight == NULL || eList[i].weight < prims[j].weight) {
					prims[j].weight = eList[i].weight;
					prims[j].i = eList[i].i;
					prims[j].j = eList[i].j;
					eList[i] = eList[eNum--];
				}
				else {
					eList[i] = eList[eNum--];
				}
			}
			else if (eList[i].j == v) {
				int j = eList[i].i;
				/*printf("edge %d %d %d\n", eList[i].i, eList[i].j, eList[i].weight);*/
				if (prims[j].weight == NULL || eList[i].weight < prims[j].weight) {
					prims[j].weight = eList[i].weight;
					prims[j].i = eList[i].i;
					prims[j].j = eList[i].j;
					eList[i] = eList[eNum--];
				}
				else {
					eList[i] = eList[eNum--];
				}
			}
		}

		/*printf("\n");
		for (int i = 0; i < n; i++) {
			if (prims[i].weight == NULL) {
				printf("X ");
			}
			else printf("%d ", prims[i].weight);
		}
		printf("\n");*/

		edge min = prims[0];
		int m = 0;
		for (int i = 0; i < n; i++) {
			if (min.weight == NULL || min.weight == -1) {
				if (prims[i].weight != NULL && prims[i].weight != -1) {
					min = prims[i];
					m = i;
				}
			}
			else {
				if (prims[i].weight != -1 && prims[i].weight < min.weight) {
					min = prims[i];
					m = i;
				}
			}
		}
		prims[m].weight = -1;
		selectedEdge[s++] = min;
		cost += min.weight;

		if (min.i == v) {
			prims_algorithm(min.j);
		}
		else {
			prims_algorithm(min.i);
		}
	}
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;

	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	fscanf(infile, "%d", &n);

	printf("input\n\n%d\n", n);

	adjLists = malloc(sizeof(*adjLists) * n);
	matrix = malloc(sizeof(*matrix) * n);
	prims = malloc(sizeof(*prims) * n);
	selectedEdge = malloc(sizeof(*selectedEdge) * (n - 1));
	for (int i = 0; i < n; i++) {
		prims[i].weight = NULL;
		adjLists[i] = NULL;
		matrix[i] = malloc(sizeof(**matrix) * n);
	}

	int data;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			fscanf(infile, "%d", &data);
			printf("%d ", data);
			addAdjList(i, j, data);
			makeMatrix(i, j, data);
		}
		printf("\n");
	}
	eNum /= 2;

	//printAdjList();

	eListAdd();
	prims_algorithm(0);

	printf("\noutput\n\n");

	printf("Adjacency matrix representation MCST = {");
	fprintf(outfile, "Adjacency matrix representation MCST = {");
	int c = 0;
	for (int i = 0; i < s; i++) {
		if (c == 0) {
			printf("(%d, %d)", selectedEdge[i].i, selectedEdge[i].j);
			fprintf(outfile, "(%d, %d)", selectedEdge[i].i, selectedEdge[i].j);
			c++;
		}
		else {
			printf(", (%d, %d)", selectedEdge[i].i, selectedEdge[i].j);
			fprintf(outfile, ", (%d, %d)", selectedEdge[i].i, selectedEdge[i].j);
		}
	}
	printf("}\n");
	fprintf(outfile, "}\n");
	printf("Total cost = %d\n\n", cost);
	fprintf(outfile, "Total cost = %d\n\n", cost);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			int check = -1;
			for (int k = 0; k < s; k++) {
				if ((selectedEdge[k].i == i && selectedEdge[k].j == j) || (selectedEdge[k].i == j && selectedEdge[k].j == i)) {
					check = k;
				}
			}
			if (check != -1) {
				printf("%d ", selectedEdge[check].weight);
				fprintf(outfile, "%d ", selectedEdge[check].weight);
			}
			else {
				printf("0 ");
				fprintf(outfile, "0 ");
			}
		}
		printf("\n");
		fprintf(outfile, "\n");
	}
}