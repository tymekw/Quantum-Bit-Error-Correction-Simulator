import os
from subprocess import Popen

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    p1 = Popen("python {}\\kivy_server.py".format(dir_path))
    p2 = Popen("python {}\\kivy_bob.py".format(dir_path))
    print(p1.communicate())
    print(p2.communicate())
