#!/usr/bin/env python3
"""
pre-commit.py
------------------
Adds all relevant results (pngs prewiew and CONSIDERATIONS.md) into README.md
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent


def main(
    readme_path_str: str,
    output_path_str: str,
    considerations_path_str: str,
):
    readme_path: Path = BASE_DIR / readme_path_str
    output_path: Path = BASE_DIR / output_path_str
    considerations_path: Path = BASE_DIR / considerations_path_str

    pdf_path = next(output_path.glob("*.pdf"))

    # Build the images markdown list
    images = [
        f"[![Preview]({img_path.relative_to(BASE_DIR)})]({pdf_path.relative_to(BASE_DIR)})"
        for img_path in sorted(output_path.glob("*.png"))
    ]
    images_block = f"\n{'\n'.join(images)}\n\n"

    # Replace section 'Preview'
    readme_text = re.sub(
        r"(?<=### Preview\n)[\s\S]+?(?=###)",
        lambda _: images_block,
        readme_path.read_text(),
    )

    if considerations_path.exists():
        # Replace section 'Considerations'
        readme_text = re.sub(
            r"(?<=### Considerations\n)[\s\S]+?(?=###|$)",
            lambda _: f"\n{considerations_path.read_text()}\n\n",
            readme_text,
        )

    readme_path.write_text(readme_text)


if __name__ == "__main__":
    main(
        readme_path_str="README.md",
        output_path_str="output",
        considerations_path_str="CONSIDERATIONS.md",
    )
