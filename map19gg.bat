:start
set current_dir=G:\�������\game
pushd %current_dir% 
javac *.java
java Raft -p 12348 -i t9.in
goto start