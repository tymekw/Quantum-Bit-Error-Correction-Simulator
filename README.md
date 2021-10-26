# Application allowing to correct errors arising in quantum key distribution

Application allows user to simulate error correction of bits created in quantum key distribution process using neural network.
User is able to upload bits on its own as well as create random bits with chosen bit error rate to be corrected.
Some tweaks in neural network structure are also possible. Application after synchronization process
checks if new bits are properly corrected and shows it by green or red frame around them

## Prerequisites
 - Python 3.7 installed and added to PATH
 - Installed required packages, using pip:
~~~~
pip install -r requirements.txt
~~~~

## Run locally
2. Run script main.py inside neural_crypto directory
~~~~
python main.py
~~~~

## /test directory
- loop_test.py script generates data about number of required synchronizations
- test_data.ipynb used to display plots and calculate statistics
- remaining scripts are used by loop_test.py
