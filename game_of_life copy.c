#include <ncurses.h>
#include <stdio.h>
#define cols 80
#define rows 25
#define max_delay 900000
#define min_delay 10000
#define delay_step 2000

void load_field(int current_matrix[rows][cols]);
void draw_field(int current_matrix[rows][cols]);
int handle_speed_input(int *miliseci);
int count_all_alive_cells(
    int current_matrix[rows][cols]);  // эта функция считать живые клетки на поле и возвращать значение. если
                                      // клеток ноль, игра завершается
int count_alive_neighbours(int current_matrix[rows][cols], int x,
                           int y);  // найдёт координаты соседей клетки и их колво
void new_cell_generation(int current_matrix[rows][cols],
                         int future_matrix[rows][cols]);  // новое поколение клеток такое типо
void copy_last_generation(int current_matrix[rows][cols],
                          int copy_matrix[rows][cols]);  // скопируем предыдущее положение клеток
int generations_equal(int current_matrix[rows][cols],
                      int future_matrix[rows][cols]);  // сравнение поколений. если одинаковое, игра овер
void game();  // в этой функции будет вся игра. в мейне, по факту, нужно будет вызвать ей и прописать ретерн)

int main() {
    game();
    return 0;
}

void game() {
    int current_matrix[rows][cols], future_matrix[rows][cols], copy_matrix[rows][cols];
    int running = 1;
    int miliseci = 200;

    initscr();  // подключаем нкёрсес
    cbreak();  // делаем так чтобы программа не оиждала ввода энтер воооот!!
    noecho();     // скрываем отображение вводимых символов
    curs_set(0);  // это мы курсор скрыли
    nodelay(stdscr, TRUE);
    load_field(current_matrix);  // чтение поля из файла
    nodelay(stdscr, TRUE);
    noecho();  // отключает автоматический вывод символов на экран при вводе с клавиатуры

    while (running) {
        clear();
        draw_field(current_matrix);

        if (handle_speed_input(&miliseci) == 1) {
            running = 0;
        }
        printf("%d", miliseci);
        refresh();        // выводим текущее значение задержки
        napms(miliseci);  // задаётся скорость обновления кадров

        new_cell_generation(current_matrix, future_matrix);
        copy_last_generation(current_matrix, copy_matrix);

        if (count_all_alive_cells(current_matrix) == 0 ||
            generations_equal(current_matrix, copy_matrix) == 1) {
            running = 0;
        }
    }
    endwin();
}

int generations_equal(int current_matrix[rows][cols], int copy_matrix[rows][cols]) {
    int equal = 1;
    for (int i = 0; equal && i < rows; i++) {
        for (int j = 0; equal && j < cols; j++) {
            if (copy_matrix[i][j] != current_matrix[i][j]) {
                equal = 0;
            }
        }
    }
    return equal;
}

void copy_last_generation(int current_matrix[rows][cols], int copy_matrix[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            copy_matrix[i][j] = current_matrix[i][j];
        }
    }
}

void new_cell_generation(int current_matrix[rows][cols], int future_matrix[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (current_matrix[i][j] == 0 && count_alive_neighbours(current_matrix, i, j) == 3) {
                future_matrix[i][j] = 1;
            } else if (current_matrix[i][j] == 1 &&
                       (count_alive_neighbours(current_matrix, i, j) < 2 ||
                        count_alive_neighbours(current_matrix, i, j) > 3)) {
                future_matrix[i][j] = 0;
            } else if (current_matrix[i][j] == 1 &&
                       (count_alive_neighbours(current_matrix, i, j) == 2 ||
                        count_alive_neighbours(current_matrix, i, j) == 3)) {
                future_matrix[i][j] = 1;
            } else {
                future_matrix[i][j] = 0;
            }
        }
    }
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            current_matrix[i][j] = future_matrix[i][j];
        }
    }
}

int count_alive_neighbours(int current_matrix[rows][cols], int x, int y) {
    int count = 0;
    int wrapped_i, wrapped_j;
    for (int i = x - 1; i <= x + 1; i++) {
        for (int j = y - 1; j <= y + 1; j++) {
            wrapped_i = (i + rows) % rows;
            wrapped_j = (j + cols) % cols;
            if ((wrapped_i != x || wrapped_j != y) && current_matrix[wrapped_i][wrapped_j] == 1) {
                count++;
            }
        }
    }
    return count;
}

int count_all_alive_cells(int current_matrix[rows][cols]) {
    int count = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (current_matrix[i][j] == 1) {
                count++;
            }
        }
    }
    return count;
}

void load_field(int current_matrix[rows][cols]) {
    char c;
    for (int y = 0; y < rows; y++) {
        for (int x = 0; x < cols; x++) {
            c = getchar();
            if (c == EOF) {  // eof - end of file конец файла типа ю ноу сигнал что данные закончились
                current_matrix[y][x] = 0;
                x++;
            } else if (c == '1') {
                current_matrix[y][x] = 1;
                x++;
            } else if (c == '0') {
                current_matrix[y][x] = 0;
                x++;
            }
        }
        while (c != '\n' && c != EOF) c = getchar();
    }
}

void draw_field(int current_matrix[rows][cols]) {
    for (int y = 0; y < rows; y++) {
        for (int x = 0; x < cols; x++) {
            char cell =
                current_matrix[y][x] ? 'O' : ' ';  // это тренарный оператор. если клетка жива (не равна 0) то вернуть
                                          // символ 0 а если клетка филд у х == 0 то пробел вот!!
            mvaddch(y, x, cell);  // это крч из нкёрсес функция, объединяет move & addch это для вывода
                                  // симивола на экран в опред позиции
        }
    }
    refresh();
}

int handle_speed_input(int *miliseci) {
    char prkey = getch();                  // читаем один символ с клавиатуры
    if (prkey == ' ') return 1;            // пробел = выход
    if (prkey == 'z' && *miliseci <= 300)  // замедление
        *miliseci += 40;
    if (prkey == 'a' && *miliseci >= 40)  // ускорение
        *miliseci -= 40;
    return 0;
}