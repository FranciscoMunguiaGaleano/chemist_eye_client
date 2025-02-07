#!/bin/bash

# Directory where audio files are stored
SOUND_DIR="sound/intros"

# Check if the directory exists and contains .ogg files
if [ ! -d "$SOUND_DIR" ] || [ -z "$(ls -A $SOUND_DIR/*.mp3 2>/dev/null)" ]; then
    echo "No audio files found in $SOUND_DIR. Please generate them first."
    exit 1
fi

# Pick a random file from the directory
RANDOM_FILE=$(ls "$SOUND_DIR"/chemisteyethree.mp3 | shuf -n 1)

# Play the selected file
play "$RANDOM_FILE"
