import os

from dotenv import load_dotenv

load_dotenv()


OWNER_ID = int(
    os.getenv("BOT_OWNER_ID", 0)
)


def has_role(member, role_id):
    if not role_id:
        return False

    return any(
        role.id == role_id
        for role in member.roles
    )


def is_owner(member):
    return member.id == OWNER_ID


def is_admin(member, config):
    return (
        is_owner(member)
        or has_role(
            member,
            config.get("admin_role")
        )
    )


def is_mod(member, config):
    return (
        is_admin(member, config)
        or has_role(
            member,
            config.get("mod_role")
        )
    )


def is_helper(member, config):
    return (
        is_mod(member, config)
        or has_role(
            member,
            config.get("helper_role")
        )
    )
