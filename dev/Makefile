CC = g++
TARGET = test
SRCS = main_new.cpp
OBJS = $(SRCS:.cpp=.o)
DLIBS = -lopencv_core -lopencv_imgproc -lopencv_highgui
$(TARGET):$(OBJS)
	$(CC) -o $@ $^ $(DLIBS)  

clean:
	rm -rf $(TARGET) $(OBJS)

%.o:%.cpp
	$(CC) -o $@ -c $<
