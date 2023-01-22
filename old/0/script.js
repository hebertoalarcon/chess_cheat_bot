const socket = io("http://127.0.0.1:5000");

socket.on('moves', (data) => {
    console.log("moves:", data);
    document.getElementById('moves').innerHTML = JSON.stringify(data, null, 2);
});