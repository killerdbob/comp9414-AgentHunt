:start
set current_dir=G:\�������\game
pushd %current_dir% 
javac *.java
java Raft -p 12343 -i t0.in
goto start