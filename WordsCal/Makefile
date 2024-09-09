# 编译器
CXX = g++

# 编译选项
CXXFLAGS = -Wall -std=c++11

# 定义目标文件
TARGET = main

# 默认目标
ALL: $(TARGET)

# 编译目标
$(TARGET): main.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) main.cpp

# 清理目标
clean:
	rm -f $(TARGET)