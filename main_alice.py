import alice_server
import time


alice = alice_server.AliceServer()



print("alice bind")
alice.bind()
time.sleep(1)
print("bob bind")
alice.generate_bits()
time.sleep(1)
print("alice create machine")
alice.create_machine()
time.sleep(1)
print("alice send machine")
alice.send_machine_config()
time.sleep(1)
print("bob receive machine")
time.sleep(1)
print("bob create machine")
time.sleep(1)
print("alice run")
alice.run_machine()
print("bob run")
