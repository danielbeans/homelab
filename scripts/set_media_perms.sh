#!/bin/bash

# Set basic 755 and 644 folder and file permissions and user:group ownership

# Check if both user and group arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <user> <group>"
    exit 1
fi

USER=$1
GROUP=$2

echo "Applying permissions for $USER:$GROUP in the current directory..."

sudo chown -R "$USER:$GROUP" .

sudo find . -type d -exec chmod 755 {} +

sudo find . -type f -exec chmod 664 {} +

echo "Permissions updated successfully!"
