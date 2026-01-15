// -------- Persistent Player ID --------
let playerId = localStorage.getItem("playerId");

if (!playerId) {
  playerId = crypto.randomUUID();
  localStorage.setItem("playerId", playerId);
}

// -------- WebSocket --------
const ws = new WebSocket(`ws://localhost:8000/ws?playerId=${playerId}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "room_created") {
    localStorage.setItem("roomData", JSON.stringify(data.room));
    window.location.href = "lobby.html";
  }

  if (data.type === "lobby_update") {
  localStorage.setItem("roomData", JSON.stringify(data.room));

  // If not already in lobby, redirect
  if (!window.location.pathname.includes("lobby.html")) {
    window.location.href = "lobby.html";
    return;
  }

  renderLobby(data.room);
}

  if (data.type === "game_started") {
    alert("Game starting (Phaser comes next)");
  }

  if (data.type === "error") {
    alert(data.message);
  }
};

// -------- Actions --------
function createRoom() {
  ws.send(JSON.stringify({ type: "create_room" }));
}

function joinRoom() {
  const code = prompt("Enter Room Code");
  if (!code) return;
  ws.send(JSON.stringify({
    type: "join_room",
    room_code: code.toUpperCase()
  }));
}

// -------- Lobby Rendering --------
function renderLobby(room) {
  if (!document.getElementById("players")) return;

  document.getElementById("code").innerText = room.code;
  const list = document.getElementById("players");
  list.innerHTML = "";

  room.players.forEach(pid => {
    const li = document.createElement("li");
    li.textContent = pid === room.host ? `${pid} (Host)` : pid;
    list.appendChild(li);
  });

  const startBtn = document.getElementById("startBtn");
  startBtn.disabled = !(playerId === room.host && room.players.length >= 2);
}

function startGame() {
  ws.send(JSON.stringify({ type: "start_game" }));
}
