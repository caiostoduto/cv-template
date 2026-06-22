#!/usr/bin/env python3
"""
join-properties.py
------------------
Joins all `rendercv/*.yaml` into a single `output/rendercv.yaml` file to be rendered by rendercv cli
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def main(input_path_str: str, output_path_str: str) -> None:
    input_path: Path = BASE_DIR / input_path_str
    output_path: Path = BASE_DIR / output_path_str

    # Read yaml files
    yamls = sorted(Path(input_path).glob("*.yaml"))
    yamls_text = map(lambda yaml: yaml.read_text(), yamls)

    # Concat each yaml file (without the heading line) into a single yaml
    flat_lines = [line for txt in yamls_text for line in txt.splitlines()[1:]]

    # Write the final file
    output_text = (
        f"# yaml-language-server: $schema={(input_path / 'schemas' / 'rendercv.schema.json')}\n"
        + "\n".join(flat_lines)
    )
    output_path.write_text(output_text)


if __name__ == "__main__":
    main(input_path_str="rendercv", output_path_str="output/rendercv.yaml")
