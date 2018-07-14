:start
set current_dir=D:\javaproject\src
pushd %current_dir% 
javac *.java
java Raft -p 12347 -i s7.in
goto start