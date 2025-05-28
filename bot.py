import os
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

# --- Configuration
GUILD_ID = 1352331475927830528  # Remplace par l’ID de ton serveur
SUPER_ADMIN_ROLE_ID = 1111111111111111111  # Remplace par l’ID du rôle Super Admin
STAFF_ROLE_ID = 2222222222222222222         # Remplace par l’ID du rôle Staff
SUPPORT_ROLE_ID = 3333333333333333333       # Remplace par l’ID du rôle Support

TOKEN = "NzI4MTIzNDU2Nzg5MTIzNDY1.XyZ_ABC12345dEfGhIjKlMnOpQrStUvWxYz"  # Remplace par ton vrai token Discord


# --- Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True
intents.guilds = True

MY_GUILD = discord.Object(id=GUILD_ID)

class CustomBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)
        self.session = None

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        try:
            self.tree.copy_global_to(guild=MY_GUILD)
            await self.tree.sync(guild=MY_GUILD)
            print("Commandes slash synchronisées avec succès !")
        except Exception as e:
            print(f"Erreur lors de la synchronisation des commandes : {e}")

    async def close(self):
        if self.session:
            await self.session.close()
        await super().close()

    async def on_error(self, event_method: str, *args, **kwargs):
        print(f"Erreur dans {event_method}: {args[0]}")

bot = CustomBot()

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")

async def handle_command(interaction: discord.Interaction, action_func):
    try:
        await action_func()
    except Exception as e:
        error_message = "Une erreur est survenue lors de l'exécution de la commande."
        print(f"[ERREUR] Détail : {e}")
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(error_message, ephemeral=True)
            else:
                await interaction.followup.send(error_message, ephemeral=True)
        except Exception as follow_up_error:
            print(f"Erreur lors de l'envoi du message d'erreur: {follow_up_error}")

def has_permission(interaction: discord.Interaction, allowed_roles: list[int]) -> bool:
    if not interaction.guild:
        return False
    member = interaction.guild.get_member(interaction.user.id)
    if not member:
        return False
    return any(role.id in allowed_roles for role in member.roles)

@bot.tree.command(name="admin", description="Attribue le rôle Super Admin à un utilisateur")
@app_commands.describe(pseudo="Sélectionnez un membre")
async def admin(interaction: discord.Interaction, pseudo: discord.Member):
    async def action():
        if not has_permission(interaction, [SUPER_ADMIN_ROLE_ID]):
            await interaction.response.send_message("Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
            return

        member = pseudo
        role_super = interaction.guild.get_role(SUPER_ADMIN_ROLE_ID)
        role_staff = interaction.guild.get_role(STAFF_ROLE_ID)
        role_support = interaction.guild.get_role(SUPPORT_ROLE_ID)

        # Retirer les rôles inférieurs
        if role_staff in member.roles:
            await member.remove_roles(role_staff)
        if role_support in member.roles:
            await member.remove_roles(role_support)

        if role_super not in member.roles:
            await member.add_roles(role_super)
            await interaction.response.send_message(f"Le rôle Super Admin a été attribué à {member.mention}.")
        else:
            await interaction.response.send_message(f"{member.mention} a déjà le rôle Super Admin.")

    await handle_command(interaction, action)

@bot.tree.command(name="staff", description="Attribue le rôle Staff à un utilisateur")
@app_commands.describe(pseudo="Sélectionnez un membre")
async def staff(interaction: discord.Interaction, pseudo: discord.Member):
    async def action():
        if not has_permission(interaction, [SUPER_ADMIN_ROLE_ID, STAFF_ROLE_ID]):
            await interaction.response.send_message("Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
            return

        member = pseudo
        role_super = interaction.guild.get_role(SUPER_ADMIN_ROLE_ID)
        role_staff = interaction.guild.get_role(STAFF_ROLE_ID)
        role_support = interaction.guild.get_role(SUPPORT_ROLE_ID)

        if role_super in member.roles:
            await interaction.response.send_message(f"{member.mention} a déjà un rôle supérieur.", ephemeral=True)
            return

        if role_support in member.roles:
            await member.remove_roles(role_support)

        if role_staff not in member.roles:
            await member.add_roles(role_staff)
            await interaction.response.send_message(f"Le rôle Staff a été attribué à {member.mention}.")
        else:
            await interaction.response.send_message(f"{member.mention} a déjà le rôle Staff.")

    await handle_command(interaction, action)

@bot.tree.command(name="support", description="Attribue le rôle Support à un utilisateur")
@app_commands.describe(pseudo="Sélectionnez un membre")
async def support(interaction: discord.Interaction, pseudo: discord.Member):
    async def action():
        if not has_permission(interaction, [SUPER_ADMIN_ROLE_ID, STAFF_ROLE_ID]):
            await interaction.response.send_message("Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)
            return

        member = pseudo
        role_super = interaction.guild.get_role(SUPER_ADMIN_ROLE_ID)
        role_staff = interaction.guild.get_role(STAFF_ROLE_ID)
        role_support = interaction.guild.get_role(SUPPORT_ROLE_ID)

        if role_super in member.roles or role_staff in member.roles:
            await interaction.response.send_message(f"{member.mention} a déjà un rôle supérieur.", ephemeral=True)
            return

        if role_support not in member.roles:
            await member.add_roles(role_support)
            await interaction.response.send_message(f"Le rôle Support a été attribué à {member.mention}.")
        else:
            await interaction.response.send_message(f"{member.mention} a déjà le rôle Support.")

    await handle_command(interaction, action)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    try:
        error_msg = "Une erreur est survenue lors de l'exécution de la commande."

        if isinstance(error, app_commands.CommandOnCooldown):
            error_msg = f"Cette commande est en cooldown. Réessayez dans {error.retry_after:.2f} secondes."
        elif isinstance(error, app_commands.CommandInvokeError):
            print(f"Erreur originale: {error.original}")
            error_msg = "Une erreur s'est produite lors de l'exécution de la commande."
        elif isinstance(error, app_commands.TransformerError):
            error_msg = "Erreur de conversion des paramètres de la commande."
            print(f"Erreur de transformation: {error}")

        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(error_msg, ephemeral=True)
            else:
                await interaction.followup.send(error_msg, ephemeral=True)
        except discord.errors.InteractionNotResponded:
            await interaction.followup.send(error_msg, ephemeral=True)
    except Exception as e:
        print(f"Erreur critique dans le gestionnaire d'erreurs: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)
