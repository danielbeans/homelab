#!/bin/bash

# Set basic 755 and 644 folder and file permissions and user:group ownership

# Check if user, group, and path arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <user> <group> <path>"
    exit 1
fi

# Dependency Check: Ensure 'acl' is installed
if ! command -v getfacl &> /dev/null; then
    echo "Error: 'acl' package (getfacl/setfacl) is not installed."
    read -p "Would you like to install it now? (y/n): " confirm
    if [[ $confirm == [yY] ]]; then
        sudo apt update && sudo apt install -y acl
    else
        echo "Aborting. ACL is required for the undo functionality."
        exit 1
    fi
fi

USER=$1
GROUP=$2
TARGET_PATH=$3

# Check if the directory exists
if [ ! -d "$TARGET_PATH" ]; then
    echo "Error: Directory $TARGET_PATH does not exist."
    exit 1
fi

BACKUP_FILE="$TARGET_PATH/.permissions_backup.acl"
echo "Creating permissions backup at $BACKUP_FILE..."
sudo getfacl -R "$TARGET_PATH" > "$BACKUP_FILE"

echo "Applying permissions for $USER:$GROUP in $TARGET_PATH"

sudo chown -R "$USER:$GROUP" "$TARGET_PATH"
sudo find "$TARGET_PATH" -type d -exec chmod 755 {} +
sudo find "$TARGET_PATH" -type f -exec chmod 664 {} +

echo "----------------------------------------------------------"
echo "Permissions updated successfully!"
echo "To UNDO these changes, run the following command:"
echo "sudo setfacl --restore=$BACKUP_FILE"
echo "----------------------------------------------------------"
