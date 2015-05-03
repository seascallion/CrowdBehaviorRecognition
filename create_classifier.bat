opencv_createsamples -info data/images/positive.dat -bg data/images/bg.dat -vec data/images/samples.vec -w 20 -h 20
rm -r data/images/data
mkdir data/images/data
opencv_traincascade -data data/images/data -vec data/images/samples.vec -bg data/images/bg.dat -numPos 200 -numNeg 100 -numStages 10 -w 20 -h 20 -featureType HAAR
