:start
set current_dir=G:\�������\game
pushd %current_dir% 
javac *.java
java Raft -p 12347 -i t8.in
goto start