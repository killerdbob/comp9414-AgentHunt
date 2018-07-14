:start
set current_dir=D:\javaproject\src
pushd %current_dir% 
javac *.java
java Raft -p 12342 -i s2.in
goto start