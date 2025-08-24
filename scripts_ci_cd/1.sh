#!/bin/bash



# Set default key path
KEY_PATH="$HOME/.ssh/id_rsa"

# Get username and server URL
USERNAME=$(whoami)
read -p "Enter the server URL: " SERVER_URL

echo "Username: $USERNAME"
echo "Server URL: $SERVER_URL"

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
# ssh-add "$KEY_PATH"

# Display the public key
# echo -e "\nYour public SSH key:"
# cat "${KEY_PATH}.pub"

ssh-copy-id -i "$HOME/.ssh/id_rsa.pub $USERNAME@$SERVER_URL"

echo -e "\nAdd the PRIVATE key to your Git hosting service."

echo -e "\nYour PRIVATE SSH key:\n"
cat "${KEY_PATH}"


# apos isso o SSH deve estar configurado conrretamente