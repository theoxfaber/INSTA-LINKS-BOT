<p align="center">
  <img src="banner.png" alt="Professor-Bot Banner" width="100%">
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com/?lines=𝗧𝗛𝗜𝗦+𝗜𝗦+𝐏𝐑𝐎𝐅𝐄𝐒𝐒𝐎𝐑+𝐁𝐎𝐓!;𝗖𝗥𝗘𝗔𝗧𝗘𝗗+𝗕𝗬+𝗠𝗞𝗡+𝗕𝗢𝗧𝗭™;𝗧𝗛𝗘+𝗙𝗨𝗧𝗨𝗥𝗘+𝗢𝗙+𝗧𝗚+𝗔𝗨𝗧𝗢𝗙𝗜𝗟𝗧𝗘𝗥𝗜𝗡𝗚!" alt="Typing SVG">
</p>

<p align="center">
  <a href="https://github.com/MrMKN/PROFESSOR-BOT/stargazers"><img src="https://img.shields.io/github/stars/MrMKN/PROFESSOR-BOT?style=for-the-badge&color=yellow&logo=github" alt="Stars"></a>
  <a href="https://github.com/MrMKN/PROFESSOR-BOT/network/members"><img src="https://img.shields.io/github/forks/MrMKN/PROFESSOR-BOT?style=for-the-badge&color=orange&logo=github" alt="Forks"></a>
  <a href="https://github.com/MrMKN/PROFESSOR-BOT/issues"><img src="https://img.shields.io/github/issues/MrMKN/PROFESSOR-BOT?style=for-the-badge&color=red&logo=github" alt="Issues"></a>
  <a href="https://github.com/MrMKN/PROFESSOR-BOT/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-AGPL-blue?style=for-the-badge&logo=opensourceinitiative" alt="License"></a>
</p>

---

## 🚀 Overview

**Professor-Bot** is a high-performance, feature-rich Telegram Auto-Filter Bot designed for scale and intelligence. Built with **Pyrogram**, **MongoDB**, and **Redis**, it now features cutting-edge **Semantic Vector Search** and **Rust-powered indexing** for near-instant results across millions of files.

<details>
<summary><b>Features Checklist</b></summary>

- [x] ⚡ Auto & Manual Filters
- [x] 🧠 Semantic Vector Search
- [x] 🔍 RapidFuzz Typo Handling
- [x] 🎞️ IMDB Integration (Posters, Ratings)
- [x] 🔋 Redis-based State Persistence
- [x] 🦀 Rust-powered Search Engine (Tantivy)
- [x] 🐳 Dockerized Deployment
- [x] ✉️ Broadcast & Group Management
</details>

---

## 🔥 Key Upgrades (v4.5.1)

| Feature | Description | Status |
| :--- | :--- | :---: |
| 🛡️ **RCE Patch** | Replaced `eval()` with `ast.literal_eval()` for top-tier security. | ✅ |
| ⚡ **Redis Migration** | In-memory state now persists in Redis with optimized TTL. | ✅ |
| 🧠 **Semantic Search** | Natural language query support via `sentence-transformers`. | ✅ |
| 🔍 **Fuzzy Matching** | Local `rapidfuzz` WRatio matching for effortless typo handling. | ✅ |
| 🦀 **Rust Engine** | Tantivy-based inverted index for sub-5ms lookup speeds. | ✅ |

---

## ⚙️ Configuration

### 🔑 Essential Variables

<<<<<<< HEAD
| Variable | Description | Source |
| :--- | :--- | :--- |
| `BOT_TOKEN` | Your Telegram Bot Token | [@BotFather](https://t.me/BotFather) |
| `API_ID` / `HASH` | Telegram API credentials | [my.telegram.org](https://my.telegram.org) |
| `DATABASE_URL` | MongoDB Connection URI | [MongoDB Atlas](https://mongodb.com) |
| `REDIS_URL` | Redis URL for state caching | Local or Cloud Redis |

### 🛠️ Advanced Features

- **Auto & Manual Filters**: Modular response systems for groups and PMs.
- **IMDB Integration**: Automatic posters, ratings, and genre metadata.
- **Global Filters**: Admin-controlled responses across all connected chats.
- **Vector Search**: Search for content by "meaning" rather than just exact words.

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/mongodb-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/rust-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white" alt="Rust">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

## 📦 Deployment

### 🐳 Docker (Recommended)

```bash
docker-compose up --build -d
```

<details>
<summary><b>Deploy to VPS (Manual)</b></summary>

```bash
apt update && apt upgrade -y
apt install git -y  
git clone https://github.com/MrMKN/PROFESSOR-BOT 
cd PROFESSOR-BOT
bash vps.sh
```
</details>

<details>
<summary><b>Basic Commands</b></summary>

```
start - check bot alive
settings - get settings 
logs - to get the rescent errors
restart - restart the server
update - update from git latest 
stats - to get status of files in db.
filter - add manual filters
filters - view filters
connect - connect to PM.
disconnect - disconnect from PM
connections - check all connections
del - delete a filter
delall - delete all filters
deleteall - delete all index(autofilter)
delete - delete a specific file from index.
info - get user info
id - get tg ids.
imdb - fetch info from imdb.
users - to get list of my users and ids.
chats - to get list of the my chats and ids 
leave  - to leave from a chat.
disable  -  do disable a chat.
enable - re-enable chat.
ban_user  - to ban a user.
unban_user  - to unban a user.
channel - to get list of total connected channels
broadcast - to broadcast a message
```
</details>
```

### ☁️ Heroku / Koyeb

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/MrMKN/PROFESSOR-BOT)
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/MrMKN/PROFESSOR-BOT)

---

## 🤝 Support & Community

* 📢 [MKN UPDATES](https://t.me/mkn_bots_updates) - Get the latest news and features.
* 💬 [SUPPORT GROUP](https://t.me/TeamEvamaria) - Join our community for help.

---

## 📜 License & Credits

- Derived from **Team Eva-Maria**. Special thanks to the original contributors.
- Licensed under **GNU AGPL 3.0**.
- **Disclaimer**: Unauthorized selling of this code is strictly prohibited.

---

<p align="center">
  <b>Built with ❤️ by <a href="https://t.me/Mr_MKN">Mʀ.MKN</a></b>
</p>
