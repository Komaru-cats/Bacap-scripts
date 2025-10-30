import json
from pathlib import Path

from .Advancement import AdvancementsManager, Advancement
from .Datapack import DatapackList
from .InterfaceSchema import get_value
from .Resources import ItemProperties
from .utils import cut_namespace


def generate_type(adv: Advancement):
    if adv.hidden:
        return "Hidden"
    if adv.color.value == "gold":
        return "Advancement Legend"
    return adv.type.replace("_", " ").title()


def generate_requirements():
    req_path = Path('pages/assets/requirements.json')
    if not req_path.exists():
        req_path.write_text(json.dumps({}), encoding=DatapackList.default.encoding)
    data = json.loads(req_path.read_text(encoding=DatapackList.default.encoding))
    for adv in AdvancementsManager.filtered_iterator(datapack=DatapackList.default):
        if adv.mc_path not in data:
            data[adv.mc_path] = ""
    req_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding=DatapackList.default.encoding)


def create():
    generate_requirements()
    data = []
    req_data = json.loads(Path('pages/assets/requirements.json').read_text(encoding=DatapackList.default.encoding))
    for adv in AdvancementsManager.filtered_iterator(datapack=DatapackList.default):
        if adv.functions.reward.item:
            reward_msg = f"{adv.functions.reward.item.amount} {ItemProperties.dict[cut_namespace(adv.functions.reward.item.id)]["display_name"]}"
        else:
            reward_msg = ""
        data.append({
            "title": adv.title,
            "description": adv.description,
            "color": adv.color.as_hex,
            "tab": adv.tab_display,
            "type": generate_type(adv),
            "trophy": adv.functions.trophy.item.name if adv.functions.trophy.item else "",
            "reward": reward_msg,
            "exp": adv.functions.exp.value or 0,
            "req": req_data.get(adv.mc_path, "")
        })
    ver = get_value("Версия релиза (Например 2.2.3):")
    path = Path(f'pages/ver/{ver.replace(".", "_")}/data.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding=DatapackList.default.encoding)
