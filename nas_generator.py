def generate_nas():
    print("Welcome to the Simple NAS Notation Generator!")
    print("Please enter the parts of your full name, separated by spaces.")
    full_name_str = input("Full Name: ").strip()
    name_parts = full_name_str.split()

    if not name_parts:
        print("Please enter your name.")
        return

    nas_notation = []
    preferences = {}

    print("\nNow, let's identify each part as a name (n) or surname (s).")
    print("Enter 'n' for a given name and 's' for a surname.")

    part_types = []
    for part in name_parts:
        while True:
            part_type = input(f"Is '{part}' a name (n) or surname (s)? ").lower()
            if part_type in ['n', 's']:
                part_types.append(part_type)
                break
            else:
                print("Invalid input. Please enter 'n' or 's'.")

    print("\nDo you have any preferred name(s) or surname(s) you'd like to emphasize?")
    preference_input = input("Enter the preferred name(s) exactly as you typed them earlier, separated by spaces (or leave blank if none): ").strip()
    preferred_parts = preference_input.split()

    preferred_surnames_input = input("Enter the preferred surname(s) exactly as you typed them earlier, separated by spaces (or leave blank if none): ").strip()
    preferred_surnames = preferred_surnames_input.split()

    for i, part_type in enumerate(part_types):
        part = name_parts[i]
        if part in preferred_parts and part_type == 'n':
            nas_notation.append('N')
        elif part in preferred_surnames and part_type == 's':
            nas_notation.append('S')
        else:
            nas_notation.append(part_type)

    print("\nGenerated NAS Notation:")
    print("(" + ".".join(nas_notation) + ")")
    print("\nRemember to manually add hyphens '-' for multi-part first or last names if applicable.")

if __name__ == "__main__":
    generate_nas()