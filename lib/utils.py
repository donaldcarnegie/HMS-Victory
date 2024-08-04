# lib/utils.py
from datetime import datetime, timezone
import discord

async def restrict_channel_for_new_members(message: discord.Message, channel_id: int, days_required: int = 7, whitelisted_user_ids: list[int] = []):
    if message.channel.id == channel_id:
        if message.author.id in whitelisted_user_ids:
            return True
        join_date = message.author.joined_at
        if join_date is None or (datetime.now(timezone.utc) - join_date).days < days_required:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, you need to be in the server for at least {days_required} days to use this channel. If you believe you should be whitelisted, please <#1143560594138595439>",
                delete_after=10,
            )
            return False
    return True