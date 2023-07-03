# DIRECTORIES
# src directory
SRC_DIR         :=./src
GTEST_DIR       :=./gtests
OUTPUT_DIR      :=./output
# aditional project libs directory
EXTRA_LIB_DIR   :=
# temporal files directory
TMP_DIR         :=./tmp
SRC_CODE_EXT    :=c
SRC_HEADERS_EXT :=h
MAIN_FILE       :=main.c
# excluded files from the project
EXCLUDED_FILES  :=


# binary file name
BIN_NAME:=bin.out
# binary arguments (if executed by the makefile).
BIN_ARGUMENTS:= 
# compiler
CXX:=gcc
# compilation flags
CXXFLAGS:=-Wall

# [YES/NO]
EXECUTE_AFTER_COMPILATION:=NO
ALLOW_FOR_GNU_DEBUGGER:=NO
# automatic linking from all files under the app directory
AUTOMATIC_LINKING:=YES


include ./make-files/Makefile

.PHONY: config
config:
	@echo "\tConfiguring makefile"
	@./make-files/config.sh

.PHONY: reset
reset:
	@echo "\tReseting makefile configuration"
	@./make-files/config.sh reset



#    __
# __( o)>
# \ <_ ) r90