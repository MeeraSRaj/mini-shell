import sys
import shutil
import os
import subprocess

BUILT_IN=["exit", "echo", "type"]

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            if command[5:] in BUILT_IN:
                print(f"{command[5:]} is a shell builtin")
            elif path := shutil.which(command[5:]):
                print(f"{command[5:]} is {path}")
            else:
                print(f"{command[5:]}: not found")
        elif path := shutil.which(command.split()[0]):
            exec_path=path
            parts=command.split()
            subprocess.run(parts, executable=exec_path)
        else:
            print(f"{command}: command not found")

        pass


if __name__ == "__main__":
    main()
