from subprocess import Popen, PIPE
if __name__ == "__main__":
    p1 = Popen("python D:\\AGH\\inż\\neural_crypto\\neural_crypto\\kivy_server.py",stderr=PIPE, stdout=PIPE, shell=True)
    p2 = Popen("python D:\\AGH\\inż\\neural_crypto\\neural_crypto\\kivy_bob.py",stderr=PIPE, stdout=PIPE, shell=True)
    p1.communicate()
    p2.communicate()
    # print()