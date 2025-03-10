import subprocess

def main():
    subprocess.run(["darktable-cli", "--version"])

if __name__ == "__main__":
    main()