def markdown_to_blocks(markdown):
    split_lines = markdown.split("\n\n")
    strip_lines = []
    for line in split_lines:
        new_line = line.strip()
        if new_line == "":
            continue
        strip_lines.append(new_line)
    return strip_lines
