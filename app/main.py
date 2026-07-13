import sys
import shutil
import os
import subprocess
import shlex

BUILT_IN=["exit", "echo", "type", "pwd", "cd"]

def main():
    while True:
        redirect_file=None
        sys.stdout.write("$ ")
        command = input()
        parts=shlex.split(command)
        if ">" in parts:
            idx=parts.index(">")
            redirect_file=parts[idx+1]
            parts=parts[:idx]
        elif "1>" in parts:
            idx=parts.index("1>")
            redirect_file=parts[idx+1]
            parts=parts[:idx]

        if parts[0] == "exit":
            break
        elif parts[0]=="echo":
            output=" ".join(parts[1:])
            if redirect_file:
                with open(redirect_file,"w") as f:
                    f.write(output+"\n")
            else:
                print(output)

        elif parts[0] =="type":
            if parts[1] in BUILT_IN:
                output="f {parts[1]} is a shell builtin"
                if redirect_file:
                    with open(redirect_file,"w") as f:
                        f.write(output+"\n")
                else:
                    print(output)
            elif path := shutil.which(command[5:]):
                output="f {parts[1]} is {path}"
                if redirect_file:
                    with open(redirect_file,"w") as f:
                        f.write(output)
                else:
                    print(output)
            else:
                print(f"{parts[1]}: not found")
        elif command == "pwd":
            print(os.getcwd())
        elif parts[0]=="cd":
            dir=parts[1]
            if dir=="~":
                dir=os.getenv('HOME')
            try:
                os.chdir(dir)
            except FileNotFoundError:
                print(f"cd: {dir}: No such file or directory")
        elif path := shutil.which(parts[0]):
            exec_path=path
            if redirect_file:
                with open(redirect_file,"w") as f:
                    subprocess.run(parts, executable=exec_path,stdout=f)
            else:
                subprocess.run(parts, executable=exec_path)
        elif not parts:
            continue
        else:
            print(f"{command}: command not found")

        pass


if __name__ == "__main__":
    main()
