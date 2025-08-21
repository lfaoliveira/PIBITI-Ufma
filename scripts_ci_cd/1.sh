#!/bin/bash

# Set default key path
KEY_PATH="$HOME/.ssh/ssh_git"

# Generate SSH key pair if it doesn't exist
if [ ! -f "$KEY_PATH" ]; then
    echo "Generating new SSH key pair..."
    ssh-keygen -t rsa -b 4096 -f "$KEY_PATH" -N ""
else
    echo "SSH key pair already exists at $KEY_PATH"
fi

# Start SSH agent if not running
eval "$(ssh-agent -s)"

# Add the key to SSH agent
ssh-add "$KEY_PATH"

# Display the public key
echo -e "\nYour public SSH key:"
cat "${KEY_PATH}.pub"

echo -e "\nAdd this public key to your Git hosting service."