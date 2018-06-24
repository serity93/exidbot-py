def get_guild_role(role_id, roles):
    for role in roles:
        if role.id == role_id:
            return role