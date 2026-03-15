import discord
from discord.ext import commands
import database

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pause")
    async def pause(self, ctx):
        user_id = str(ctx.author.id)

        if database.is_paused(user_id):
            await ctx.send("⚠️ Suas notificações já estão pausadas!")
            return

        database.set_paused(user_id, 1)
        await ctx.send("⏸️ Notificações pausadas com sucesso!")

    @commands.command(name="return")
    async def return_notifications(self, ctx):
        user_id = str(ctx.author.id)

        if not database.is_paused(user_id):
            await ctx.send("⚠️ Suas notificações já estão ativas!")
            return

        database.set_paused(user_id, 0)
        await ctx.send("▶️ Notificações retomadas com sucesso!")

    @commands.command(name="status")
    async def status(self, ctx):
        user_id = str(ctx.author.id)
        keywords = database.list_keywords(user_id)
        channels = database.list_channels(user_id)
        paused = database.is_paused(user_id)

        keywords_text = "\n".join([f"• {k}" for k in keywords]) if keywords else "Nenhuma"
        channels_text = "\n".join([f"• <#{c}>" for c in channels]) if channels else "Nenhum"
        status_text = "⏸️ Pausado" if paused else "▶️ Ativo"

        embed = discord.Embed(title="📊 Status do Vigil", color=discord.Color.blue())
        embed.add_field(name="Status", value=status_text, inline=False)
        embed.add_field(name="Palavras-chave", value=keywords_text, inline=False)
        embed.add_field(name="Canais monitorados", value=channels_text, inline=False)
        embed.set_footer(text=f"Usuário: {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command(name="commands")
    async def help_command(self, ctx):
        embed = discord.Embed(title="📖 Comandos do Vigil", color=discord.Color.blue())
        embed.add_field(name="🔍 Palavras-chave", value="`!add <palavra>` → Adiciona palavra-chave\n`!remove <palavra>` → Remove palavra-chave\n`!list` → Lista suas palavras-chave", inline=False)
        embed.add_field(name="📡 Canais", value="`!vigil <canal>` → Monitora um canal\n`!ignore <canal>` → Para de monitorar\n`!chan` → Lista canais monitorados", inline=False)
        embed.add_field(name="⚙️ Configurações", value="`!pause` → Pausa notificações\n`!return` → Retoma notificações\n`!status` → Exibe seu status", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Config(bot))