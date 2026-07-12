import sys
import shutil
import os
import subprocess
import shlex

BUILT_IN=["exit", "echo", "type", "pwd", "cd"]

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo "):
            print(shlex.split(command)[1:])
        elif command.startswith("type "):
            if command[5:] in BUILT_IN:
                print(f"{command[5:]} is a shell builtin")
            elif path := shutil.which(command[5:]):
                print(f"{command[5:]} is {path}")
            else:
                print(f"{command[5:]}: not found")
        elif path := shutil.which(shlex.split(command)[0]):
            exec_path=path
            parts=shlex.split(command)
            subprocess.run(parts, executable=exec_path)
        elif command == "pwd":
            print(os.getcwd())
        elif command.startswith("cd "):
            dir=command[3:]
            if dir=="~":
                dir=os.getenv('HOME')
            try:
                os.chdir(dir)
            except FileNotFoundError:
                print(f"cd: {dir}: No such file or directory")
        else:
            print(f"{command}: command not found")

        pass


if __name__ == "__main__":
    main()
