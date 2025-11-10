function sendText() {
    const text = document.getElementById("text").value;

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("response").innerText = data.reply;
            speak(data.reply); // 🔊 speak result
        });
}

// ✅ SPEECH RECOGNITION
function startListening() {
    const mic = document.getElementById("micBtn");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech recognition not supported in this browser");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    mic.innerText = "🎤 Listening...";

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        document.getElementById("text").value = text;
        sendText();
        mic.innerText = "🎤 Speak";
    };

    recognition.onerror = () => {
        mic.innerText = "🎤 Speak";
        alert("Error recognizing speech");
    };
}

// ✅ TEXT → SPEECH
function speak(message) {
    const speech = new SpeechSynthesisUtterance(message);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
}
