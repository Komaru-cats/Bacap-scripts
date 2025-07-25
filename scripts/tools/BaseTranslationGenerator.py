import json
from collections.abc import Iterable
from pathlib import Path

import jsoncomment

from . import Datapack


class BaseTranslationGenerator:
    @classmethod
    def update(cls, datapack: Datapack | Iterable[Datapack]):
        """Main method to create a new base translation file with keys from source JSON."""
        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)
        for dp in datapack:
            # Load the source JSON data (including comments)
            source_json = cls._load_json_from_file(dp.main_translation_path, dp.encoding)

            # Create a new base JSON structure with empty values
            base_json = cls._create_new_base_json(source_json)

            # Convert the base JSON structure to a string with a header
            json_string = cls._add_header_to_base_translation(base_json, dp.base_translation_header)

            # Write the new JSON string to the file, overwriting it completely
            dp.base_translation_path.write_text(data=json_string, encoding=dp.encoding)

    @staticmethod
    def _load_json_from_file(file_path: Path, encoding: str):
        """Loads JSON data from a file, preserving comments using jsoncomment."""
        return jsoncomment.JsonComment().loads(file_path.read_text(encoding=encoding))

    @classmethod
    def _create_new_base_json(cls, source_json: dict[str, str]) -> dict[str, str]:
        """Creates a new JSON structure with keys from source JSON and empty values."""
        return {key: "" for key in source_json.keys()}

    @staticmethod
    def _add_header_to_base_translation(base_json: dict[str, str], header_text: str):
        """
        Converts JSON to string and inserts header text after the opening brace.
        Returns a string ready to be written to the file.
        """

        json_string = json.dumps(base_json, ensure_ascii=False, indent=4)

        brace_index = json_string.find("{") + 1
        json_with_header = f"{json_string[:brace_index]}\n{header_text}\n{json_string[brace_index:]}"

        return json_with_header
