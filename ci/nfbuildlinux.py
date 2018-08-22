#!/usr/bin/env python

import fnmatch
import os
import plistlib
import re
import shutil
import subprocess
import sys

from distutils import dir_util
from nfbuild import NFBuild


class NFBuildLinux(NFBuild):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.project_file = os.path.join(
            self.build_directory,
            'NFParam.xcodeproj')

    def generateProject(self,
                        code_coverage=False,
                        address_sanitizer=False,
                        thread_sanitizer=False,
                        undefined_behaviour_sanitizer=False,
                        ios=False):
        cmake_call = [
            'cmake',
            '..',
            '-GUnix Makefiles']
        cmake_result = subprocess.call(cmake_call, cwd=self.build_directory)
        if cmake_result != 0:
            sys.exit(cmake_result)

    def targetBinary(self, target):
        for root, dirnames, filenames in os.walk(self.build_directory):
            for filename in fnmatch.filter(filenames, target):
                full_target_file = os.path.join(root, filename)
                return full_target_file
        return ''

    def buildTarget(self, target, sdk='linux', arch='x86_64'):
        make_result = subprocess.call(['make'], cwd=self.build_directory)
        if make_result != 0:
            sys.exit(make_result)