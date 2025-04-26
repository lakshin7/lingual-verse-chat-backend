document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('userInput');

    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
        messageDiv.innerHTML = `<strong>${isUser ? 'You' : 'Chatbot'}:</strong> ${message}`;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    async function sendMessage(endpoint) {
        const message = userInput.value;
        if (!message) return alert("Please enter a message.");
        addMessage(message, true);
        try {
            const response = await fetch(`http://127.0.0.1:5001/${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            addMessage(data.reply, false);
        } catch (error) {
            console.error("Error:", error);
            addMessage("An error occurred.", false);
        }
        userInput.value = '';
    }

    document.getElementById('sendButton').addEventListener('click', () => sendMessage('chat'));
    document.getElementById('correctGrammarButton').addEventListener('click', () => sendMessage('correct'));
    document.getElementById('translateButton').addEventListener('click', () => {
        const targetLang = document.getElementById('languageSelect').value;
        sendMessage(`translate?target_lang=${targetLang}`);
    });
    document.getElementById('analyzeSentimentButton').addEventListener('click', () => sendMessage('sentiment'));
    document.getElementById('textToSpeechButton').addEventListener('click', () => sendMessage('tts'));
});
