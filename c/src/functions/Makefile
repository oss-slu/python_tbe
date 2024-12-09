CC = clang
CFLAGS = -Wall -Wextra -g
TARGET = strip_header_test
SRC = strip_header.c test.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $(SRC)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
