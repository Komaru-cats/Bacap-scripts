import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

DEFAULT_PATH = "user_config.json"
ENCODING = "utf-8"


class ConfigList(list):
    def __init__(self, parent, keys, *args, **kwargs):
        """
        Initializes a ConfigList object.

        :param parent: Reference to the parent Config object.
        :param keys: Keys to access the current element in the configuration.
        :param args: Additional arguments for initializing the list.
        :param kwargs: Additional named arguments for initializing the list.
        """
        self.parent = parent
        self.keys = keys
        super().__init__(*args, **kwargs)

    def __setitem__(self, index, value):
        """
        Sets the item at the specified index and updates the configuration.

        :param index: Index where the item will be set.
        :param value: Value to set at the specified index.
        """
        super().__setitem__(index, value)
        self.parent.update_config(self.keys, self)

    def append(self, value):
        """
        Appends a value to the list and updates the configuration.

        :param value: Value to append to the list.
        """
        super().append(value)
        self.parent.update_config(self.keys, self)

    def extend(self, values):
        """
        Extends the list by appending elements from the iterable and updates the configuration.

        :param values: Sequence of values to extend the list.
        """
        super().extend(values)
        self.parent.update_config(self.keys, self)

    def insert(self, index, value):
        """
        Inserts a value at the specified index and updates the configuration.

        :param index: Index where the value will be inserted.
        :param value: Value to insert at the specified index.
        """
        super().insert(index, value)
        self.parent.update_config(self.keys, self)

    def remove(self, value):
        """
        Removes the first occurrence of a value from the list and updates the configuration.

        :param value: Value to remove from the list.
        """
        super().remove(value)
        self.parent.update_config(self.keys, self)

    def pop(self, index=-1):
        """
        Removes and returns the item at the specified index and updates the configuration.

        :param index: Index of the item to remove and return. Default is -1.
        :return: The removed item.
        """
        value = super().pop(index)
        self.parent.update_config(self.keys, self)
        return value

    def __getitem__(self, key):
        """
        Gets the item at the specified key. Wraps dict and list items in ConfigDict and ConfigList, respectively.

        :param key: Key of the item to get.
        :return: The item at the specified key.
        """
        item = super().__getitem__(key)
        if isinstance(item, dict):
            return ConfigDict(self.parent, self.keys + [key], item)
        elif isinstance(item, list):
            return ConfigList(self.parent, self.keys + [key], item)
        return item


class ConfigDict(dict):
    def __init__(self, parent, keys, *args, **kwargs):
        """
        Initializes a ConfigDict object.

        :param parent: Reference to the parent Config object.
        :param keys: Keys to access the current element in the configuration.
        :param args: Additional arguments for initializing the dictionary.
        :param kwargs: Additional named arguments for initializing the dictionary.
        """
        self.parent = parent
        self.keys = keys
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """
        Sets the item with the specified key and updates the configuration.

        :param key: Key where the item will be set.
        :param value: Value to set at the specified key.
        """
        super().__setitem__(key, value)
        self.parent.update_config(self.keys, self)

    def __getitem__(self, key):
        """
        Gets the item at the specified key. Wraps dict and list items in ConfigDict and ConfigList, respectively.

        :param key: Key of the item to get.
        :return: The item at the specified key.
        """
        item = super().__getitem__(key)
        if isinstance(item, dict):
            return ConfigDict(self.parent, self.keys + [key], item)
        elif isinstance(item, list):
            return ConfigList(self.parent, self.keys + [key], item)
        return item

    def __delitem__(self, key):
        """
        Deletes the item with the specified key and updates the configuration.

        :param key: Key of the item to delete.
        """
        super().__delitem__(key)
        self.parent.update_config(self.keys, self)


class Config:
    def __init__(self, path: Path | str = DEFAULT_PATH, encoding: str = ENCODING,
                 can_object_change_config: bool = True):
        """
        Initializes a Config object by loading a JSON configuration file.

        :param path: Path to the JSON configuration file. Default is user_config.json.
        :param encoding: Encoding used to read the file. Default is utf-8.
        :param can_object_change_config: If it's True, dict and list update the config when they change. Default is True
        """
        self.path = path
        self.encoding = encoding
        self.can_object_change_config = can_object_change_config
        with open(self.path, encoding=self.encoding) as f:
            self.config = json.load(f)

    def get_dict_by_path(self, keys: Sequence) -> Any:
        """
        Retrieves an object from the configuration based on a list of keys.

        :param keys: List or tuple of keys to traverse the nested dictionary.
        :return: The nested dictionary at the specified path.
        :raises KeyError: If the path does not exist or is invalid.
        """
        json_obj = self.config
        if not keys:
            return json_obj
        for key in keys:
            if isinstance(json_obj, dict):
                json_obj = json_obj.get(key, None)
                if json_obj is None:
                    raise KeyError(f"Key {keys} does not exist in {self.path}: {key}")
            else:
                raise KeyError(f"Key {keys} contains a path to non-dict objects in {self.path}: {key}")
        return json_obj

    def update_config(self, keys: Sequence, value) -> None:
        """
        Updates the configuration with a new value at the specified path of keys.

        :param keys: List of keys to traverse the configuration.
        :param value: New value to set at the specified path.
        """
        json_obj = self.config
        for key in keys[:-1]:
            json_obj = json_obj.setdefault(key, {})
        json_obj[keys[-1]] = value
        self.__write_file_json()

    def __write_file_json(self) -> None:
        """
        Writes the current configuration back to the JSON file.
        """
        with open(self.path, "w", encoding=self.encoding) as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str) -> Any | ConfigList | ConfigDict:
        """
        Retrieves a value from the configuration based on a slash-separated key path.

        :param key: Slash-separated key path.
        :return: The value at the specified key path.
        :raises KeyError: If the path does not exist or is invalid.
        """
        keys = key.split("/")
        value = self.get_dict_by_path(keys)
        if isinstance(value, dict) and self.can_object_change_config:
            return ConfigDict(self, keys, value)
        elif isinstance(value, list) and self.can_object_change_config:
            return ConfigList(self, keys, value)
        return value

    def set(self, key: str, value) -> None:
        """
        Sets a value in the configuration based on a slash-separated key path.

        :param key: Slash-separated key path.
        :param value: Value to set at the specified key path.
        """
        keys = key.split("/")
        self.update_config(keys, value)

    def delete(self, key) -> None:
        """
        Deletes a value from the configuration based on a slash-separated key path.

        :param key: Slash-separated key path.
        :raises KeyError: If the path does not exist or is invalid.
        """
        keys = key.split("/")
        json_obj = self.config
        for key in keys[:-1]:
            json_obj = json_obj.setdefault(key, {})
        del json_obj[keys[-1]]
        self.__write_file_json()

    def __setitem__(self, key, value) -> None:
        """
        Sets a value in the configuration using dictionary-style assignment.

        :param key: Slash-separated key path.
        :param value: Value to set at the specified key path.
        """
        self.set(key, value)

    def __getitem__(self, item) -> Any | ConfigList | ConfigDict:
        """
        Retrieves a value from the configuration using dictionary-style access.

        :param item: Slash-separated key path.
        :return: The value at the specified key path.
        """
        return self.get(item)

    def __delitem__(self, key) -> None:
        """
        Deletes a value from the configuration using dictionary-style deletion.

        :param key: Slash-separated key path.
        """
        self.delete(key)

    def __str__(self) -> str:
        """
        Returns the string representation of the current configuration.

        :return: String representation of the configuration.
        """
        return str(self.config)


def get_config(key: str = None, path: str | Path = DEFAULT_PATH, encoding: str = ENCODING) -> Any:
    """
    Retrieves a value from the configuration file.

    :param key: Slash-separated key path. If None, returns the entire configuration.
    :param path: Path to the JSON configuration file. Default is user_config.json.
    :param encoding: Encoding used to read the file. Default is utf-8.
    :return: The value at the specified key path, or the entire configuration if key is None.
    :raises KeyError: If the path does not exist or is invalid.
    """
    with open(path, encoding=encoding) as f:
        json_obj = json.load(f)
    if not key:
        return json_obj
    for i in key.split("/"):
        if isinstance(json_obj, dict):
            json_obj = json_obj.get(i, None)
            if not json_obj:
                raise KeyError(f"Key {key} does not exist in {path}: {i}")
        else:
            raise KeyError(f"Key {key} contains a path to non-dict objects in {path}: {i}")
    return json_obj
