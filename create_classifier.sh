opencv_createsamples -info data/images/hand_classifier/positive.dat -bg data/images/hand_classifier/bg.dat -vec data/images/hand_classifier/samples.vec -w 20 -h 20
rm -r data/images/hand_classifier/cascades
mkdir data/images/hand_classifier/cascades
opencv_traincascade -data data/images/hand_classifier/cascades -vec data/images/hand_classifier/samples.vec -bg data/images/hand_classifier/bg.dat -numPos 200 -numNeg 100 -numStages 10 -w 20 -h 20 -featureType HAAR
