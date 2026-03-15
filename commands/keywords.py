from discord.ext import commands
import database

class Keywords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add")
    async def add_keyword(self, ctx, *, keyword: str):
        user_id = str(ctx.author.id)
        keywords = database.list_keywords(user_id)
        
        if keyword.lower() in [k.lower() for k in keywords]:
            await ctx.send(f"A palavra-chave **{keyword}** já está sendo monitorada!")
            return
        
        database.add_keyword(user_id, keyword.lower())
        await ctx.send(f"✅ Palavra-chave **{keyword}** adicionada com sucesso!")

    @commands.command(name="remove")
    async def remove_keyword(self, ctx, *, keyword: str):
        user_id = str(ctx.author.id)
        keywords = database.list_keywords(user_id)

        if keyword.lower() not in [k.lower() for k in keywords]:
            await ctx.send(f"A palavra-chave **{keyword}** não existe na sua lista!")
            return

        database.remove_keyword(user_id, keyword.lower())
        await ctx.send(f"🗑️ Palavra-chave **{keyword}** removida com sucesso!")

    @commands.command(name="list")
    async def list_keywords(self, ctx):
        user_id = str(ctx.author.id)
        keywords = database.list_keywords(user_id)

        if not keywords:
            await ctx.send("Você não tem nenhuma palavra-chave cadastrada!")
            return

        lista = "\n".join([f"• {k}" for k in keywords])
        await ctx.send(f"🔍 **Suas palavras-chave:**\n{lista}")

async def setup(bot):
    await bot.add_cog(Keywords(bot))