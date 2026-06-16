// bienvenida.js — auto-reloads greetings.xml when the file changes

print(0, "Bienvenida.js ha sido cargado");

var FILENAME     = "greetings.xml";
var CHECK_EVERY  = 60;   // seconds between file-change checks
var _tickCounter = 0;
var _lastSize    = -1;   // track file size to detect changes

// ── Initial load ─────────────────────────────────────────────────────────────
var gmsg  = [];
var items = [];

function loadGreetings() {
    var raw = File.load(FILENAME);
    if (!raw || raw.length === 0) {
        print(0, "[Bienvenida] AVISO: greetings.xml está vacío o no se encontró.");
        return false;
    }

    gmsg = raw.split("\r\n");

    var parser = new XmlParser();
    parser.load(gmsg);
    items = parser.getNodesByName("item");

    _lastSize = raw.length;
    print(0, "[Bienvenida] greetings.xml cargado — " + items.length + " entradas.");
    return true;
}

loadGreetings();   // load on startup

// ── Timer — runs every engine tick ───────────────────────────────────────────
function onTimer() {
    _tickCounter++;

    // Only check every CHECK_EVERY ticks (≈ seconds, depending on engine tick rate)
    if (_tickCounter < CHECK_EVERY) return;
    _tickCounter = 0;

    var raw = File.load(FILENAME);
    if (!raw) return;

    // Reload only if the file size has changed (fast, no XML re-parse otherwise)
    if (raw.length !== _lastSize) {
        print(0, "[Bienvenida] greetings.xml modificado — recargando...");
        gmsg = raw.split("\r\n");

        var parser = new XmlParser();
        parser.load(gmsg);
        items = parser.getNodesByName("item");

        _lastSize = raw.length;
        print(0, "[Bienvenida] Recarga completada — " + items.length + " entradas.");
    }
}

// ── Join handler ─────────────────────────────────────────────────────────────
function onJoin(userobj) {
    if (!items || items.length === 0) return;

    var item = items[Math.floor(Math.random() * items.length)];
    var msg  = item.nodeValue
        .replace("+nick", userobj.name)
        .replace("+n",    userobj.name)
        .replace("+id",   userobj.id);

    print(0, msg);
}
