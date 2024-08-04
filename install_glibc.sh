#!/bin/bash

# Update and install dependencies
apt-get update && \
    apt-get install -y wget build-essential python3 python3-pip

# Download glibc 2.29
wget http://ftp.gnu.org/gnu/libc/glibc-2.29.tar.gz && \
    tar -xzf glibc-2.29.tar.gz

# Build and install glibc 2.29
cd glibc-2.29 && \
    mkdir build && cd build && \
    ../configure --prefix=/usr/local/glibc-2.29 && \
    make -j$(nproc) && \
    make install

# Clean up
cd ../.. && \
    rm -rf glibc-2.29 glibc-2.29.tar.gz

# Export environment variables
echo 'export LD_LIBRARY_PATH=/usr/local/glibc-2.29/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PATH=/usr/local/glibc-2.29/bin:/usr/local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install Python dependencies
pip3 install -r requirements.txt
