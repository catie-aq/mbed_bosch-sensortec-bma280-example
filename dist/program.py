#!/usr/bin/env python
import os
import argparse

# Check args
parser = argparse.ArgumentParser(description='Program elf binary to board')
parser.add_argument("mcu", help="Reference of the MCU to flash")
parser.add_argument("elf_file", help="Path to the elf file")
parser.add_argument("--probe", default="jlink", help="The programming method to use: st-link or jlink")
args = parser.parse_args()

script_dirname = os.path.dirname(os.path.abspath(__file__))

if args.probe == "jlink":
    elf_path = os.path.abspath(args.elf_file).replace("\\","/").replace(".elf",".bin")

    #create the JLink command file
    command_file_content = "si 1\n\
speed 4000\n\
r\n\
h\n\
loadfile {},0x08000000\n\
r\n\
q\n".format(elf_path)
    command_file = open(os.path.join(script_dirname, "jlink_command_file.jlink").replace("\\", "/"), 'w')
    command_file.write(command_file_content)
    command_file.close()

    command_path = os.path.join(script_dirname, "jlink_command_file.jlink").replace("\\", "/")

    # Flash target
    if os.name == 'nt':
	executable = 'JLink.exe'
    else:
	executable = 'JLinkExe'
    cmd = executable + ' -Device {} -if JTAG -CommanderScript {} '.format(args.mcu, command_path)
    ret = os.system(cmd)
    if ret != 0 and os.name == 'nt':
	print "Error when calling JLink executable. Please verify that JLink.exe has been added to the PATH"

    os.remove(command_path)

if args.probe == "st-link":
    elf_path = os.path.abspath(args.elf_file).replace("\\","/")
    config_path = os.path.join(script_dirname, "openocd.cfg").replace("\\", "/")

    if "STM32L4" in args.mcu:
        openocd_cli_args = " -f interface/stlink-v2-1.cfg -c \"transport select hla_swd\"\
                -f target/stm32l4x.cfg -c \"reset_config srst_only srst_nogate\""
        
        # Flash target
        cmd = "openocd" + openocd_cli_args + ' -c "program {} verify reset exit"'.format(elf_path)
        ret = os.system(cmd)
        if ret != 0 and os.name == 'nt':
	    print "Error when calling openocd executable. Please verify that openocd has been added to the PATH"

    else:  # use the config file of the project
        print "Unknown target, using openocd.cfg configuration file of the project"
	print
        
        # Flash target
        cmd = 'openocd -f openocd.cfg -c "program {} verify reset exit"'.format(config_path, elf_path)
        ret = os.system(cmd)
        if ret != 0 and os.name == 'nt':
	    print "Error when calling openocd executable. Please verify that openocd has been added to the PATH"
