import sys
import json

from configuration.configuration_loader import ConfigurationLoader
from ramen.Ramen import Ramen

def main(config_filename, save_json_filename, random_walk_only):
    config_loader = ConfigurationLoader(config_filename)
    ramen_bowl = Ramen(config_loader.csv_filename, config_loader.end_var, config_loader.min_values)
    ramen_bowl.random_walk(
        config_loader.num_exp,
        config_loader.num_walks,
        config_loader.num_steps,
        config_loader.p_value,
        config_loader.correction)

    if random_walk_only:
        save_to_json(save_json_filename, ramen_bowl.export_ramen_as_dict())
        return

    ramen_bowl.genetic_algorithm(
        config_loader.num_candidates,
        config_loader.end_thresh,
        config_loader.mutate_num,
        config_loader.best_cand_num,
        config_loader.bad_repod_accept,
        config_loader.reg_factor,
        config_loader.hard_stop)

    save_to_json(save_json_filename, ramen_bowl.export_ramen_as_dict())

def parse_str_to_bool(string):
    if string.lower() in ("true", "1"):
        return True
    elif string.lower() in ("false", "0", "no"):
        return False
    else:
        raise ValueError(f"Valid values are: true, 1, false, 0 - Input value is {string}")

def save_to_json(json_file_name, ramen_result_dict):
    with open(json_file_name, "w") as file:
        json.dump(str(ramen_result_dict), file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <config_filename> <save_json_filename> <random_walk_only>")
        sys.exit(1)

    config_name = sys.argv[1]
    save_name = sys.argv[2]
    rw_only_bool = parse_str_to_bool(sys.argv[3])

    main(config_name, save_name, rw_only_bool)
