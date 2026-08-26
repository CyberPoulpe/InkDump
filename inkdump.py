#!/usr/bin/env python3
import re
import sys

def parse_bash_history_from_mem(pid):
    # Regex stricte : commandes typiques d'un sysadmin (sans retours à la ligne ni scripts bash intégrés)
    bash_cmd_pattern = re.compile(r'^(?:sudo\s+|apt\s+|git\s+|cd\s+|systemctl\s+|nano\s+|cat\s+|docker\s+|grafana-cli\s+|cfdisk\s+|pvs\s+|fdisk\s+|ls\s+|ps\s+|kill\s+)[^\r\n]{2,100}$')

    found_commands = []
    seen = set()

    try:
        with open(f"/proc/{pid}/maps", "r") as maps_file:
            heap_lines = [line for line in maps_file if "[heap]" in line or "rw-p" in line]

        with open(f"/proc/{pid}/mem", "rb") as mem_file:
            for line in heap_lines:
                parts = line.split()
                start, end = int(parts[0].split("-")[0], 16), int(parts[0].split("-")[1], 16)

                # Ignorer les plages mémoires trop grandes pour éviter le ralentissement
                if (end - start) > 15 * 1024 * 1024:
                    continue

                try:
                    mem_file.seek(start)
                    chunk = mem_file.read(end - start)

                    # Découpage par octet nul (séparateur standard dans Readline/Bash)
                    tokens = chunk.split(b'\x00')
                    for token in tokens:
                        try:
                            decoded = token.decode('utf-8').strip()
                            if bash_cmd_pattern.match(decoded):
                                if decoded not in seen:
                                    seen.add(decoded)
                                    found_commands.append(decoded)
                        except UnicodeDecodeError:
                            continue
                except OSError:
                    continue

    except PermissionError:
        print(f"Erreur : Droits insuffisants pour lire /proc/{pid}/mem")
        sys.exit(1)

    return found_commands

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <PID>")
        sys.exit(1)

    for cmd in parse_bash_history_from_mem(sys.argv[1]):
        print(cmd)
