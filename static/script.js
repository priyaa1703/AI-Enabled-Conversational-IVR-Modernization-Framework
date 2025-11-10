const SEND_URL = "/predict";
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const textEl = document.getElementById("text");
const responseText = document.getElementById("responseText");

sendBtn.onclick = () => sendText();
micBtn.onclick = () => startListening();

async function sendText(){
    const text = textEl.value || "";
    responseText.innerText = "Thinking...";
    try{
        const res = await fetch(SEND_URL, {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({text})
        });
        const data = await res.json();
        responseText.innerText = data.reply || JSON.stringify(data);
        speak(data.reply || data.intent || "No reply");
    }catch(err){
        responseText.innerText = "Error connecting to backend";
        console.error(err);
    }
}

function startListening(){
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if(!SpeechRecognition){ alert("Speech recognition not supported"); return; }
    const rec = new SpeechRecognition();
    rec.lang = "en-US";
    rec.onresult = (e) => {
        textEl.value = e.results[0][0].transcript;
        sendText();
    };
    rec.onerror = () => { alert("Speech recognition error"); };
    rec.start();
}

function speak(msg){
    if(!msg) return;
    const u = new SpeechSynthesisUtterance(msg);
    u.lang = "en-US";
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
}
