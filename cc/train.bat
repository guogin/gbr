"C:\Users\kol\Documents\opencv\opencv-3.4.8\build\bin\Release\opencv_traincascade.exe" -data m/ -vec samples.vec -bg n/negatives.txt -numPos 1000 -numNeg 1000 -numStages 10 -mode ALL -w 80 -h 80 -minHitRate 0.999 -maxFalseAlarmRate 0.3 -mem 512 -numThreads 40