#include <stdio.h>
#include <stdlib.h>
#define MAX 100

void matoutput(int **matrix, int r, int c) {
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            printf("%d", matrix[i][j]);
            if (j < c - 1) printf(" ");
        }
        printf("\n");
    }
}

int matinput(int **matrix, int r, int c) {
    for (int i = 0; i < r; i++)
        for (int j = 0; j < c; j++)
            if (scanf("%d", &matrix[i][j]) != 1) return 0;
    return 1;
}

void print_array(int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d", arr[i]);
        if (i < size - 1) printf(" ");
    }
}

void process_matrix(int **matrix, int r, int c) {
    int max_rows[r];
    int min_cols[c];

    for (int i = 0; i < r; i++) {
        max_rows[i] = matrix[i][0];
        for (int j = 1; j < c; j++) {
            if (matrix[i][j] > max_rows[i])
                max_rows[i] = matrix[i][j];
        }
    }

    for (int j = 0; j < c; j++) {
        min_cols[j] = matrix[0][j];
        for (int i = 1; i < r; i++) {
            if (matrix[i][j] < min_cols[j])
                min_cols[j] = matrix[i][j];
        }
    }

    print_array(max_rows, r);
    printf("\n");
    print_array(min_cols, c);
}

// --- Статическое выделение
void f1static() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r > MAX || c > MAX || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    static int matrix[MAX][MAX];
    int *p[MAX];
    for (int i = 0; i < r; i++) p[i] = matrix[i];

    if (!matinput(p, r, c)) {
        printf("n/a");
        return;
    }

    matoutput(p, r, c);
    process_matrix(p, r, c);
}

// --- Один malloc
void s2method() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    int **matrix = malloc(r * sizeof(int*) + r * c * sizeof(int));
    if (!matrix) {
        printf("n/a");
        return;
    }

    int *data = (int*)(matrix + r);
    for (int i = 0; i < r; i++)
        matrix[i] = data + i * c;

    if (!matinput(matrix, r, c)) {
        printf("n/a");
        free(matrix);
        return;
    }

    matoutput(matrix, r, c);
    process_matrix(matrix, r, c);
    free(matrix);
}

// --- Несколько malloc (строки отдельно)
void t3method() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    int **matrix = malloc(r * sizeof(int*));
    if (!matrix) {
        printf("n/a");
        return;
    }

    for (int i = 0; i < r; i++) {
        matrix[i] = malloc(c * sizeof(int));
        if (!matrix[i]) {
            for (int j = 0; j < i; j++) free(matrix[j]);
            free(matrix);
            printf("n/a");
            return;
        }
    }

    if (!matinput(matrix, r, c)) {
        printf("n/a");
        for (int i = 0; i < r; i++) free(matrix[i]);
        free(matrix);
        return;
    }

    matoutput(matrix, r, c);
    process_matrix(matrix, r, c);
    for (int i = 0; i < r; i++) free(matrix[i]);
    free(matrix);
}

// --- malloc указателей и массива значений
void f4method() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    int **matrix = malloc(r * sizeof(int*));
    int *values = malloc(r * c * sizeof(int));
    if (!matrix || !values) {
        free(matrix);
        free(values);
        printf("n/a");
        return;
    }

    for (int i = 0; i < r; i++)
        matrix[i] = values + i * c;

    if (!matinput(matrix, r, c)) {
        printf("n/a");
        free(values);
        free(matrix);
        return;
    }

    matoutput(matrix, r, c);
    process_matrix(matrix, r, c);
    free(values);
    free(matrix);
}

// --- main
int main() {
    int method;
    if (scanf("%d", &method) != 1 || method < 1 || method > 4) {
        printf("n/a");
        return 0;
    }

    switch (method) {
        case 1:
            f1static();
            break;
        case 2:
            s2method();
            break;
        case 3:
            t3method();
            break;
        case 4:
            f4method();
            break;
        default:
            printf("n/a");
    }

    return 0;
}
