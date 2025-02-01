import discord
import asyncio
import os
import platform
import requests
from colorama import Fore, Style
import re

# Ön Arayüz Başlangıcı
mytitle = "cimidi Emoji Klonlama Aracı"
os.system(f"title {mytitle}")

client = discord.Client()

# Terminal temizleme işlemi
if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")
    print(chr(27) + "[2J")

print(f"""{Fore.RED}
██████╗██╗███╗   ███╗██╗██████╗ ██╗
██╔════╝██║████╗ ████║██║██╔══██╗██║
██║     ██║██╔████╔██║██║██║  ██║██║
██║     ██║██║╚██╔╝██║██║██║  ██║██║
╚██████╗██║██║ ╚═╝ ██║██║██████╔╝██║
 ╚═════╝╚═╝╚═╝     ╚═╝╚═╝╚═════╝ ╚═╝
                   cimidi - Biz bu sporu yapıyoruz kankam <3
                   Ücretli Discord Botları için discord.gg/devcode
{Style.RESET_ALL}
""")

# Kullanıcıdan bilgileri al
token = input(f'Token:\n > ')
guild_s = input('Hedef Sunucu ID:\n > ')

# Geçersiz karakterleri temizleme fonksiyonu
def sanitize_name(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

# Emojileri kaydetme fonksiyonu
def download_emoji(emoji_id, emoji_name, guild_folder, is_animated):
    folder_type = "GIFs" if is_animated else "PNGs"
    emoji_folder = f"{guild_folder}/{folder_type}"
    
    if not os.path.exists(emoji_folder):
        os.makedirs(emoji_folder)

    extension = "gif" if is_animated else "png"
    url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{extension}"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{emoji_folder}/{emoji_name}.{extension}", 'wb') as f:
            f.write(response.content)
        print(f"{Fore.GREEN}✅ {emoji_name}.{extension} indirildi.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ {emoji_name}.{extension} indirilemedi.{Style.RESET_ALL}")

# Emojileri çekme fonksiyonu
async def fetch_emojis(guild):
    guild_name = sanitize_name(guild.name)
    guild_folder = f"Emojis/{guild_name}"
    
    for emoji in await guild.fetch_emojis():
        download_emoji(emoji.id, emoji.name, guild_folder, emoji.animated)

@client.event
async def on_ready():
    print(f"Giriş Yapıldı: {client.user}")
    print("🎯 Aktarım Başladı...")

    guild_from = client.get_guild(int(guild_s))

    if guild_from:
        await fetch_emojis(guild_from)
        print(f"""{Fore.GREEN}
✅ Emojiler Başarıyla {guild_from.name} Klasörüne PNGs ve GIFs Olarak Ayrıldı...
{Style.RESET_ALL}""")
    else:
        print(f"{Fore.RED}❌ Sunucu bulunamadı!{Style.RESET_ALL}")

    await asyncio.sleep(5)
    await client.close()

client.run(token, bot=False)
