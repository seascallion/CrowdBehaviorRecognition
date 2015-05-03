opencv_createsamples -info data/images/samples.dat -vec data/images/samples.vec -w 20 -h 20
opencv_traincascade -data data/images/data -vec data/images/samples.vec -bg data/images/background.dat
