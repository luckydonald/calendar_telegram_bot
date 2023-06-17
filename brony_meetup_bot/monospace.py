MONOSPACE_INPUT = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
MONOSPACE_OUTPUT = "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
MONOSPACE_REPLACEMENTS = {
    MONOSPACE_INPUT[i]: MONOSPACE_OUTPUT[i]
    for i in range(max(len(MONOSPACE_INPUT), len(MONOSPACE_OUTPUT)))
}
MONOSPACE_REVERSE_REPLACEMENTS = {
    MONOSPACE_OUTPUT[i]: MONOSPACE_INPUT[i]
    for i in range(max(len(MONOSPACE_INPUT), len(MONOSPACE_OUTPUT)))
}


def replace_with_monospace(text: str) -> str:
    return "".join([MONOSPACE_REPLACEMENTS.get(char, char) for char in text])
# end def


def replace_with_plain(text: str) -> str:
    return "".join([MONOSPACE_REVERSE_REPLACEMENTS.get(char, char) for char in text])
# end def
