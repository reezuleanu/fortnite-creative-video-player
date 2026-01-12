import sys
import os


def find_textures_module(contents: str) -> str:
    """Paste full .verse contents and it will spit out only the Textures module

    Args:
        contents (str): entire .verse assets file

    Returns:
        str: Textures module only
    """
    content_lines = contents.split("\n")
    for i, line in enumerate(content_lines):
        # find beginning of module
        if line == "Textures := module:":
            start_idx = i

    for i, line in enumerate(content_lines[start_idx]):
        # find beginning of a new module
        if line.endswith("module:"):
            end_idx = i
        # if there are no following modules
        end_idx = len(content_lines) - 1

    return "\n".join(content_lines[start_idx:end_idx])


def generate_texture_mappings(textures_module: str) -> dict:
    """Generate a dictionary of texture_name: texture_object in .verse

    Args:
        textures_module (str): Texture Module text

    Returns:
        dict: texture mappings
    """
    mappings = {}

    for x in [x.lstrip() for x in textures_module.split("\n")]:
        if not x:
            continue
        if x.endswith(r":texture = external {}"):
            texture_name = x.split("<scoped")[0]
            mappings[texture_name] = f"Textures.{texture_name}"

    return mappings


def generate_verse_module(texture_mappings: dict) -> None:
    """Write a .verse module containing the texture mappings

    Args:
        texture_mappings (dict): texture mappings
    """

    mappings = "\n".join([f'\t\t"{k}" => {v}' for k, v in texture_mappings.items()])

    verse_module = f"""
TextureLibrary<public> := module:
    using {{/Verse.org/Assets}}
    # Map of names to textures
    var TextureMap<public>: [string]texture = map{{
{mappings}
    }}

"""

    return verse_module


def main(file_input: str) -> None:
    if not os.path.exists(file_input):
        raise Exception(
            f"Path {file_input} is invalid. Make sure the file exists or provide an absolute path"
        )

    with open(file_input, "r") as fp:
        contents = fp.read()

    if not contents:
        raise Exception(f"File {file_input} is empty!")

    textures_module = find_textures_module(contents)

    texture_mappings = generate_texture_mappings(textures_module)

    verse_module = generate_verse_module(texture_mappings)

    with open("TextureMappings.verse", "w") as fp:
        fp.write(verse_module)

    print("Textures mapped successfully!")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "You must provide an input .verse assets file"

    assert sys.argv[1], "Input file name must not be blank"

    main(sys.argv[1])
