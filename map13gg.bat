:start
set current_dir=G:\�������\game
pushd %current_dir% 
javac *.java
java Raft -p 12340 -i t4.in
goto start