#!/usr/bin/env python

# Copyright (c) 2017, CATIE, All Rights Reserved
# SPDX-License-Identifier: Apache-2.0
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import argparse

# Check args
parser = argparse.ArgumentParser(description='Program elf binary to board')
parser.add_argument("elf_file", help="Path to the elf file")
args = parser.parse_args()

elf_path = os.path.abspath(args.elf_file).replace("\\","/")

script_dirname = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dirname, "openocd.cfg").replace("\\", "/")

# Flash target
cmd = 'openocd -f {} -c "program {} verify reset exit"'.format(config_path, elf_path)
os.system(cmd)
