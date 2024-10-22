CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2

TARGET = matvec
SRCS = matvec.cpp

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^

run: $(TARGET)
	./$(TARGET)

.PHONY: clean

clean:
	rm -f $(TARGET)
