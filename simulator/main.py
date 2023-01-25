# ToDo pseudo code for data gathering
"""
for N_OF_BITS:
    for L:
        for N:
            for K:
                for BER:
                    for REPS_FOR_STATS:
                        change_random_seed()
                        initial_weights_alice, initial_weights_bob = generate_weigths(ber, ber_type)
                        alice = TPM(n,k,l, initial_weights_alice)
                        bob = TPM(n,k,l, initial_weights_bob)
                        while not alice.W == bob.W:
                            X = generate_random_input()
                            alice.set_X(X)
                            bob.set_X(X)
                            a_sigma, a_tau = alice.calculate_TPM_results()
                            b_sigma, b_tau = bob.calculate_TPM_results()
                            while a_tau != b_tau:
                                X = generate_random_input()
                                alice.set_X(X)
                                bob.set_X(X)
                                a_sigma, a_tau = alice.calculate_TPM_results()
                                b_sigma, b_tau = bob.calculate_TPM_results()
                            alice.set_tau(a_tau)
                            alice.set_sigma(a_sigma)
                            bob.set_tau(a_tau)
                            bob.set_sigma(a_sigma)
                            alice.update_weights()
                            bob.update_weights()
"""