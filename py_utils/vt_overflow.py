import os
import argparse
import logging
from pathlib import Path
import re

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger()

DIFF = 910

pattern = re.compile(r"^(?P<prefix>.*?)(?P<index>\d+)$")

parser = argparse.ArgumentParser(
    "vt_overflow",
    description="Duplicate frames and modify their suffix as to not be \
    picked up by UEFN's shit virtual textures",
)

parser.add_argument(
    "input_path",
    type=str,
    help="The directory containing the source frames",
    default=".",
)
parser.add_argument(
    "-i",
    "--start-idx",
    type=int,
    help="The index to start from, if None, will start with the frame with the lowest index",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Destination directory. If None, will create a directory wherever this program is ran",
    default="vt_output/",
)

if __name__ == "__main__":
    args = parser.parse_args()

    input_path = Path(args.input_path)

    results = []
    PREFIX = None
    EXTENSION = None
    for file in input_path.glob("*"):
        if not file.is_file():
            continue

        match = pattern.match(file.stem)
        if not match:
            continue

        if not PREFIX:
            PREFIX = match.group("prefix")

        if not EXTENSION:
            EXTENSION = file.suffix

        index = int(match.group("index"))

        results.append((PREFIX, index, EXTENSION))

    if args.start_idx:
        start_idx = args.start_idx
    elif results:
        start_idx = min(idx for _, idx, _ in results)
    else:
        start_idx = None

    if not start_idx:
        logger.exception("Starting index could not be inferred from naming scheme")
        SystemExit(1)

    output_path = Path(args.output)

    os.makedirs(output_path, exist_ok=True)

    for i in range(start_idx, start_idx + DIFF):
        try:
            with open(os.path.join(input_path, f"{PREFIX}{i}{EXTENSION}"), "rb") as fp:
                contents = fp.read()

            with open(
                os.path.join(output_path, f"{PREFIX}10{i}{EXTENSION}"), "wb"
            ) as fp:
                fp.write(contents)
        except FileNotFoundError:
            logger.warning(
                f"Not enough input files provided to be able to overflow a virtual texture,\
 only duplicated up to '{PREFIX}{i-1}{EXTENSION}'"
            )
            break

    logger.info(f"Duplication finished successfully, output: {output_path.absolute()}")
