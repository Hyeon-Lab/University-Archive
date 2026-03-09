#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* preorder;
char* inorder;
char* tree;
int preIndex = 0;
int len = 0;
int max = 100;

void buildTree(int start, int end, int position) {
	if (start <= end) {
		int inIndex;
		int count = 0;
		char current = preorder[preIndex++];
		for (int i = 0; i < len; i++) {
			if (current == inorder[i]) {
				inIndex = i;
				count++;
			}
		}
		if (count == 0) {
			inIndex = -1;
		}
		tree[position] = current;

		if (2 * position >= max || 2 * position + 1 >= max) {
			realloc(tree, sizeof(tree) * max * 2);
			for (int i = max; i < 2 * max; i++) {
				tree[i] = NULL;
			}
			max *= 2;
		}

		buildTree(start, (inIndex - 1), 2 * position);
		buildTree((inIndex + 1), end, 2 * position + 1);
	}
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;

	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	tree = malloc(sizeof(*tree) * 100);
	for (int i = 0; i < max; i++) {
		tree[i] = NULL;
	}
	preorder = malloc(sizeof(*preorder) * 20);
	inorder = malloc(sizeof(*inorder) * 20);
	fscanf(infile, "preorder sequence : %s\n", preorder);
	fscanf(infile, "inorder sequence : %s", inorder);

	printf("input\n\n");
	printf("preorder sequence : %s\n", preorder);
	printf("inorder sequence : %s\n", inorder);

	len = strlen(inorder);

	buildTree(0, len - 1, 1);


	printf("\noutput\n\n");

	int count = 0;
	for (int i = 0; i < max; i++) {
		if (tree[i] != NULL) {
			if (count == 0) {
				printf("%d", i);
				fprintf(outfile, "%d", i);
				count++;
			}
			else {
				printf(", %d", i);
				fprintf(outfile, ", %d", i);
			}

		}
	}

	fclose(infile);
	fclose(outfile);
}