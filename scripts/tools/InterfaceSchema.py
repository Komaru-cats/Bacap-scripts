from functools import partial

from .Advancement import Advancement, InvalidAdvancement, TechnicalAdvancement
from .Interface import Interface, Icon
from .utils import cut_namespace

format_type_data = {
    str: {"color": "white", "bold": False, "italic": False},
    int: {"color": "purple", "bold": False, "italic": False},
    dict: {"color": "white", "bold": False, "italic": False},
    Advancement: {"color": "green", "bold": False, "italic": False},
    InvalidAdvancement: {"color": "red", "bold": True, "italic": False},
    TechnicalAdvancement: {"color": "cyan", "bold": False, "italic": False}}

interface = Interface(format_type_data=format_type_data)
print_warning = Interface(output_icon=Icon.warning, format_type_data=format_type_data).output

output = interface.output
get_value = interface.get_value
get_value_from_variants = interface.get_value_from_variants
get_bool = interface.get_bool
text = interface.text_wrapper

eget_value = partial(get_value, exit_on_empty=True)
eget_value_from_variants = partial(get_value_from_variants, exit_on_empty=True)
eget_bool = partial(get_bool, exit_on_empty=True)


def print_adv_data(adv: Advancement):
    output(adv)
    output(adv.title, icon=Icon("[n]", color="purple"), indent=3)
    output(adv.description, icon=Icon("[d]", color="purple"), indent=3)
    output(adv.type, icon=Icon("[t]", color="purple"), indent=3)
    output(adv.hidden, icon=Icon("[h]", color="purple"), indent=3)
    output(adv.tab, icon=Icon("[t]", color="purple"), indent=3)
    output(adv.datapack, icon=Icon("[D]", color="purple"), indent=3)
    if (exp := adv.functions.exp).value:
        output(text(exp.value) + " exp", indent=3, icon=Icon("[e]", color="purple"))
    if (reward := adv.functions.reward).item:
        output(text(reward.item.amount) + " " + text(cut_namespace(reward.item.id), color="yellow"), indent=3,
               icon=Icon("[r]", color="purple"))
    if (trophy := adv.functions.trophy).item:
        output(trophy.item.name, indent=3, icon=Icon("[t]", color="purple"), color="blue")
        output(trophy.item.lore, indent=4, icon=Icon("[l]", color="blue"))
        output(trophy.item.color, indent=4, icon=Icon("[c]", color="blue"))
        output(cut_namespace(trophy.item.id), indent=4, icon=Icon("[i]", color="blue"))
