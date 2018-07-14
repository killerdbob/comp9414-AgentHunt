:start
set current_dir=G:\³ÌĞòÉè¼Æ\game
pushd %current_dir% 
javac *.java
java Raft -p 12340 -i t2.in
goto start