// Establish WebSocket connection
const socket = new WebSocket(`ws://localhost:8000/ws/chat/${ticket.pk}/`);


// Send message to the WebSocket server
function sendMessage(message) {
  socket.send(JSON.stringify({
    'message': message
  }));
}

// Handle incoming messages from the WebSocket server
socket.onmessage = function(event) {
  const message = JSON.parse(event.data);
  // Handle the incoming message here, e.g. display it in the chat interface
};

// Handle form submission to send a new message
const form = document.getElementById('chat-form');
const input = document.getElementById('chat-input');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  const message = input.value;
  sendMessage(message);
  input.value = '';
});
