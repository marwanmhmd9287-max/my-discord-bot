import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. نظام الترحيب والرتب التلقائية
@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
    auto_role = discord.utils.get(member.guild.roles, name="Member")
    
    if auto_role:
        await member.add_roles(auto_role)
        
    if welcome_channel:
        embed = discord.Embed(
            title="ترحيب بالأعضاء!",
            description=f"أهلاً بك {member.mention} في السيرفر! 🥳",
            color=discord.Color.green()
        )
        await welcome_channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم {bot.user}')

# 2. نظام التذاكر (Ticket System)
class TicketButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="فتح تذكرة دعم 📩", style=discord.ButtonStyle.primary, custom_id="ticket_button")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(name=f"ticket-{member.name}", overwrites=overwrites)
        await interaction.response.send_message(f"تم إنشاء تذكرتك هنا: {channel.mention}", ephemeral=True)
        await channel.send(f"أهلاً بك {member.mention}! كيف يمكننا مساعدتك اليوم؟")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title="الدعم الفني والخدمات",
        description="اضغط على الزر بالأسفل لفتح تذكرة خاصة بك.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketButton())

# bot.run('YOUR_BOT_TOKEN')
