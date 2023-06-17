from enum import IntEnum, auto as a

INPUT = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Fonts(IntEnum):
    MONOSPACE = a()
    ITALIC = a()
    BOLD = a()
# end class


OUTPUT: dict[Fonts, str] = {
    Fonts.MONOSPACE: "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
    Fonts.ITALIC: "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",
    Fonts.BOLD: "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭",
}


REPLACEMENTS: dict[Fonts, dict[str, str]] = {
    font: {
        INPUT[i]: replacement[i]
        for i in range(max(len(INPUT), len(replacement)))
    }
    for font, replacement in OUTPUT.items()
}

REVERSE_REPLACEMENTS: dict[Fonts, dict[str, str]] = {
    font: {
        replacement[i]: INPUT[i]
        for i in range(max(len(INPUT), len(replacement)))
    }
    for font, replacement in OUTPUT.items()
}


def replace_with(text: str, replacements: dict[str, str]) -> str:
    return "".join([replacements.get(char, char) for char in text])
# end def


def replace(text: str, font: Fonts, reverse: bool = False) -> str:
    replacements = REVERSE_REPLACEMENTS if reverse else REPLACEMENTS
    return replace_with(text=text, replacements=replacements[font])
# end def

