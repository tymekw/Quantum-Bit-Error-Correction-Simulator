
import bob_client
import time

bob = bob_client.BobClient()



print("alice bind")
time.sleep(1)
print("bob bind")
bob.bind()
time.sleep(1)
print("alice create machine")
time.sleep(1)
print("alice send machine")
time.sleep(1)
print("bob receive machine")
bob.receive_machine_config()
time.sleep(1)
print("Create bits")
bob.create_random_bits()
time.sleep(1)
print("bob create machine")
bob.create_machine()
print("alice run")
time.sleep(1)
print("bob run")
bob.run_TPM_machine()