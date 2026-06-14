print(0, "Bienvenida.js ha sido cargado");

var gmsg = File.load("greetings.xml").split("\r\n");
var parser = new XmlParser();
parser.load(gmsg);
var items = parser.getNodesByName("item");

function onJoin(userobj){
    var item = items[Math.floor(Math.random() * items.length)];
    var msg = item.nodeValue
        .replace("+nick", userobj.name)
        .replace("+n", userobj.name)
        .replace("+id", userobj.id);
    print(0, msg);
}
