# Simulator and data processing tool for correcting errors arisen during quantum key distribution

# WEB API (under development)

## how to run:
install all required packages (python and sveltekit), ToDO which exactly?

run backend: `fastapi dev src/backend/api/main.py `

run frontend: go to src/frontend `npm run dev`

follow link from frontend and enjoy!

# CLI version:

## Prerequisites
 - Python 3.10+ installed and added to PATH
 - Installed required packages, using pip:
~~~~
pip install -r requirements.txt
~~~~

## Simulation tool
A tool allowing simulation of tree parity machine synchronization for post quantum key distribution error correction.

Base mode allows for simulation error correction for machines of different sizes
(size is connected with number of bits to correct) as well as other TPM parameters.

Tool allows user to choose desired quantum bit error rates to be tested.

There are two QBER modes that are simulated:
- random - where errors appear at random places in the key
- bursty - where errors appear in batches one after another in the key

The tool also allows for simulation with an attacker. User has to choose how many TPM does attacker have.
Simulation runs as normal between Alice and Bob (legitimate parties that are trying to correct errors).
At the same time number of Eve (attacker) machines try to synchronize with Alice and Bobs machine but having random values instead ones with given QBER.
Simulation stops after any of Eves machines are synchronized with Alice and Bob.


Run script main.py inside src/backend/cli_simulation_runner directory from this project with chosen arguments
setup PYTHON_PATH to this directory.
~~~~
usage: main.py [-h] [-l WEIGHTS_RANGE [WEIGHTS_RANGE ...]]
               [-n NUMBER_OF_INPUTS_PER_NEURON [NUMBER_OF_INPUTS_PER_NEURON ...]]
               [-k NUMBER_OF_NEURONS_IN_HIDDEN_LAYER [NUMBER_OF_NEURONS_IN_HIDDEN_LAYER ...]]
               [-b QBER [QBER ...]] [-e EVE] [-f FILENAME]

Simulate TPM to correct errors.

optional arguments:
  -h,
   --help            
                        show this help message and exit
                        
  -l WEIGHTS_RANGE [WEIGHTS_RANGE ...],
   --weights_range WEIGHTS_RANGE [WEIGHTS_RANGE ...]
                        list of Ls (range of weights {-L,L}) to generate data, separated by SPACE
                        
  -n NUMBER_OF_INPUTS_PER_NEURON [NUMBER_OF_INPUTS_PER_NEURON ...],
   --number_of_inputs_per_neuron NUMBER_OF_INPUTS_PER_NEURON [NUMBER_OF_INPUTS_PER_NEURON ...]
                        Ns (numbers of inputs to a single neuron) to generate data, [from to by] separated by SPACE
                        
  -k NUMBER_OF_NEURONS_IN_HIDDEN_LAYER [NUMBER_OF_NEURONS_IN_HIDDEN_LAYER ...],
   --number_of_neurons_in_hidden_layer NUMBER_OF_NEURONS_IN_HIDDEN_LAYER [NUMBER_OF_NEURONS_IN_HIDDEN_LAYER ...]
                        Ks (numbers of neurons in hidden layer) to generate data, [from to by] separated by SPACE
  -b QBER [QBER ...],
   --QBER QBER [QBER ...]
                        set list of QBERs to generate data about, separated by SPACE
                        
  -e EVE,
   --eve EVE     
                        number of Eve's machines
                        
  -f FILENAME,
   --filename FILENAME
                        name of file to save data to [test iterations.csv]
~~~~
Example usage:

go to `src` directory and run:
~~~~
python simulator.main --weights_range 1 2 3 4 5 --QBER 10 11
 --number_of_inputs_per_neuron 10 140 10 --number_of_neurons_in_hidden_layer 10 140 10
  --filename raw_data.csv
~~~~

As a result in the chosen by user file a csv is generated.

- In the classic mode (without an attacker) a cvs has the following headers:
  - L;N;K;QBER; - TPM parameters for given run
  - ERRORS - number of different weights between TPMS
  - QBER_TYPE - bursty or random
  - REP - 0-5 one of the repetitions for the same set of parameters (different input weights)
  - TAU_MISSES - number of time that input weights had to be regenerated to get the same result value before updating weights
  - TIME - time that took to synchronize machines
  - repetitions - number of loop repetitions required to synchronize TPMs
- in the mode with the attacker to the classic headers two are added:
   - EVE_SUCCESS - how many Eve's TPMs successfully synchronized (usually 1)
   - EVE_REQUIRED - how many loop repetitions it took to synchronize at least one of Eve's TPMs

## Data processing

### inside src/_wip_data_processor
Module for processing result csv, currently ongoing refactor

## Generating plots

### inside src/_wip_data_processor
Module for automatic plot generation after result csv is processed, currently ongoing refactor
