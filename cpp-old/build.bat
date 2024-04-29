@echo off

rem Compile individual source files
g++ -c main.cpp -o main.o
g++ -c utils.cpp -o utils.o
g++ -c scheduler.cpp -o scheduler.o
g++ -c process.cpp -o process.o

rem Link object files into an executable
g++ main.o utils.o scheduler.o process.o -o my_program

rem Clean up intermediate object files (optional)
del main.o utils.o scheduler.o process.o

rem Pause the script to view any error messages
pause
