#!/bin/bash

SSH_KEY="/home/alex/.ssh/id_alexlock"

PRIVATE_SERVER="alex@10.128.0.32"

if ssh -i $SSH_KEY $PRIVATE_SERVER "echo 'Connection successful'"; then
    echo "Successfully connected to private server"
    
    echo "Starting package update..."
    ssh -i $SSH_KEY $PRIVATE_SERVER "sudo apt-get update"
    
    echo "Update completed"
else
    echo "Failed to connect to private server"
    exit 1
fi