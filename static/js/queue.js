
function inqueue() {
    var name = prompt("Input Movie Name: ");
    if (name == null) {
        alert("NULL Input");
        return;
    }
    mySocket = io.connect();
    mySocket.emit('inqueue', name);
    alert(name);

}