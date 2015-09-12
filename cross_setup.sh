echo "The script is starting"
# CROSS=~/pi-tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf
# echo "cross = $CROSS"
# export CC=$CROSS-gcc
# export CXX=$CROSS-g++
# export LD=$CROSS-ld
# export AR=$CROSS-ar
# export RANLIB=$CROSS-ranlib
export CXX=/usr/bin/arm-linux-gnueabi-g++-4.7
export CC=/usr/bin/arm-linux-gnueabi-gcc-4.7
export AR=/usr/bin/arm-linux-gnueabi-ar
export LD=/usr/bin/arm-linux-gnueabi-ld

echo "done with script?"
