# Melilapse-Client

Python based script to take pictures

## Features

- Taking pictures with a webcam
- Only taking pictures during the day (or night!)
- Taking pictures during the golden hour
- Local and remote output options
- Either a simple script or part of a larger deployment

## Installation

1. make /var/python directory
2. Clone repo to /var/python/Melilapse-Client
3. copy example.env to .env
4. edit .env to fit environment
5. run setup.sh to create venv and populate with requirements
6. use cron to execute /var/python/Melilapse-Client/melilapse.sh at your interval
7. Collect images and enjoy!

## Output

### Local Output

Melilapse Client supports first and foremost a local output of jpg files. Point the .env to your directory and watch it fill up

### Remote output

Eventually melilapse client will support multiple remote targets (storage, S3, etc...)

## Configuration

### Base config

Basic config is controlled by the .env file. Please see example file to check syntax

### Remote config

Upon release of Melilapse Server a remote config option will be available for cloud based control of time lapse cameras.