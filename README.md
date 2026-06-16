# 🎉 sb0t Random Greeter + Real-Time XML Sync

A small automation project for **sb0t chat rooms** — automatically greets users with a random message when they join, and keeps the greeting list in sync across two locations in real time.

---

## 📦 What's included

| File | Description |
|------|-------------|
| `bienvenida.js` | sb0t script — greets users on join with a random message from XML |
| `sync_greetings.py` | Python watcher — keeps both `greetings.xml` files in sync |

---

## 🧠 How it works

### `bienvenida.js` — The greeter

A JavaScript script that runs inside the **sb0t scripting engine**.

- On load, reads `greetings.xml` and parses all `<item>` nodes
- When a user joins the room, picks a **random greeting** and sends it to chat
- Supports dynamic placeholders: `+nick` / `+n` (username) and `+id` (user ID)
- Uses `onTimer()` to **hot-reload** the XML every 60 ticks — no restart needed if the file changes

```js
function onJoin(userobj) {
    var item = items[Math.floor(Math.random() * items.length)];
    var msg = item.nodeValue
        .replace("+nick", userobj.name)
        .replace("+n", userobj.name)
        .replace("+id", userobj.id);
    print(0, msg);
}
```

---

### `sync_greetings.py` — The sync watcher

A Python script that runs in the background (or as a Windows service).

- Checks every **5 seconds** if the original `greetings.xml` has changed
- Detects changes by comparing **file timestamps** and **byte content**
- Automatically copies the updated file to the script's `Data/` folder
- Logs all activity to console and `sync_greetings.log`

```
Original:  ...sb0t.exe\greetings.xml
    |
    |  (Python copies in ~5s)
    v
Copy:      ...sb0t.exe\Scripting\bienvenida.js\Data\greetings.xml
    |
    |  (JS reloads in ~60s)
    v
Live in chat
```

---

## ⏱️ Update timing

| Step | Max delay |
|------|-----------|
| Python detects change & copies file | ~5 seconds |
| JS script detects new file & reloads | ~60 seconds |
| **Total end-to-end** | **~65 seconds** |

> You can lower `CHECK_EVERY` in `bienvenida.js` for faster reloads (e.g. `10` = ~15s total).

---

## 🚀 Setup

### Requirements

- Python 3.x
- sb0t with scripting support enabled

### 1. Place the files

```
C:\Users\Administrator\AppData\Roaming\sb0t\sb0t.exe\
│
├── greetings.xml                          ← main file (edit this one)
│
└── Scripting\
    └── bienvenida.js\
        ├── bienvenida.js                  ← greeter script
        └── Data\
            └── greetings.xml              ← auto-synced copy
```

### 2. Run the Python watcher

```bash
python sync_greetings.py
```

Leave it running in the background. It will keep both XML files in sync automatically.

### 3. Load the script in sb0t

Load `bienvenida.js` through the sb0t scripting panel. It will print a confirmation on load:

```
Bienvenida.js ha sido cargado
```

---

## 📄 greetings.xml format

```xml
<greetings>
    <item>Welcome to the room, +nick!</item>
    <item>Hey +n, glad you joined us!</item>
    <item>Hello +nick, your ID is +id</item>
</greetings>
```

Edit only the **original** file — Python handles the rest.

---

## 📝 Notes

- The Python script logs to `sync_greetings.log` in the same directory
- The sync is **one-way**: original → copy. Never edit the copy directly
- The JS hot-reload compares file size — if content changes but size stays the same (rare edge case), restart the script manually

---

## 👤 Author

Made for personal use with the sb0t chat platform.
