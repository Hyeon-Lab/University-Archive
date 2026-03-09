#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>

typedef struct avl* avlpointer;
typedef struct avl {
	int data;
	avlpointer lchild;
	avlpointer rchild;
	avlpointer parent;
	int bf;
	int lnum;
	int rnum;
}avl;

avlpointer tree;

void printAvl(int n, FILE* outfile) {
	int count = 0;
	int index = 1;
	while (count != n) {
		int b[100];
		int i = 0;
		int num = index;
		avlpointer temp = tree;
		if (index == 1) {
			printf("CBT %d번 노드 = %d \tbf = %d\n", index, temp->data, temp->bf);
			fprintf(outfile, "CBT %d번 노드 = %d \tbf = %d\n", index, temp->data, temp->bf);
			index++;
			count++;
		}
		else {
			while (num != 0) {
				b[i++] = num % 2;
				num /= 2;
			}
			for (int j = i - 2; j > 0; j--) {
				if (b[j] == 1) {
					temp = temp->rchild;
				}
				else {
					temp = temp->lchild;
				}
			}
			if (b[0] == 1) {
				if (temp->rchild != NULL) {
					printf("CBT %d번 노드 = %d \tbf = %d\n", index, temp->rchild->data, temp->rchild->bf);
					fprintf(outfile, "CBT %d번 노드 = %d \tbf = %d\n", index, temp->rchild->data, temp->rchild->bf);
					count++;
				}
			}
			else {
				if (temp->lchild != NULL) {
					printf("CBT %d번 노드 = %d \tbf = %d\n", index, temp->lchild->data, temp->lchild->bf);
					fprintf(outfile, "CBT %d번 노드 = %d \tbf = %d\n", index, temp->lchild->data, temp->lchild->bf);
					count++;
				}
			}
			index++;
			//printf("count %d index %d\n", count, index);
		}
	}
}

void LL(avlpointer child, avlpointer temp, avlpointer parent) {
	avlpointer root = parent->parent;
	if (root == NULL) {
		tree = temp;
	}
	else if (root->rchild == parent) {
		root->rchild = temp;
	}
	else {
		root->lchild = temp;
	}
	temp->parent = root;

	int h = parent->rnum;
	parent->lchild = temp->rchild;
	if (temp->rchild != NULL) {
		temp->rchild->parent = parent;
	}

	temp->rchild = parent;
	parent->parent = temp;

	parent->lnum = h;
	temp->rnum = h + 1;
	temp->lnum = h + 1;
	parent->bf = 0;
	temp->bf = 0;
}

void RR(avlpointer child, avlpointer temp, avlpointer parent) {
	avlpointer root = parent->parent;
	if (root == NULL) {
		tree = temp;
	}
	else if (root->rchild == parent) {
		root->rchild = temp;
	}
	else {
		root->lchild = temp;
	}
	temp->parent = root;

	int h = parent->lnum;
	parent->rchild = temp->lchild;
	if (temp->lchild != NULL) {
		temp->lchild->parent = parent;
	}

	temp->lchild = parent;
	parent->parent = temp;

	parent->rnum = h;
	temp->rnum = h + 1;
	temp->lnum = h + 1;
	parent->bf = 0;
	temp->bf = 0;
}

void LR(avlpointer child, avlpointer temp, avlpointer parent) {
	//printf("\n\n%d %d %d\n\n", child->data, temp->data, parent->data);
	avlpointer root = parent->parent;
	if (root == NULL) {
		tree = child;
	}
	else if (root->rchild == parent) {
		root->rchild = child;
	}
	else {
		root->lchild = child;
	}
	child->parent = root;

	int h = parent->rnum;
	temp->rchild = child->lchild;
	if (child->lchild != NULL) {
		child->lchild->parent = temp;
	}
	child->lchild->parent = temp;
	temp->rnum = child->lnum;
	temp->bf = (temp->lnum - temp->rnum);

	parent->lchild = child->rchild;
	if (child->rchild != NULL) {
		child->rchild->parent = parent;
	}
	parent->lnum = child->rnum;
	parent->bf = (parent->lnum - parent->rnum);

	child->lchild = temp;
	temp->parent = child;

	child->rchild = parent;
	parent->parent = child;

	child->lnum = h + 1;
	child->rnum = h + 1;
	child->bf = 0;
}

void RL(avlpointer child, avlpointer temp, avlpointer parent) {
	avlpointer root = parent->parent;
	if (root == NULL) {
		tree = child;
	}
	else if (root->rchild == parent) {
		root->rchild = child;
	}
	else {
		root->lchild = child;
	}
	child->parent = root;

	int h = parent->lnum;
	temp->lchild = child->rchild;
	if (child->rchild != NULL) {
		child->rchild->parent = temp;
	}
	child->rchild->parent = temp;
	temp->lnum = child->rnum;
	temp->bf = (temp->lnum - temp->rnum);

	parent->rchild = child->lchild;
	if (child->lchild != NULL) {
		child->lchild->parent = parent;
	}
	parent->rnum = child->lnum;
	parent->bf = (parent->lnum - parent->rnum);

	child->rchild = temp;
	temp->parent = child;

	child->lchild = parent;
	parent->parent = child;

	child->lnum = h + 1;
	child->rnum = h + 1;
	child->bf = 0;
}

void checkRotation(avlpointer child, avlpointer temp, avlpointer parent) {
	//printf("parent %d, temp %d, child %d ", parent->data, temp->data, child->data);
	if (parent->lchild == temp) {
		if (temp->lchild == child) {
			//printf("LL ");
			LL(child, temp, parent);
		}
		else if (temp->rchild == child) {
			//printf("LR ");
			LR(child, temp, parent);
		}
	}
	else if (parent->rchild == temp) {
		if (temp->lchild == child) {
			//printf("RL ");
			RL(child, temp, parent);
		}
		else if (temp->rchild == child) {
			//printf("RR ");
			RR(child, temp, parent);
		}
	}
}

void checkBf(avlpointer temp) {
	//printf("checkBf ");
	avlpointer child = temp;
	int bfCheck = 0;
	//printf(" !!%d ", temp->data);
	for (avlpointer parent = temp->parent; parent; parent = parent->parent) {
		bfCheck++;
		if (parent->rchild == temp) {
			if (parent->rnum < bfCheck) {
				parent->rnum = bfCheck;
				if ((parent->lnum - parent->rnum) <= -2 || (parent->lnum - parent->rnum) >= 2) {
					checkRotation(child, temp, parent);
					return;
				}
				else {
					//printf("%d ", parent->data);
					parent->bf = parent->lnum - parent->rnum;
					child = temp;
					temp = parent;
				}
			}
			else {
				child = temp;
				temp = parent;
				//printf("3@%d@ ", parent->data); 
			}
		}
		else if (parent->lchild == temp) {
			if (parent->lnum <= bfCheck) {
				parent->lnum = bfCheck;
				if ((parent->lnum - parent->rnum) <= -2 || (parent->lnum - parent->rnum) >= 2) {
					checkRotation(child, temp, parent);
					return;
				}
				else {
					//printf("%d ", parent->data);
					parent->bf = parent->lnum - parent->rnum;
					child = temp;
					temp = parent;
				}
			}
			else {
				child = temp;
				temp = parent;
				//printf("1@%d@ ", parent->data);
			}
		}
		//else { printf("2@%d@ (%d, %d, %d) ", parent->data ,temp->parent->data, parent->lchild->data, parent->rchild->data); }
	}
	//printf("!! ");
}

void avlInsert(int data, avlpointer tree) {
	//printf("avlInsert ");
	avlpointer node = tree;
	avlpointer temp = malloc(sizeof(*temp));
	temp->lchild = NULL;
	temp->rchild = NULL;
	temp->data = data;
	temp->bf = 0;
	temp->lnum = 0;
	temp->rnum = 0;
	if (node->data > data) {
		//printf("!%d 보다 %d 가 작다!\n", node->data, data);
		if (node->lchild == NULL) {
			node->lchild = temp;
			temp->parent = node;
			checkBf(temp);
		}
		else {
			node = node->lchild;
			//printf("@");
			avlInsert(data, node);
		}
	}
	else if (node->data < data) {
		//printf("!%d 보다 %d 가 크다!\n", node->data, data);
		if (node->rchild == NULL) {
			node->rchild = temp;
			temp->parent = node;
			checkBf(temp);
		}
		else {
			node = node->rchild;
			//printf("@");
			avlInsert(data, node);
		}
	}
}

void main(int argc, char* argv[]) {
	FILE* infile, * outfile;
	infile = fopen(argv[1], "r");
	outfile = fopen(argv[2], "w");

	int n;
	fscanf(infile, "%d", &n);

	printf("input\n\n%d\n", n);

	int data;
	fscanf(infile, "%d", &data);
	printf("%d ", data);

	tree = malloc(sizeof(*tree));
	tree->bf = 0;
	tree->data = data;
	tree->lnum = 0;
	tree->rnum = 0;
	tree->lchild = NULL;
	tree->rchild = NULL;
	tree->parent = NULL;

	for (int i = 0; i < n - 1; i++) {
		fscanf(infile, "%d", &data);
		printf("%d ", data);
		avlInsert(data, tree);
	}

	printf("\n\noutput\n\n");

	avlpointer temp;
	printAvl(n, outfile);

	fclose(infile);
	fclose(outfile);
}
