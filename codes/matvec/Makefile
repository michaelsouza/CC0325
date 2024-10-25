matvec.bin: matvec.cpp
	g++ -std=c++11 -Wall -Wextra -O2 matvec.cpp -lblas -o matvec.bin

.PHONY: clean run

run: matvec.bin
	./matvec.bin

clean:
	rm -f matvec.bin
