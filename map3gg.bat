:start
set current_dir=D:\javaproject\src
pushd %current_dir% 
javac *.java
java Raft -p 12343 -i s3.in
goto start