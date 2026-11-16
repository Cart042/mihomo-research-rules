#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
pattern = re.compile(r"^  - DOMAIN-SUFFIX,([a-z0-9][a-z0-9.-]*\.[a-z]{2,63})$")

for file in sorted((root / "rules").glob("*.yaml")):
    lines = file.read_text(encoding="utf-8").splitlines()
    assert "payload:" in lines, file
    entries = [line for line in lines if line.startswith("  - ")]
    domains = []
    for line in entries:
        match = pattern.fullmatch(line)
        if not match:
            raise ValueError(f"Malformed entry: {file.name}: {line}")
        domains.append(match.group(1))
    if len(domains) != len(set(domains)):
        raise ValueError(f"Duplicate rules in {file.name}")
    print(f"{file.name}: {len(domains)} rules OK")

print("All domain-rule files passed static checks.")
