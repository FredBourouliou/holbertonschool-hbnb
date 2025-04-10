#!/bin/bash

# Create images directory if it doesn't exist
mkdir -p static/images

# Download logo and icon
curl -o static/images/logo.png https://raw.githubusercontent.com/Holberton-Uy/hbnb-doc/main/part4/base_files/images/logo.png
curl -o static/images/icon.png https://raw.githubusercontent.com/Holberton-Uy/hbnb-doc/main/part4/base_files/images/icon.png 