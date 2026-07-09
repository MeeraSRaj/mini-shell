import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        if command.startswith("echo "):
            print(command[5:])
        if command.startswith("type "):
            if command[5:] == "echo":
                print("echo is a shell builtin")
            if command[5:]=="exit":
                print("exit is a shell builtin")
            if command[5:]=="type":
                print("type is a shell builtin")
        else:
            print(f"{command}: command not found")

        pass


if __name__ == "__main__":
    main()
