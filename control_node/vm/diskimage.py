#!/usr/bin/env python

import os.path
import subprocess


# Simple structure to represent a disk image based on a qcow2 file format.
class DiskImage(object):

    def __init__(self, disk_image_filepath):
        self.filepath = os.path.abspath(disk_image_filepath)

    def create_linked_qcow2_image(self, destination_disk_image_filepath):
        """ Creates a new qcow2 image referencing the current image. """

        # Check if the source disk image file exists.
        if not os.path.exists(self.filepath):
            raise Exception("Source image file does not exist (%s)." % self.filepath)

        # Check if the new disk image file already exists.
        if os.path.exists(destination_disk_image_filepath):
            # This is an error, as we don't want to overwrite an existing disk image with a source.
            raise Exception("Destination image file already exists (%s). Will not overwrite existing image." % destination_disk_image_filepath)

        # We need to use the qemu-img command line tool for this.
        # Note that we set the source file as its backing file. This is stored in the qcow2 file.
        # Note that we also use 4K as the cluster size, since it seems to be the best compromise.
        print "Creating qcow2 image %s based on source image %s..." % (destination_disk_image_filepath, self.filepath)
        image_tool_command = 'qemu-img create -f qcow2 -o backing_file=%s,cluster_size=4096 %s' \
                           % (self.filepath, destination_disk_image_filepath)
        self.__run_image_creation_tool(image_tool_command)
        print 'New disk image created.'

        cloned_disk_image = DiskImage(destination_disk_image_filepath)
        return cloned_disk_image

    def __run_image_creation_tool(self, image_tool_command):
        """ Starts the image creation tool in a separate process, and waits for it."""
        tool_pipe = subprocess.PIPE
        tool_process = subprocess.Popen(image_tool_command, shell=True, stdin=tool_pipe, stdout=tool_pipe, stderr=tool_pipe)
        normal_output, error_output = tool_process.communicate()

        # Show errors, if any.
        if len(error_output) > 0:
            print error_output

        # Show output, if any.
        if len(normal_output) > 0:
            print normal_output
