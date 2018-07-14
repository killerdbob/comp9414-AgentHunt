:start
set current_dir=D:\javaproject\src
pushd %current_dir% 
javac *.java
java Raft -p 12346 -i s6.in
goto start