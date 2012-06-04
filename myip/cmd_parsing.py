def split_output_into_blocks(out):
    cur_entry = ""
    first_line = True
    for line in out.split("\n"):
        if first_line:
            first_line = False
            cur_entry += line + "\n"
            continue

        if not line.startswith(" ") and not line.startswith("\t"):
            yield cur_entry
            cur_entry = line + "\n"
        else:
            cur_entry += line + "\n"

    yield cur_entry # last but not least
 


