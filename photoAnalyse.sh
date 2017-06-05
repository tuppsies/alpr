#~ /bin/bash

location=$1
storage=$2

echo Beginning photo image analysis...

# split each picture into smaller pictures
echo Splitting picture into fragments...

IMAGES="$location/*.jpg"

echo $storage

for file in $IMAGES
do
	filename=$(basename "$file")
	filename="${filename%.*}"
	echo $filename
	for size in 3 4 5
	do
		convert $file -crop $size'x'$size@ +repage +adjoin "$storage/$filename-size-$size.jpg"
		echo $size
	done
	echo Converted a picture
done

#echo "Calling python script to analyse images for number plates..."
#python3 /home/pi/LicensePlateRecognition/analyse.py "$dir/tmp" "p"

echo Complete

