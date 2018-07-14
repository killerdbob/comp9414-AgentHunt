set current_dir=D:\javaproject\src
pushd %current_dir% 
javac *.java
java Agent -p 12343
pause