# Docker Setup for Gym Tracker and bot

The docker images for tracker and bot are built seperately. Depending on which you are building for, you just need to change the execute command in Dockerfile.

To build docker image, run:
```bash
docker build -t gym-bot .
