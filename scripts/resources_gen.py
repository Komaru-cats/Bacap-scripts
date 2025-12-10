import json
import os

ASSETS_FOLDER = "minecraft-data/data/pc/1.21.10"

GENERATED_FOLDER = ASSETS_FOLDER + "_GEN"

items = {}
blocks = {}

_blocks = json.load(open(ASSETS_FOLDER + "/blocks.json"))
_items = json.load(open(ASSETS_FOLDER + "/items.json"))
_attributes = json.load(open(ASSETS_FOLDER + "/attributes.json"))

for block in _blocks:
    items[block["name"]] = {"display_name": block["displayName"], "stack_size": block["stackSize"], "type": "block"}
    blocks[block["name"]] = {"display_name": block["displayName"], "stack_size": block["stackSize"]}

for item in _items:
    name = item["name"]
    if name in items:
        continue
    items[name] = {"display_name": item["displayName"], "stack_size": item["stackSize"], "type": "item"}

if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)

json.dump(items, open(GENERATED_FOLDER + "/items.json", "w"), indent=2)
json.dump(blocks, open(GENERATED_FOLDER + "/blocks.json", "w"), indent=2)

attrs = []
for attr in _attributes:
    attrs.append(attr["resource"])

print("\nATTRS")
print(attrs)
