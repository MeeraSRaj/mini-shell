import sys
import shutil
import os
import subprocess
import shlex

BUILT_IN=["exit", "echo", "type", "pwd", "cd"]

def main():
    while True:
        redirect_file=None
        error_file=None
        sys.stdout.write("$ ")
        command = input()
        parts=shlex.split(command)
        if not parts:
            continue

        #Redirection
        elif ">" in parts or "1>" in parts:
            if ">" in parts:
                idx=parts.index(">")
            elif "1>" in parts:
                idx=parts.index("1>")
            redirect_file=parts[idx+1]
            parts=parts[:idx]
        if "2>" in parts:
            idx=parts.index("2>")
            error_file=parts[idx+1]
            parts=parts[:idx]


        if parts[0] == "exit":
            break
        elif parts[0]=="echo":
            output=" ".join(parts[1:])
            if redirect_file:
                with open(redirect_file,"w") as f:
                    f.write(output+"\n")
            elif error_file:
                with open(error_file,"w") as f:
                    f.write(output+"\n")
            else:
                print(output)

        elif parts[0] =="type":
            if parts[1] in BUILT_IN:
                output=f"{parts[1]} is a shell builtin"
                if redirect_file:
                    with open(redirect_file,"w") as f:
                        f.write(output+"\n")
                else:
                    print(output)
            elif path := shutil.which(command[5:]):
                output=f"{parts[1]} is {path}"
                if redirect_file:
                    with open(redirect_file,"w") as f:
                        f.write(output)
                else:
                    print(output)
            else:
                output=f"{parts[1]}: not found"
                if error_file:
                    with open(error_file,"w") as f:
                        f.write(output)
                else:
                    print(output)

        elif command == "pwd":
            print(os.getcwd())

        elif parts[0]=="cd":
            dir=parts[1]
            if dir=="~":
                dir=os.getenv('HOME')
            try:
                os.chdir(dir)
            except FileNotFoundError:
                output=f"cd: {dir}: No such file or directory"
                if error_file:
                    with open(error_file,"w") as f:
                        f.write(output)
                else:
                    print(output)

        elif path := shutil.which(parts[0]):
            exec_path=path
            if redirect_file:
                with open(redirect_file,"w") as f:
                    subprocess.run(parts, executable=exec_path,stdout=f)
            elif error_file:
                with open(error_file,"w") as f:
                    subprocess.run(parts,executable=exec_path,stderr=f)
            else:
                subprocess.run(parts, executable=exec_path)

        else:
            print(f"{command}: command not found")

        pass


if __name__ == "__main__":
    main()
