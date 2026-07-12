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
        parts=shlex.split(command)
        if parts[0] == "exit":
            break
        elif parts[0]=="echo":
            print(" ".join(parts[1:]))
        elif parts[0] =="type":
            if command[5:] in BUILT_IN:
                print(f"{command[5:]} is a shell builtin")
            elif path := shutil.which(command[5:]):
                print(f"{command[5:]} is {path}")
            else:
                print(f"{command[5:]}: not found")
        elif path := shutil.which(parts[0]):
            exec_path=path
            subprocess.run(parts, executable=exec_path)
        elif command == "pwd":
            print(os.getcwd())
        elif parts[0]=="cd":
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
