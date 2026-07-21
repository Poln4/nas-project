#!/usr/bin/env python3
"""Interactive generator for NAS (Names Acknowledgment System) notation, v.2."""

TYPES = {
    "n": "given name",
    "s": "surname",
    "p": "patronymic",
    "m": "matronymic",
    "t": "title / honorific",
}

STATES = {"1": "preferred", "2": "present", "3": "implied"}


def ask(prompt):
    return input(prompt).strip()


def ask_choice(prompt, valid):
    while True:
        answer = ask(prompt).lower()
        if answer in valid:
            return answer
        print(f"Please enter one of: {', '.join(valid)}")


def get_name_parts():
    print("Enter your name, with each distinct unit (a given name, a surname, a")
    print("patronymic, ...) separated by a space. This works with any script; for")
    print("names written without spaces (e.g. many Chinese names), add your own")
    print("spaces to mark where one unit ends and the next begins, e.g. '范 寶琳'.")
    parts = ask("Full name: ").split()
    if not parts:
        raise ValueError("No name entered.")
    return parts


def classify_parts(parts):
    print("\nFor each unit, choose its role:")
    for letter, meaning in TYPES.items():
        print(f"  {letter} = {meaning}")
    units = []
    for part in parts:
        part_type = ask_choice(f"  '{part}' -> ", TYPES)
        units.append({"text": part, "type": part_type})
    return units


def mark_hyphenation(units):
    print("\nSome units are really multiple parts treated as one, e.g. 'Eun-jung'.")
    print("Mark a unit's number with '-' for a short combined unit, or '--' for a")
    print("longer multi-part one. Example: '2-,4--'. Leave blank if none apply.")
    for i, unit in enumerate(units, start=1):
        print(f"  {i}. {unit['text']} ({TYPES[unit['type']]})")
    raw = ask("Hyphen marks: ")
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if token.endswith("--"):
            idx_str, marker = token[:-2], "--"
        elif token.endswith("-"):
            idx_str, marker = token[:-1], "-"
        else:
            print(f"Skipping '{token}': must end in '-' or '--'.")
            continue
        try:
            idx = int(idx_str) - 1
            if not (0 <= idx < len(units)):
                raise IndexError
        except ValueError:
            print(f"Skipping '{token}': not a valid unit number.")
            continue
        except IndexError:
            print(f"Skipping '{token}': no unit #{idx_str}.")
            continue
        units[idx]["hyphen"] = marker
    return units


def set_states(units, label):
    print(f"\nNow set each unit's rendering state for the '{label}' NAS:")
    print("  1 = preferred (written, this is how you want to be addressed)")
    print("  2 = present   (written, but not required for address)")
    print("  3 = implied   (acknowledged to exist, but NOT written)")
    rendering = []
    for unit in units:
        # Titles have no "preferred" spelling of their own, so they only toggle
        # between present and implied (matches every title example in the docs).
        allowed = {"2", "3"} if unit["type"] == "t" else set(STATES)
        choice = ask_choice(
            f"  '{unit['text']}' ({TYPES[unit['type']]}) -> [{'/'.join(sorted(allowed))}]: ",
            allowed,
        )
        state = STATES[choice]
        abbreviate = False
        if state == "present":
            answer = ask_choice(
                f"    Write '{unit['text']}' in full, or as an initial? [f/i]: ", {"f", "i"}
            )
            abbreviate = answer == "i"
        rendering.append({**unit, "state": state, "abbreviate": abbreviate})
    return rendering


def build_notation(rendering):
    tokens = []
    for unit in rendering:
        letter = unit["type"].upper() if unit["state"] == "preferred" else unit["type"]
        letter += unit.get("hyphen", "")
        tokens.append((letter, unit["state"] == "implied"))

    # A unit's letter is followed by "." unless it's the very last unit in the
    # whole notation. An implied unit always keeps its dot inside the
    # parentheses regardless of position, since the parentheses are what mark
    # its boundary, not the dot: (N.(n.)S.s) vs (N.(n.)S.(s.)).
    pieces = []
    for i, (letter, implied) in enumerate(tokens):
        is_last = i == len(tokens) - 1
        if implied:
            pieces.append(f"({letter}.)")
        else:
            pieces.append(letter if is_last else f"{letter}.")
    return "(" + "".join(pieces) + ")"


def build_display_name(rendering):
    words = []
    for unit in rendering:
        if unit["state"] == "implied":
            continue
        text = unit["text"]
        if unit["state"] == "present" and unit["abbreviate"]:
            text = text[0] + "."
        words.append(text)
    return " ".join(words)


def run():
    print("Welcome to the NAS Notation Generator (v.2)!")
    print("This builds one or more NAS renderings for your name - e.g. a formal")
    print("one for publications and a casual one for everyday email.\n")

    try:
        parts = get_name_parts()
    except ValueError as exc:
        print(exc)
        return

    units = classify_parts(parts)
    units = mark_hyphenation(units)

    renderings = {}
    while True:
        label = ask("\nLabel for this rendering (e.g. 'legal', 'casual'): ")
        label = label or f"rendering {len(renderings) + 1}"
        rendering = set_states(units, label)
        renderings[label] = rendering

        print(f"\n{label}: {build_display_name(rendering)} {build_notation(rendering)}")

        again = ask_choice("\nAdd another rendering for a different context? [y/n]: ", {"y", "n"})
        if again == "n":
            break

    print("\n--- Your NAS renderings ---")
    for label, rendering in renderings.items():
        print(f"{label}: {build_display_name(rendering)} {build_notation(rendering)}")

    save = ask_choice("\nSave these to a text file? [y/n]: ", {"y", "n"})
    if save == "y":
        filename = ask("Filename (default: my_nas.txt): ") or "my_nas.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for label, rendering in renderings.items():
                f.write(f"{label}: {build_display_name(rendering)} {build_notation(rendering)}\n")
        print(f"Saved to {filename}")


if __name__ == "__main__":
    run()
