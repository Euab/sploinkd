CXX = g++
CXXFLAGS := -std=c++14 -Wall -g

OUT ?= ./bin
TARGET := myAwesomeApplication

SRC := $(wildcard src/*.cpp)
OBJS := $(SRC:%=$(OUT)/%.o)

MKDIR ?= mkdir -p
RM ?= rm -rf

// START-USE-INCLUDE
INCLUDE := ./include
INCLUDE_FLAGS = $(addprefix -I, $(INCLUDE))

CXXFLAGS := $(INCLUDE_FLAGS)
// END-USE-INCLUDE

.PHONY: clean all

$(OUT)/$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $@

$(OUT)/%.cpp.o: %.cpp
	$(MKDIR) $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	$(RM) $(BUILD_DIR)
