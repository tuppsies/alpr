if [ $# -eq 0 ]
    then
        echo "ERROR: supply the IP address of the drive to mount"
        exit
fi

sudo sshfs -o allow_other,default_permissions joshua@$1:/ /media/laptop
