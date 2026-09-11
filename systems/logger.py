import os
import json
from datetime import datetime


LOG_DIR = "data/logs"


def ensure_logs():
    os.makedirs(LOG_DIR, exist_ok=True)


def log_message(
    user,
    guild,
    channel,
    message,
    response
):
    ensure_logs()

    entry = {
        "time": datetime.now().isoformat(),

        "user": {
            "id": user.id,
            "display_name": user.display_name
        },

        "server": {
            "id": guild.id,
            "name": guild.name
        },

        "channel": {
            "id": channel.id,
            "name": channel.name
        },

        "message": message,
        "response": response
    }

    # Terminal output
    print("\n" + "=" * 60)
    print(f"User: {user.display_name}")
    print(f"Server: {guild.name}")
    print(f"Channel: {channel.name}")
    print(f"Message: {message}")
    print(f"Bot: {response}")
    print("=" * 60)


    # Per-server log file
    path = f"{LOG_DIR}/{guild.id}.json"

    logs = []

    if os.path.exists(path):
        with open(path, "r") as f:
            logs = json.load(f)

    logs.append(entry)

    with open(path, "w") as f:
        json.dump(
            logs,
            f,
            indent=4
        )


def log_command(ctx, response):
    """
    Shortcut for Discord commands.
    """

    log_message(
        ctx.author,
        ctx.guild,
        ctx.channel,
        ctx.message.content,
        response
    )
