# Simulator and data processing tool for correcting errors arisen during quantum key distribution


## Prerequisites
 - Python 3.7 installed and added to PATH
 - Installed required packages, using pip:
~~~~
pip install -r requirements.txt
~~~~

## Simulation tool
Run script main.py inside simulator directory from this project with chosen arguments
~~~~
usage: main.py [-h] [-l WEIGHTS_RANGE [WEIGHTS_RANGE ...]]
               [-n NUMBER_OF_INPUTS_PER_NEURON [NUMBER_OF_INPUTS_PER_NEURON ...]]
               [-k NUMBER_OF_NEURONS_IN_HIDDEN_LAYER [NUMBER_OF_NEURONS_IN_HIDDEN_LAYER ...]]
               [-b QBER [QBER ...]] [-e EVE] [-f FILENAME]

Simulate TPM to correct errors.

optional arguments:
  -h, --help            
                        show this help message and exit
  -l WEIGHTS_RANGE [WEIGHTS_RANGE ...], --weights_range WEIGHTS_RANGE [WEIGHTS_RANGE ...]
                        list of Ls (range of weights {-L,L}) to generate data, separated by SPACE
  -n NUMBER_OF_INPUTS_PER_NEURON [NUMBER_OF_INPUTS_PER_NEURON ...], --number_of_inputs_per_neuron NUMBER_OF_INPUTS_PER_NEURON [NUMBER_OF_INPUTS_PER_NEURON ...]
                        Ns (numbers of inputs to a single neuron) to generate data, [from to by] separated by SPACE
  -k NUMBER_OF_NEURONS_IN_HIDDEN_LAYER [NUMBER_OF_NEURONS_IN_HIDDEN_LAYER ...], --number_of_neurons_in_hidden_layer NUMBER_OF_NEURONS_IN_HIDDEN_LAYER [NUMBER_OF_NEURONS_IN_HIDDEN_LAYER ...]
                        Ks (numbers of neurons in hidden layer) to generate data, [from to by] separated by SPACE
  -b QBER [QBER ...], --QBER QBER [QBER ...]
                        set list of QBERs to generate data about, separated by SPACE
  -e EVE, --eve EVE     
                        number of Eve's machines
  -f FILENAME, --filename FILENAME
                        name of file to save data to [test iterations.csv]
~~~~
Example usage:
~~~~
python main.py --weights_range 1 2 3 4 5 --QBER 10 11 --number_of_inputs_per_neuron 10 140 10 --number_of_neurons_in_hidden_layer 10 140 10 --filename raw_data.csv
~~~~

## Data processing

# ToDo


## Generating plots

# TODo
