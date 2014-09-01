import os


def run_tests():
    dir = os.getcwd()
    if dir[-5:] != "tests":
        os.chdir("tests")

    names = os.listdir(os.curdir)
    for name in names:
        if name[:5] == "test_" and name[-3:] == ".py":
            print(name)
            os.system("python " + name)


if __name__ == '__main__':
    run_tests()