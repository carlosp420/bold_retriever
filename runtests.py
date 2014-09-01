import os
import subprocess
import sys


def run_tests():
    dir = os.getcwd()
    if dir[-5:] != "tests":
        tests_path = os.path.join(dir, "tests")

    names = os.listdir(tests_path)
    for name in names:
        if name[:5] == "test_" and name[-3:] == ".py":
            print(name)
            cmd = "python " + os.path.join(tests_path, name)
            try:
                subprocess.check_call(cmd, shell=True)
            except subprocess.CalledProcessError:
                sys.exit(str(subprocess.CalledProcessError))


if __name__ == '__main__':
    run_tests()