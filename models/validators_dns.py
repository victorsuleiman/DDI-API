# validators for the creation of zones (and records after)

#check a label within a zone name (the substrings between the dots). No hyphens or dots can be in the extremities, 1-63 characters for each label, no empty labels, 
# case-insensitive, no special symbols or spaces,
def _is_label(label: str) -> bool:
    if not (1 <= len(label) <= 63): return False
    if label[0] == "-" or label[-1] == "-": return False
    for ch in label:
        if not (ch.isalnum() or ch == "-"):
            return False
    return True

#checks if name follows Fully Qualified Domain Name standards.
def is_fqdn(name: str) -> bool:
    if not name: return False
    # allow trailing dot, but check without it
    core = name[:-1] if name.endswith(".") else name
    labels = core.split(".")
    if any(not _is_label(l) for l in labels): return False
    # total length incl trailing dot <= 255
    total = len(core) + (1 if name.endswith(".") else 0)
    return 1 <= len(labels) and total <= 255

def canonical_zone_name(name: str) -> str:
    # store lowercase, no trailing dot
    n = name.strip().lower()
    return n[:-1] if n.endswith(".") else n

def canonical_fqdn(name: str) -> str:
    n = name.strip().lower()
    return n if n.endswith(".") else n + "."
