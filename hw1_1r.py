CC = gcc
CFLAGS = -Wall -Wextra -Werror

BUILD_DIR = ../../build
TARGET = $(BUILD_DIR)/Quest_3

SRC = ../../src/main_executable_module/main_executable_module.c \
      ../../src/data_module/data_process.c \
      ../../src/data_libs/data_io.c \
      ../../src/data_libs/data_stat.c

all: $(TARGET)

$(TARGET): $(SRC)
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

rebuild: clean all
