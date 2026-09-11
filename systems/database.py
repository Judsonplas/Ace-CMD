import json
import os

BASE = "data"

SERVERS = f"{BASE}/servers.json"
WARNINGS = f"{BASE}/warnings.json"


def ensure_files():
    os.makedirs(BASE, exist_ok=True)
    os.makedirs(f"{BASE}/logs", exist_ok=True)

    for file in [SERVERS, WARNINGS]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump({}, f, indent=4)


def load(file):
    ensure_files()

    with open(file, "r") as f:
        return json.load(f)


def save(file, data):
    ensure_files()

    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# --------------------
# Server Config System
# --------------------

def get_server_config(guild_id):
    servers = load(SERVERS)

    gid = str(guild_id)

    if gid not in servers:
        servers[gid] = {
            "admin_role": None,
            "mod_role": None,
            "helper_role": None,
            "logs": True
        }

        save(SERVERS, servers)

    return servers[gid]


def update_server_config(guild_id, key, value):
    servers = load(SERVERS)

    gid = str(guild_id)

    if gid not in servers:
        servers[gid] = {}

    servers[gid][key] = value

    save(SERVERS, servers)


# --------------------
# Warning System
# --------------------

def add_warning(guild_id, user_id, warning):
    warnings = load(WARNINGS)

    gid = str(guild_id)
    uid = str(user_id)

    if gid not in warnings:
        warnings[gid] = {}

    if uid not in warnings[gid]:
        warnings[gid][uid] = []

    warnings[gid][uid].append(warning)

    save(WARNINGS, warnings)


def get_user_warnings(guild_id, user_id):
    warnings = load(WARNINGS)

    return (
        warnings
        .get(str(guild_id), {})
        .get(str(user_id), [])
    )


def get_all_warnings():
    return load(WARNINGS)
