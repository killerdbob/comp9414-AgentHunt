:start
set current_dir=G:\³ÌĞòÉè¼Æ\game
pushd %current_dir% 
javac *.java
java Raft -p 12349 -i t1.in
goto start