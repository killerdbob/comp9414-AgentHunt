:start
set current_dir=G:\�������\game
pushd %current_dir% 
javac *.java
java Raft -p 12344 -i t5.in
goto start