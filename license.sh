#!/bin/bash

# Get the MAC address of the first Ethernet interface
mac_address=$(ip link show ens192 | awk '/ether/ {print $2}')

# Generate a license key based on the MAC address
license_key=$(echo -n "$mac_address" | sha256sum | awk '{print $1}')

# Save the license key to a file
license_text=$(curl -s -X POST -d "input_string=$mac_address" http://SERVER_IP:5000/validate)
license_filename="/etc/init.d/license.key"

if [ ! -f "$license_filename" ]; then
    echo "$license_text" > "$license_filename"
    logger "License content is written to $license_filename."
else
	logger "File $license_filename is already exists or corrupted. Skipping content write."
fi

#Check License if present and stop services if isn't present
key_content=$(<"$license_filename")

if [[ "$key_content" == "$license_key" ]]; then
    logger "License Key is validated and Good"

else
    logger "Invalid or corrupted license file"
    #systemctl stop serviceA
    #systemctl stop serviceB
fi
