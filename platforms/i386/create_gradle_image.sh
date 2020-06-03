#!/bin/bash
# Since the latest available gradle image for 32 bits is 5.4 and we don't care about the changes between 5.4 and 5.6,
# just create a new image with the expected version tag based on the 5.4 one to be used as a base for the other components.
docker pull i386/gradle:5.4-jdk8
docker tag i386/gradle gradle:5.6.4-jdk8
