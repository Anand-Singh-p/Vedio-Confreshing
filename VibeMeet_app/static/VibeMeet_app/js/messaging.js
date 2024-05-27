// messaging.js

// Get the message input field and message list
const messageInput = document.getElementById('messageInput');
const messageList = document.getElementById('messageList');

// Function to send a message
function sendMessage() {
    const message = messageInput.value.trim();
    if (message !== '') {
        // Display the sent message in the UI
        displayMessage('You', message);
        // Send the message using WebRTC data channel (implementation required)
        // For example: sendDataMessage(message);
        // Clear the message input field
        messageInput.value = '';
    }
}

// Function to receive a message
function receiveMessage(sender, message) {
    // Display the received message in the UI
    displayMessage(sender, message);
}

// Function to display a message in the UI
function displayMessage(sender, message) {
    const li = document.createElement('li');
    li.textContent = `${sender}: ${message}`;
    messageList.appendChild(li);
}
