import subprocess
import sys
import os


if __name__ == "__main__":

    os.chdir("maxe/build/TheSimulator/TheSimulator/")
    cwd = os.getcwd()
    # List all files and directories in the CWD
    contents = os.listdir(cwd)

    # Print the contents
    for item in contents:
        print(item) 
    simulator = "/TheSimulator"
    
    simulation = sys.argv[1]

    subprocess.run([cwd + simulator, simulation])

