from tpm.simulator_tmp.parser import TPMSimulatorParser

from tpm.simulator_tmp.tpm_simulator import TPMSimulator

if __name__ == '__main__':
    parser = TPMSimulatorParser()
    simulator = TPMSimulator(parser)
    simulator.run_simulation()
