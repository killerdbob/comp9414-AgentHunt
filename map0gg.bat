:start
set current_dir=D:\javaproject\src
pushd %current_dir% 
javac *.java
java Raft -p 12340 -i s0.in
goto start