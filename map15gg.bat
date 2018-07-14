:start
set current_dir=G:\³ÌĞòÉè¼Æ\game
pushd %current_dir% 
javac *.java
java Raft -p 12344 -i t5.in
goto start