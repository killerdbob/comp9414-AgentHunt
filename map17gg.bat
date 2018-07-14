:start
set current_dir=G:\³ÌĞòÉè¼Æ\game
pushd %current_dir% 
javac *.java
java Raft -p 12346 -i t7.in
goto start