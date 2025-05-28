# Bot Discord de gestion des rôles

Ce bot permet d’attribuer des rôles (`Super Admin`, `Staff`, `Support`) à des membres via des commandes slash.  
Les permissions sont gérées :  
- Super Admin peut tout faire  
- Staff peut exécuter `/staff` et `/support`  
- Support a seulement son rôle

---

## Prérequis

- Python 3.8 ou plus
- Un bot Discord créé sur [Discord Developer Portal](https://discord.com/developers/applications)
- Les intents privilégiés activés (intents membres et contenu des messages)

---

## Étape 1 : Créer le bot sur Discord

1. Va sur https://discord.com/developers/applications  
2. Clique sur "New Application" → donne un nom → crée l’application  
3. Va dans l’onglet "Bot" → clique sur "Add Bot"  
4. Active **Privileged Gateway Intents** :  
   - `SERVER MEMBERS INTENT`  
   - `MESSAGE CONTENT INTENT`  
5. Copie le **Token** du bot (garde-le secret !)  

---

## Étape 2 : Inviter le bot sur ton serveur

1. Dans le portail développeur, va dans "OAuth2" → "URL Generator"  
2. Coche :  
   - `bot`  
   - `applications.commands`  
3. Dans "Bot Permissions", coche :  
   - `Manage Roles`  
   - `Read Messages/View Channels`  
   - `Send Messages`  
   - `Use Slash Commands`  
4. Copie l’URL générée, ouvre-la dans un navigateur  
5. Invite le bot sur ton serveur Discord

---

## Étape 3 : Installer Python et les dépendances

- avoir Python 3.8+ ([téléchargement Python](https://www.python.org/downloads/))  
- Ouvre un terminal  
- Installe les librairies nécessaires :
  pip install discord.py aiohttp

## Étape 4 : Préparer le code
Ouvre le fichier bot.py.

Configure les IDs des rôles et le token dans le fichier bot.py en remplaçant les valeurs par celles correspondant à ton serveur Discord et ton bot :

GUILD_ID = 1352331475927830528  # Remplace par l’ID de ton serveur

SUPER_ADMIN_ROLE_ID = 1111111111111111111  # Remplace par l’ID du rôle Super Admin

STAFF_ROLE_ID = 2222222222222222222         # Remplace par l’ID du rôle Staff

SUPPORT_ROLE_ID = 3333333333333333333       # Remplace par l’ID du rôle Support

TOKEN = "NzI4MTIzNDU2Nzg5MTIzNDY1.XyZ_ABC12345dEfGhIjKlMnOpQrStUvWxYz"  # Remplace par ton vrai token Discord
