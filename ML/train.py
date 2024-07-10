import os
import json
import argparse
from pathlib import Path

import torch
from neuralhydrology.nh_run import start_run, continue_run


def train():
    # check if CUDA available
    if torch.cuda.is_available():
        pass
    else:
        raise Exception("No GPU found!")

    # load allowed GPU ids
    f = open("gpu.json")
    gpus = json.load(f)
    f.close()

    # add CLI arguments
    parser = argparse.ArgumentParser(
        prog="train.py",
        description="This program trains the specified model.",
        epilog="Note, all the flags are optional, see the options to understand the default values.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--continue_train",
        action="store_true",
        help="specifies to continue train from the last epoch",
        default=False,
    )
    parser.add_argument(
        "--gpu", type=int, help="gpu id", default=gpus[0], required=False
    )
    parser.add_argument(
        "--model",
        type=str,
        help="model to use",
        default="lstm",
        choices=["lstm", "ea_lstm", "transformer"],
        required=False,
    )
    args = parser.parse_args()

    if args.gpu not in gpus:
        raise Exception(
            f"Specified prohibited gpu id: `{args.gpu}`, allowed gpu ids are: `{gpus}`"
        )

    # path to the config file
    cfg_path = Path(f"./conf/{args.model}.yml")
    # check if model config exists
    if not cfg_path.exists():
        raise Exception(
            f"No config file found for specified model `{args.model}`. Consider adding a config for this model or use one of available models, see --help."
        )

    if args.continue_train:
        # continue training from previous epoch
        try:
            run_dir = Path(f"./runs/{sorted(os.listdir('./runs'))[-1]}")
        except:
            print(
                "No `runs` directory found, first train a model from scrath without option `--continue_train`."
            )
        print("Continue training")
        continue_run(run_dir=run_dir, gpu=args.gpu)

    else:
        # training from scratch
        start_run(config_file=cfg_path, gpu=args.gpu)


if __name__ == "__main__":
    train()
