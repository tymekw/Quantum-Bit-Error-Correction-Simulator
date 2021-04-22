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
#     W = sha(w)