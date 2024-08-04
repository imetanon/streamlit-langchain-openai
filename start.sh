#!/bin/bash

# Set environment variables
export LD_LIBRARY_PATH=/usr/local/glibc-2.29/lib:$LD_LIBRARY_PATH
export PATH=/usr/local/glibc-2.29/bin:/usr/local/bin:$PATH

# Activate the virtual environment
source venv/bin/activate

# Start the Streamlit app
streamlit run Chatbot.py --server.port 8080