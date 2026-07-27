import sys
import shutil
import os
import subprocess
import shlex
import readline

BUILT_IN=["exit", "echo", "type", "pwd", "cd"]
COMMANDS=["echo","exit"]

last_text=""
tab_count=0

def longest_common_prefix(matches):
    prefix=matches[0]

    for word in matches[1:]:
        while not word.startswith(prefix):
            prefix=prefix[:-1]
    return prefix

def completer(text,state):
    global last_text,tab_count
    if last_text==text:
        tab_count+=1
    else:
        last_text=text
        tab_count=1
    matches=[cmd for cmd in COMMANDS if cmd.startswith(text)]
    path_dirs=os.environ.get("PATH","").split(os.pathsep)
    for directory in path_dirs:
        if not os.path.isdir(directory):
            continue
        for filename in os.listdir(directory):
            full_path=os.path.join(directory,filename)
            if (filename.startswith(text) and os.access(full_path,os.X_OK)):
                matches.append(filename)
    matches=sorted(set(matches))
    if len(matches)==0: return None
    elif len(matches)==1: 
        if state==0:
            return matches[0][len(text):] + " "
        return None
    elif len(matches)>1:
        prefix = longest_common_prefix(matches)
        if prefix!=text:
            return prefix[len(text):]+" "
        if tab_count==1:
            sys.stdout.write("\x07")
            sys.stdout.flush()
            return None
        elif tab_count==2:
            sys.stdout.write("\n")
            print("  ".join(matches))
            tab_count=0
            sys.stdout.write("$ "+text)
            sys.stdout.flush()
            return None

def main():
    while True:
        redirect_file=None
        append_mode=False
        error_file=None
        errappend_mode=False
        sys.stdout.write("$ ")
        command = input()
        parts=shlex.split(command)
        if not parts:
            continue

        #Redirection
        if ">" in parts or "1>" in parts:
            if ">" in parts:
                idx=parts.index(">")
            elif "1>" in parts:
                idx=parts.index("1>")
            redirect_file=parts[idx+1]
            parts=parts[:idx]
        if ">>" in parts or "1>>" in parts:
            append_mode=True
            if ">>" in parts:
                idx=parts.index(">>")
            elif "1>>" in parts:
                idx=parts.index("1>>")
            redirect_file=parts[idx+1]
            parts=parts[:idx]
        if "2>" in parts:
            idx=parts.index("2>")
            error_file=parts[idx+1]
            parts=parts[:idx]
        if "2>>" in parts:
            errappend_mode=True
            idx=parts.index("2>>")
            error_file=parts[idx+1]
            parts=parts[:idx]

        mode="a" if append_mode else "w"
        err_mode="a" if errappend_mode else "w"

        if parts[0] == "exit":
            break
        elif parts[0]=="echo":
            output=" ".join(parts[1:])
            if redirect_file:
                with open(redirect_file,mode) as f:
                    f.write(output+"\n")
            elif error_file:
                open(error_file, err_mode).close()
                print(output)
            else:
                print(output)

        elif parts[0] =="type":
            if parts[1] in BUILT_IN:
                output=f"{parts[1]} is a shell builtin"
                if redirect_file:
                    with open(redirect_file,mode) as f:
                        f.write(output+"\n")
                else:
                    print(output)
            elif path := shutil.which(parts[1]):
                output=f"{parts[1]} is {path}"
                if redirect_file:
                    with open(redirect_file,mode) as f:
                        f.write(output+"\n")
                else:
                    print(output)
            else:
                output=f"{parts[1]}: not found"
                if error_file:
                    with open(error_file,err_mode) as f:
                        f.write(output)
                else:
                    print(output)

        elif parts[0]== "pwd":
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
                    with open(error_file,err_mode) as f:
                        f.write(output)
                else:
                    print(output)

        elif path := shutil.which(parts[0]):
            exec_path=path
            if redirect_file:
                with open(redirect_file,mode) as f:
                    subprocess.run(parts, executable=exec_path,stdout=f)
            elif error_file:
                with open(error_file,err_mode) as f:
                    subprocess.run(parts,executable=exec_path,stderr=f)
            else:
                subprocess.run(parts, executable=exec_path)

        else:
            print(f"{command}: command not found")

        pass


if __name__ == "__main__":
    readline.set_completer(completer)
    readline.parse_and_bind("TAB: complete")
    main()
