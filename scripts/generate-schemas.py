#!/usr/bin/env python3
"""
split_schema.py
---------------
Splits a RenderCV JSON Schema file into four sub-schemas:
  cv, design, language (locale_catalog), settings (rendercv_settings).

Each output schema carries only the $defs entries it actually needs,
resolved recursively so no dangling $ref remains.
"""

import json
from pathlib import Path
from rendercv.schema.json_schema_generator import generate_json_schema_file


BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def collect_refs(node: object, all_defs: dict, seen: set[str]) -> None:
    """
    Walk *node* recursively and add every referenced $defs name to *seen*.
    When a new name is found, recurse into its definition so transitive
    dependencies are captured too.
    """
    if isinstance(node, dict):
        ref = node.get("$ref", "")
        if ref.startswith("#/$defs/"):
            name = ref.removeprefix("#/$defs/")
            if name not in seen:
                seen.add(name)
                if name in all_defs:
                    collect_refs(all_defs[name], all_defs, seen)
        for value in node.values():
            collect_refs(value, all_defs, seen)
    elif isinstance(node, list):
        for item in node:
            collect_refs(item, all_defs, seen)


def build_sub_schema(root_schema: dict, property_key: str) -> dict:
    """
    Build a self-contained JSON Schema for *property_key*.

    The result wraps the property inside a root object so that a YAML file
    written as:

        cv:
          name: ...

    validates correctly — the schema root expects an object with a single
    allowed key (cv / design / locale / settings).
    """
    all_defs: dict = root_schema.get("$defs", {})
    properties: dict = root_schema.get("properties", {})

    if property_key not in properties:
        raise KeyError(
            f"Property '{property_key}' not found in schema. "
            f"Available: {list(properties)}"
        )

    prop_schema: dict = properties[property_key]

    # Collect all $defs this property (and its transitive deps) needs
    needed: set[str] = set()
    collect_refs(prop_schema, all_defs, needed)

    # Wrap the property inside a root object so the YAML key is valid
    # at the document root.  additionalProperties: false prevents the
    # validator from accepting sibling keys that belong to other schemas.
    required: list[str] = root_schema.get("required", [])

    sub: dict = {
        "type": "object",
        "properties": {property_key: prop_schema},
        "additionalProperties": False,
    }

    if property_key in required:
        sub["required"] = [property_key]

    if "$schema" in root_schema:
        sub["$schema"] = root_schema["$schema"]

    if needed:
        sub["$defs"] = {
            name: all_defs[name] for name in sorted(needed) if name in all_defs
        }

    return sub


def fix_schema(schema: dict, rendercv_schema_path: Path) -> None:
    defs: dict = schema["$defs"]

    font_family: dict = defs[
        "rendercv__schema__models__design__font_family__FontFamily"
    ]
    if "enum" in font_family:
        font_family["examples"] = font_family.pop("enum")

    rendercv_schema_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(schemas_path_str: str) -> None:
    schemas_path: Path = BASE_DIR / schemas_path_str
    rendercv_schema_path: Path = schemas_path / "rendercv.schema.json"

    # Generate schema w/ rendercv lib
    generate_json_schema_file(rendercv_schema_path)

    # Read it and fix it
    root_schema: dict = json.loads(rendercv_schema_path.read_text(encoding="utf-8"))
    fix_schema(root_schema, rendercv_schema_path)

    # Split schema
    for property_key in root_schema["properties"].keys():
        sub_schema = build_sub_schema(root_schema, property_key)

        out_path = schemas_path / f"{property_key}.schema.json"
        out_path.write_text(
            json.dumps(sub_schema, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        def_count = len(sub_schema.get("$defs", {}))
        print(f"  ✓  {out_path}  ({def_count} $defs included)")


if __name__ == "__main__":
    main("rendercv/schemas")
