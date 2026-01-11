#!/bin/bash

# Set basic 755 and 644 folder and file permissions and user:group ownership

# Check if user, group, and path arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <user> <group> <path>"
    exit 1
fi

USER=$1
GROUP=$2
TARGET_PATH=$3

USER=$1
GROUP=$2

echo "Applying permissions for $USER:$GROUP in the current directory..."

sudo chown -R "$USER:$GROUP" .

sudo find "$TARGET_PATH" -type d -exec chmod 755 {} +

sudo find "$TARGET_PATH" -type f -exec chmod 664 {} +

echo "Permissions updated successfully for $TARGET_PATH"
