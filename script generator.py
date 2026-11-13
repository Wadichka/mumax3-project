import stat
import subprocess
import sys
from collections.abc import Sequence
from itertools import product
from string import Template
from pathlib import Path


def generate(
            base_script: Template,
            output_path: Path,
            variants: list[dict[Path, dict[str, str]]]
        ) -> list[Path]:
    output_directory = Path(output_path)
    output_directory.mkdir(exist_ok=True, parents=True)
    paths = []
    for item in variants:
        filename, parameters = next(iter(item.items()))
        path = output_directory / filename
        path.write_text(base_script.substitute(parameters), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)  # Makes file executable
        paths.append(path)

    return paths


def run(script_path: Path, flags: Sequence[str] = []) -> None:
    if not script_path.exists():
        raise FileNotFoundError(f"Script file {script_path} does not exist.")

    if script_path.suffix != ".mx3":
        raise ValueError(f"Path {script_path} is not a MuMax3 file.")

    cmd = ["mumax3", *flags, str(script_path)]
    print(f"Running command: {' '.join(cmd)}", flush=True, file=sys.stderr)

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    with open("script.txt", "r") as file:
        base_script = Template(file.read())

    script_dir = Path("./scripts/")

    combinations = list(product([True, False], repeat=4))
    combinations.pop()  # Delete redundant case of (False, False, False, False)

    for frequency in [5.21, 5.22, 5.23, 5.24, 5.25]:
        variants = []
        for combination in combinations:
            down_left_antenna: bool = combination[0]
            down_right_antenna: bool = combination[1]
            up_right_antenna: bool = combination[2]
            up_left_antenna: bool = combination[3]

            filename = f"{"down-left_" if down_left_antenna else ""}" + \
                f"{"down-right_" if down_right_antenna else ""}" + \
                f"{"up-right_" if up_right_antenna else ""}" + \
                f"{"up-left_" if up_left_antenna else ""}" + \
                f"{frequency}GHz.mx3"

            variables = {
                "frequency": f"{frequency}e9",
                "first_antenna_open": "" if down_left_antenna else "/*",
                "first_antenna_close": "" if down_left_antenna else "*/",
                "second_antenna_open": "" if down_right_antenna else "/*",
                "second_antenna_close": "" if down_right_antenna else "*/",
                "third_antenna_open": "" if up_right_antenna else "/*",
                "third_antenna_close": "" if up_right_antenna else "*/",
                "fourth_antenna_open": "" if up_left_antenna else "/*",
                "fourth_antenna_close": "" if up_left_antenna else "*/"
            }
            print(filename, ": {")
            for key, value in variables.items():
                print(f"    {key}: {value}")
            print("}")
            variants.append({filename: variables})

        frequency_dir = script_dir / f"{frequency}GHz"
        script_paths = generate(base_script, frequency_dir, variants)
        for script_path in script_paths:
            run(script_path)
