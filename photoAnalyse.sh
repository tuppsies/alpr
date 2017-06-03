#~ /bin/bash

dir=/home/pi/LicensePlateRecognition/photoAnalysis/data

echo Beginning photo image analysis...

echo Removing directories...
rm -r $dir/tmp

echo Creating directories...
mkdir $dir/tmp

# split each picture into smaller pictures and store them in tmp2
echo Splitting picture into fragments...
convert $1 -crop 3x3@ +repage +adjoin "$dir/tmp/image$counter%02d.jpg"

echo "Calling python script to analyse images for number plates..."
python3 /home/pi/LicensePlateRecognition/analyse.py "$dir/tmp" "p"

echo Complete

