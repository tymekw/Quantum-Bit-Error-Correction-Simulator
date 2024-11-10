from cli_simulation_runner.args_parser import (
    parse_input_arguments,
    translate_args_to_simulator_parameters,
)
from simulator.simulation_runner import run_simulation
from simulator.utils import write_headers


def main():
    args = parse_input_arguments()
    simulator_params = translate_args_to_simulator_parameters(args)
    write_headers(simulator_params.file_path, bool(simulator_params.eve))
    run_simulation(simulator_params)


if __name__ == "__main__":
    main()
