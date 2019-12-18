# launcher.sh
# This bash script will be run when the Rasberry Pi starts

cd /

#address of the repository
cd home/pi/Desktop/data-processor 

# runs main module of the application using python3
python3 Application.py # sudo may be needed depending on user

cd /