import discord
from discord.ext import commands
import database

class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vigil")
    async def add_channel(self, ctx, channel: discord.TextChannel):
        user_id = str(ctx.author.id)
        channels = database.list_channels(user_id)

        if str(channel.id) in channels:
            await ctx.send(f"O canal {channel.mention} já está sendo monitorado!")
            return

        database.add_channel(user_id, str(channel.id))
        await ctx.send(f"✅ Canal {channel.mention} adicionado ao monitoramento!")

    @commands.command(name="ignore")
    async def remove_channel(self, ctx, channel: discord.TextChannel):
        user_id = str(ctx.author.id)
        channels = database.list_channels(user_id)

        if str(channel.id) not in channels:
            await ctx.send(f"O canal {channel.mention} não está sendo monitorado!")
            return

        database.remove_channel(user_id, str(channel.id))
        await ctx.send(f"🗑️ Canal {channel.mention} removido do monitoramento!")

    @commands.command(name="chan")
    async def list_channels(self, ctx):
        user_id = str(ctx.author.id)
        channels = database.list_channels(user_id)

        if not channels:
            await ctx.send("Você não está monitorando nenhum canal!")
            return

        lista = "\n".join([f"• <#{c}>" for c in channels])
        await ctx.send(f"📡 **Canais monitorados:**\n{lista}")

async def setup(bot):
    await bot.add_cog(Channels(bot))