import sys
import shutil
import os

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
                print(f"{command[5:]} is a shell built-in")
            elif path := shutil.which(command[5:]):
                print(f"{command[5:]} is {path}")
            else:
                print(f"{command[5:]}: not found")
        else:
            print(f"{command}: command not found")

        pass


if __name__ == "__main__":
    main()
