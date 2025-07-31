#include <stdio.h>
#include <stdlib.h>
#define max 100

// Функция вывода матрицы
void matoutput(int **matrix, int r, int c) {
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            printf("%d", matrix[i][j]);
            if (j < c - 1)
                printf(" ");
        }
        if (i < r - 1)
            printf("\n");
    }
}

// Функция ввода матрицы
int matinput(int **matrix, int r, int c) {
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            if (scanf("%d", &matrix[i][j]) != 1)
                return 0;
        }
    }
    return 1;
}

// 1. Статическое выделение
void f1static() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r > max || c > max || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    static int static_matrix[max][max];
    int *p[max];
    for (int i = 0; i < r; i++) {
        p[i] = static_matrix[i];
    }

    if (!matinput(p, r, c)) {
        printf("n/a");
        return;
    }

    matoutput(p, r, c);
}

// 2. Одним malloc-ом
void s2method() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    int **single_array_matrix = malloc(r * sizeof(int*) + r * c * sizeof(int));
    if (!single_array_matrix) {
        printf("n/a");
        return;
    }

    int *ptr = (int*)(single_array_matrix + r);
    for (int i = 0; i < r; i++)
        single_array_matrix[i] = ptr + c * i;

    if (!matinput(single_array_matrix, r, c)) {
        printf("n/a");
        free(single_array_matrix);
        return;
    }

    matoutput(single_array_matrix, r, c);
    free(single_array_matrix);
}

// 3. Отдельный malloc на каждую строку
void t3method() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    int **pointer_array = malloc(r * sizeof(int*));
    if (!pointer_array) {
        printf("n/a");
        return;
    }

    for (int i = 0; i < r; i++) {
        pointer_array[i] = malloc(c * sizeof(int));
        if (!pointer_array[i]) {
            for (int j = 0; j < i; j++)
                free(pointer_array[j]);
            free(pointer_array);
            printf("n/a");
            return;
        }
    }

    if (!matinput(pointer_array, r, c)) {
        printf("n/a");
        for (int i = 0; i < r; i++)
            free(pointer_array[i]);
        free(pointer_array);
        return;
    }

    matoutput(pointer_array, r, c);

    for (int i = 0; i < r; i++)
        free(pointer_array[i]);
    free(pointer_array);
}

// 4. Отдельный malloc на указатели и на данные
void f4method() {
    int r, c;
    if (scanf("%d %d", &r, &c) != 2 || r <= 0 || c <= 0) {
        printf("n/a");
        return;
    }

    int **pointer_array = malloc(r * sizeof(int*));
    int *values_array = malloc(r * c * sizeof(int));

    if (!pointer_array || !values_array) {
        free(pointer_array);
        free(values_array);
        printf("n/a");
        return;
    }

    for (int i = 0; i < r; i++)
        pointer_array[i] = values_array + i * c;

    if (!matinput(pointer_array, r, c)) {
        printf("n/a");
        free(values_array);
        free(pointer_array);
        return;
    }

    matoutput(pointer_array, r, c);
    free(values_array);
    free(pointer_array);
}

// Меню
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
