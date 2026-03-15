import discord
from discord.ext import commands
import database

class Monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # ignora mensagens do proprio bot
        if message.author.bot:
            return

        # busca todos os usuarios cadastrados
        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT user_id FROM keywords")
        users = cursor.fetchall()
        conn.close()

        for (user_id,) in users:
            # ignora se o usuario estiver pausado
            if database.is_paused(user_id):
                continue

            # verifica se o canal esta sendo monitorado
            channels = database.list_channels(user_id)
            if channels and str(message.channel.id) not in channels:
                continue

            # busca palavras-chave do usuario
            keywords = database.list_keywords(user_id)

            for keyword in keywords:
                if keyword.lower() in message.content.lower():
                    # ignora se a mensagem foi enviada pelo proprio usuario
                    if str(message.author.id) == user_id:
                        continue

                    # destaca a palavra-chave em negrito
                    conteudo = message.content
                    conteudo_destacado = conteudo.replace(
                        keyword,
                        f"**{keyword}**"
                    )

                    # busca o usuario para mandar DM
                    user = await self.bot.fetch_user(int(user_id))

                    embed = discord.Embed(
                        title="🔔 Vigil — Palavra-chave detectada!",
                        color=discord.Color.orange()
                    )
                    embed.add_field(name="Palavra-chave", value=f"**{keyword}**", inline=False)
                    embed.add_field(name="Mensagem", value=conteudo_destacado, inline=False)
                    embed.add_field(name="Canal", value=message.channel.mention, inline=False)
                    embed.add_field(name="Enviado por", value=message.author.mention, inline=False)
                    embed.add_field(name="Servidor", value=message.guild.name, inline=False)

                    try:
                        await user.send(embed=embed)
                    except discord.Forbidden:
                        pass  # usuario bloqueou DMs

async def setup(bot):
    await bot.add_cog(Monitor(bot))