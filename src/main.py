import re
from decimal import Decimal

variables = {}
TYPE_MAP = {
    "RRRR RRRR": int,
    "RR RR RR RR": str,
    "RRRR RR RR": Decimal
}

def parse_line(line, if_state):
    line = line.strip()

    if line == "RRRRR RRRRRR":
        return "if_end"

    if line.startswith("RRRRR RRRR RRRR"):
        match = re.findall(r'"(.*?)"', line)
        if len(match) == 2:
            var, val = match
            actual = variables.get(var)
            return actual == val
        else:
            print(f"[ERROR] Invalid IF syntax")
            return False

    if line.startswith("RRR RR ") and '"' in line:
        match = re.search(r'"(.*?)"', line)
        if match:
            print(match.group(1))
        return

    if line.startswith("RRR RR "):
        var = line[len("RRR RR "):].strip()
        if var in variables:
            print(variables[var])
        else:
            print(f"[ERROR] Undefined variable: {var}")
        return

    if line.startswith("RR RRRRR "):
        parts = line.split()
        if len(parts) >= 4:
            var_name = parts[2]
            type_str = ' '.join(parts[3:])
            typ = TYPE_MAP.get(type_str)
            if not typ:
                print(f"[ERROR] Unknown type: {type_str}")
                return
            val = input()
            try:
                variables[var_name] = typ(val)
            except Exception as e:
                print(f"[ERROR] Invalid input for {typ}: {e}")
        return

    if line.startswith("RRRR RRRRRR"):
        match = re.search(r'"(.*?)"', line)
        if match:
            variables[match.group(1)] = None
        return

    if line.startswith("RR RRR RRR RRR"):
        match = re.search(r'"(.*?)"\s+RRRRRRRRRRRR\s+(.*?)\s+RR R R R RRRR', line)
        if match:
            name, type_str = match.groups()
            typ = TYPE_MAP.get(type_str)
            if typ:
                variables[name] = None
            else:
                print(f"[ERROR] Unknown type: {type_str}")
        return

    print(f"[WARN] Unknown command: {line}")


def run_rrrr(filename):
    with open(filename, encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith("RRRRR RRRR RRRR"):
            result = parse_line(line, None)
            i += 1
            if result:
                while i < len(lines):
                    if lines[i].strip() == "RRRRR RRRRRR":
                        break
                    parse_line(lines[i], True)
                    i += 1
            else:
                while i < len(lines) and lines[i].strip() != "RRRRR RRRRRR":
                    i += 1
        else:
            parse_line(line, None)
        i += 1


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python r_lang.py file.RRRR")
    else:
        run_rrrr(sys.argv[1])
