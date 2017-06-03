#~ /bin/bash

dir=/home/pi/LicensePlateRecognition/videoAnalysis/data

echo Beginning video image analysis...

echo Removing directories...
rm -r $dir/tmp
rm -r $dir/tmp2

echo Creating directories...
mkdir $dir/tmp
mkdir $dir/tmp2

# split the video into pictures and store them in tmp
echo Converting video to frames...
ffmpeg -i $1 -r $2 $dir/tmp/output_%05d.jpg

# split each picture into smaller pictures and store them in tmp2
cd $dir/tmp/
numFiles=ls -1 | wc -l
echo numFiles is $numFiles
echo Splitting frames into fragments...

counterTwo=0
for NUMBER in 2 3 4
do
    counter=0
    for IMAGE in $dir/tmp/*.jpg
    do
        convert $IMAGE -crop ${NUMBER}x${NUMBER}@ +repage +adjoin "$dir/tmp2/image$counterTwo$counter%02d.jpg"
        let counter++
    done
    echo Splitting into $NUMBER complete
    let counterTwo++
done

echo "Calling python script to analyse images for number plates..."
python3 /home/pi/LicensePlateRecognition/analyse.py "$dir/tmp2" "v"


echo Complete

