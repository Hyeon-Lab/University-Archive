#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define max_variables 10
#define max_terms 1024

typedef struct {
    char term[max_variables + 1];
    int ones_count;
    int covered;
} implicant;

int num_vars;
int max = max_terms;
int minterms[max_terms];
int dont_cares[max_terms];
int num_minterms = 0;
int num_dont_cares = 0;
int level = 0;

implicant** implicant_table;
int num_implicants = 0;

//입력을 받아서 확인하는 함수
void read_input() {

    //입력을 받는 파트
    printf(">> Enter the number of variables: ");
    scanf("%d", &num_vars);

    printf(">> Enter minterm numbers (-1 for end): ");
    int minterm;
    while (scanf("%d", &minterm) == 1 && minterm != -1) {
        minterms[num_minterms++] = minterm;
    }

    printf(">> Enter don't-care term numbers (-1 for end): ");
    int dont_care;
    while (scanf("%d", &dont_care) == 1 && dont_care != -1) {
        dont_cares[num_dont_cares++] = dont_care;
    }

    //입력된 값들을 출력하는 파트
    printf("\ncheck input\n");
    printf("the number of variable : %d\n", num_vars);
    printf("minterm number : ");
    for (int k = 0; k < num_minterms; k++) {
        printf("%d ", minterms[k]);
    }
    printf("\ndon't-care term number : ");
    for (int k = 0; k < num_dont_cares; k++) {
        printf("%d ", dont_cares[k]);
    }
    printf("\n");
}

//int 형식을 받아 이진수로 변환하여 문자열로 리턴하는 함수
char* decimal_to_binary(int num) {
    char* binary = (char*)malloc((num_vars + 1) * sizeof(char));
    for (int i = num_vars - 1; i >= 0; i--) {
        binary[num_vars - 1 - i] = ((num >> i) & 1) ? '1' : '0';
    }
    binary[num_vars] = '\0';
    return binary;
}

//두 이진수 문자열을 받아 1-bit 차이가 나면 그 인덱스값을 리턴하는 함수
int difference(const char* a, const char* b) {
    int diff = 0;
    int index = 0;
    for (int i = 0; i < num_vars; i++) {
        if (a[i] != b[i]) {
            diff++;
            index = i;
        }
    }
    if (diff == 1) {
        return index;
    }
    return -1;
}

//first에서 last까지 저장된 implicants를 group별로 출력 하는 함수
void print_group_implicants(int first, int last) {
    printf("\ngroup classification %d", level++);
    for (int i = 0; i < num_vars + 1; i++) {
        printf("\ngroup %d : ", i);
        for (int j = first; j <last; j++) {
            if (implicant_table[i][j].term && strcmp(implicant_table[i][j].term, "") != 0) {
                printf("%s ", implicant_table[i][j].term);
            }
        }
    }
    printf("\n");
}

//1-bit 차이나는 implicant를 조합하여 다른 implicant를 찾는 함수
void find_implicants(int first, int last) {
    int count = 0;
    for (int i = 0; i < num_vars; i++) {
        for (int j = first; j < last; j++) {
            for (int k = first; k < last; k++) {
                int m = difference(implicant_table[i][j].term, implicant_table[i + 1][k].term);
                if (m != -1) {
                    int l;
                    //두 implicants가 1-bit 차이가 날때, 중복된 결과를 막는 파트
                    for (l = 0; l < count; l++) {
                        int d1 = difference(implicant_table[i][j].term, implicant_table[i][last + l].term);
                        int d2 = difference(implicant_table[i + 1][k].term, implicant_table[i][last + l].term);
                        if (d1 != -1 && d2 != -1) {
                            implicant_table[i][j].covered = 1;
                            implicant_table[i + 1][k].covered = 1;
                            break;
                        }
                    }
                    if (l == count) {
                        //할당된 memory가 부족할때 realloc이후 초기화 하는 파트
                        if (last + count >= max) {
                            max *= 2;
                            for (int x = 0; x < max_variables + 1; x++) {
                                realloc(*(implicant_table + x), sizeof(**implicant_table) * max);
                                for (int j = 0; j < max; j++) {
                                    strcpy(implicant_table[x][j].term, "");
                                    implicant_table[x][j].covered = 0;
                                    implicant_table[x][j].ones_count = 0;
                                }
                            }
                        }
                        //두 implicants가 1-bit 차이가 날때, 그 결과를 저장하는 파트
                        strcpy(implicant_table[i][last + count].term, implicant_table[i][j].term);
                        implicant_table[i][last + count].term[m] = '-';
                        implicant_table[i][last + count].ones_count = implicant_table[i][j].ones_count;
                        count++;
                        num_implicants++;
                        implicant_table[i][j].covered = 1;
                        implicant_table[i + 1][k].covered = 1;
                    }
                }
            }
        }
    }
    //새로 만들어진 implicant가 있으면 출력 후 재귀하는 파트
    if (count != 0) {

        //저장된 implicants를 group별로 출력 하는 파트
        print_group_implicants(last, last + count);

        //추가된 implicant를 조합하여 만들 수 있는 implicant를 찾는 파트
        find_implicants(last, last + count);
    }
}

//quine_mccluskey 
void quine_mccluskey() {
    //implicant table에 memory를 할당하고 초기화 하는 파트
    implicant_table = malloc(sizeof(*implicant_table) * (max_variables + 1));
    for (int i = 0; i < max_variables + 1; i++) {
        *(implicant_table + i) = malloc(sizeof(**implicant_table) * max);
        for (int j = 0; j < max; j++) {
            strcpy(implicant_table[i][j].term, "");
            implicant_table[i][j].covered = 0;
            implicant_table[i][j].ones_count = 0;
        }
    }

    //minterm을 implicant table에 저장하는 파트
    for (int i = 0; i < num_minterms; i++) {
        int ones_count = 0;
        char* term = decimal_to_binary(minterms[i]);
        for (int j = 0; j < num_vars; j++) {
            if (term[j] == '1') {
                ones_count++;
            }
        }
        strcpy(implicant_table[ones_count][i].term, term);
        implicant_table[ones_count][i].ones_count = ones_count;
        free(term);
    }

    //don't-care term을 implicant table에 저장하는 파트
    for (int i = 0; i < num_dont_cares; i++) {
        int ones_count = 0;
        char* term = decimal_to_binary(dont_cares[i]);
        for (int j = 0; j < num_vars; j++) {
            if (term[j] == '1') {
                ones_count++;
            }
        }
        strcpy(implicant_table[ones_count][num_minterms + i].term, term);
        implicant_table[ones_count][num_minterms + i].ones_count = ones_count;
        free(term);
    }

    //implicant table에 저장된 implicant들을 group별로 출력하는 파트
    print_group_implicants(0, num_minterms + num_dont_cares);

    //1-bit차이나는 implicant들을 조합하여 다른 implicant를 찾는 파트
    find_implicants(0, num_minterms + num_dont_cares);
}

typedef struct {
    char term[max_variables + 1];
    int coverNum[max_terms];
    int essential;
} primeImplicant;

primeImplicant* prime_implicants;
int minterms_count[max_terms];
int num_prime_implicants = 0;
int* p;
int cover_count = 0;

//Prime implicant가 minterm을 cover하는 지 확인하는 함수
int find_cover(char* a, int b) {
    char* binary = (char*)malloc((num_vars + 1) * sizeof(char));
    binary = decimal_to_binary(b);
    int diff = 0;
    for (int i = 0; i < num_vars; i++) {
        if (a[i] != binary[i] && a[i] != '-') {
            diff++;
        }
    }
    if (diff) {
        return 0;
    }
    return 1;
}

//Prime implicant chart를 만들어 출력하는 함수
void make_prime_implicant_chart() {
    for (int i = 0; i < num_minterms; i++) {
        printf("%d\t", minterms[i]);
    }
    for (int i = 0; i < num_prime_implicants; i++) {
        printf("\n%s", prime_implicants[i].term);
        for (int j = 0; j < num_minterms; j++) {
            if (minterms_count[j] == -1 || prime_implicants[i].essential == 1) {
                printf("\tX");
            }
            else {
                if (find_cover(prime_implicants[i].term, minterms[j])) {
                    printf("\t%d", find_cover(prime_implicants[i].term, minterms[j]));
                    minterms_count[j]++;
                    prime_implicants[i].coverNum[j] = 1;
                }
                else {
                    printf("\t ");
                }
            }
        }
    }
}

//essential prime implicants를 찾는 함수
void find_Essential_prime_implicants() {
    printf("Essential prime implicants : ");
    for (int i = 0; i < num_minterms; i++) {
        if (minterms_count[i] == 1) {
            for (int j = 0; j < num_prime_implicants; j++) {
                if (prime_implicants[j].coverNum[i] == 1) {
                    printf("%s ", prime_implicants[j].term);
                    prime_implicants[j].essential = 1;
                }
            }
        }
    }
}

//essential과 추가로 선택한 prime implicant가 cover하는 minterm을 확인하는 함수
void find_essential_cover() {
    for (int i = 0; i < num_prime_implicants; i++) {
        if ((prime_implicants + i)->essential == 1) {
            for (int j = 0; j < num_minterms; j++) {
                if ((prime_implicants + i)->coverNum[j] == 1) {
                    minterms_count[j] = -1;
                }
            }
        }
    }
}

// 남은 minterm을 cover하기 위한 Pn을 찾는 함수
void find_p() {
    int x = 0;
    //선택한 prime implicant가 남은 minterms을 모두 cover할때까지 반복
    while (cover_count != num_minterms){
        //p에 memory를 할당하고 초기화 하는 파트
        p = malloc(sizeof(*p) * num_prime_implicants);
        for (int i = 0; i < num_prime_implicants; i++) {
            p[i] = 0;
        }
        //essential prime implicants가 아닌 Pn이 남은 minterm중 몇 개들 cover 하는지 p에 저장하는 파트
        for (int j = 0; j < num_minterms; j++) {
            if (minterms_count[j] != -1) {
                if (x == 0) printf("%d is covered by", minterms[j]);
                for (int i = 0; i < num_prime_implicants; i++) {
                    if ((prime_implicants + i)->essential != 1) {
                        if ((prime_implicants + i)->coverNum[j] == 1) {
                            if (x == 0) printf("P%d ", i);
                            p[i] += 1;
                        }
                    }
                }
                if (x == 0) printf("\n");
            }
        }
        x++;
        //가장 많은 minterm을 cover하는 Pn을 선택하는 파트
        int max_p = 0;
        for (int i = 0; i < num_prime_implicants; i++) {
            if (p[i] >= p[max_p]) {
                max_p = i;
            }
        }
        (prime_implicants + max_p)->essential = 1;

        //선택한 Pn이 cover하는 minterm을 찾는 함수
        find_essential_cover();

        //cover되지 않는 minterm이 있는지 확인하는 파트
        cover_count = 0;
        for (int i = 0; i < num_minterms; i++) {
            if (minterms_count[i] == -1) {
                cover_count++;
            }
        }
    } 
}

//결과 F를 출력하는 함수
void write_output() {
    int x = 0;
    printf("\n>> Minimum Sum-of-Product: F = ");
    for (int i = 0; i < num_prime_implicants; i++) {
        if ((prime_implicants + i)->essential == 1) {
            if (x != 0) {
                printf(" + ");
            }
            x++;
            for (int j = 0; j < num_vars; j++) {
                if ((prime_implicants + i)->term[j] == '0') {
                    printf("%c\'", 'A' + j);
                }
                else if ((prime_implicants + i)->term[j] == '1') {
                    printf("%c", 'A' + j);
                }
            }

        }
    }
}

//petrick's method
int petricks_method() {

    //조합되지 않은 implicants(prime implicants)를 찾아서 prime_implicants에 저장, 출력하는 파트
    int k = 0;
    prime_implicants = malloc(sizeof(*prime_implicants) * num_implicants);
    printf("\nprime implicants\n");
    for (int i = 0; i < num_dont_cares + num_minterms + num_implicants; i++) {
        for (int j = 0; j < num_vars + 1; j++) {
            if (implicant_table[j][i].term && strcmp(implicant_table[j][i].term, "") != 0 && implicant_table[j][i].covered == 0) {
                printf("%s ", implicant_table[j][i].term);
                strcpy((prime_implicants + k++)->term, implicant_table[j][i].term);
                num_prime_implicants++;
            }
        }
    }
    printf("\n\n");
    
    //primte implicant chart를 만들어 출력하는 파트
    printf("Prime_Implicant_Chart\n\n     \t");
    make_prime_implicant_chart();
    printf("\n\n");

    //essential prime implicants 찾아서 출력하는 파트
    find_Essential_prime_implicants();
    printf("\n");

    //essential prime implicant가 cover 하는 minterm을 X로 바꿔 chart로 출력하는 파트
    find_essential_cover();
    printf("Prime_Implicant_Chart(after essential prime implicants)\n\n     \t");
    make_prime_implicant_chart();
    printf("\n\n");
    
    //남은 minterm을 cover할 수 있는 prime implicants 찾는 파트
    find_p();

    //결과를 출력하는 파트
    write_output();
}

int main() {
    read_input();
    quine_mccluskey();
    petricks_method();
    return 0;
}