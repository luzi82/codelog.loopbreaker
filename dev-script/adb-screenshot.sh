#!/bin/bash

ADB=3rdparty/android-sdk-linux/platform-tools/adb
OUTPUT_DIR=/storage/sdcard1/tmp

${ADB} shell screencap -p ${OUTPUT_DIR}/screen.png
${ADB} pull ${OUTPUT_DIR}/screen.png
${ADB} shell rm ${OUTPUT_DIR}/screen.png
