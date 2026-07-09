import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command.startswith("echo "):
            print(command[5:])
            break
        pass


if __name__ == "__main__":
    main()
