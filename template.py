import os
import sys


class redirect:
    content = ""

    def write(self, str):
        self.content += str

    def flush(self):
        self.content = ""


def parse_template(file_name, context=None):
    # Read template content
    root_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_path, "templates", file_name)

    with open(path, "r") as f:
        html_content = f.read()

    # Catch the print content
    __console__ = sys.stdout
    r = redirect()
    sys.stdout = r

    # Process template
    lines = html_content.split("\n")
    processed_lines = []
    code_block = ""
    in_code_block = False

    for i, line in enumerate(lines):
        if not in_code_block:
            if "{{{" and "}}}" in line:
                code_block = line[line.index("{{{") + 3:line.index("}}}")]
                if "=" in line:
                    exec(code_block.strip(), context)
                    processed_lines.append(lines[i].replace(
                        "{{{" + code_block + "}}}", str(r.content)))
                else:
                    result = eval(code_block.strip(), context)
                    processed_lines.append(lines[i].replace(
                        "{{{" + code_block + "}}}", str(result)))
                code_block = ""
                r.flush()
            elif "{{{" in line:
                strip_index = line.index("{{{") + 4
                in_code_block = True
            else:
                processed_lines.append(lines[i])
        else:
            if "}}}" in line:
                exec(code_block, context)
                processed_lines.append(str(r.content))
                strip_index = 0
                code_block = ""
                in_code_block = False
                r.flush()
            else:
                code_block +=  line[strip_index:].rstrip()
                code_block += "\n"

    sys.stdout = __console__

    return "\n".join(processed_lines)
