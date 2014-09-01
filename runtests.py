import os
import subprocess
import sys


def run_tests():
    dir = os.getcwd()
    if dir[-5:] != "tests":
        os.chdir("tests")

    names = os.listdir(os.curdir)
    for name in names:
        if name[:5] == "test_" and name[-3:] == ".py":
            print(name)
            cmd = "python " + name
            try:
                subprocess.check_call(cmd, shell=True)
            except subprocess.CalledProcessError:
                sys.exit(str(subprocess.CalledProcessError))


if __name__ == '__main__':
    run_tests()