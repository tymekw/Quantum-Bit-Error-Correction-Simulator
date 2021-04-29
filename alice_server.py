# ALICE                               BOB
# NKL                         >       NKL
# a=create_TPM                >       b=create_TPM
# W = sha(a)
# W_b = Null
# while W != W_b:
#     UPDATE_W=True           >       UPDATE_W
#                                     While UPDATE_W:
#     X = nrand()             >           X
#     a_tau
#     B_tau                   <           b_tau
#                                         UPDATE_X = true
#     while a_tau!=b_tau                  while UPDATE_X:
#         X                   >               X
#         a_tau
#         b_tau               <               b_tau
#     UPDATE_X = False        >           UPDATE_X = false
#     a_update_W                          w=b_update_w
#     W_b                     <           sha(w)



import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
