matmat.bin: matmat.cpp
	g++ -std=c++11 -Wall -Wextra -O2 matmat.cpp -lblas -o matmat.bin

.PHONY: clean run

run: matmat.bin
	./matmat.bin

clean:
	rm -f matmat.bin
