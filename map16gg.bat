:start
set current_dir=G:\�������\game
pushd %current_dir% 
javac *.java
java Raft -p 12345 -i t6.in
goto start
