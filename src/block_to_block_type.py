import re
from block_type import BlockType

def block_to_block_type(markdown):
    lines = markdown.split('\n')

    if re.match(r"^#{1,6}\s", markdown):
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered_list = True
    for i, line in enumerate(lines):
        match = re.match(r"^(\d+)\.\s", line)
        if not match or int(match.group(1)) != i + 1:
            is_ordered_list = False
            break
    if is_ordered_list and len(lines) > 0:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
