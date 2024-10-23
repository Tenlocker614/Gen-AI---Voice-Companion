const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const transcriptionElement = document.getElementById("transcription");
const canvas = document.getElementById("waveform");
const ctx = canvas.getContext("2d");

let mediaRecorder;
let audioChunks = [];
let audioContext;
let analyser;

startBtn.addEventListener("click", async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaStreamSource(stream);
    source.connect(analyser);
    analyser.fftSize = 2048;

    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const audioUrl = URL.createObjectURL(audioBlob);
        transcribeAudio(audioBlob);
    };

    visualize();
});

stopBtn.addEventListener("click", () => {
    mediaRecorder.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
});

function visualize() {
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
        requestAnimationFrame(draw);
        analyser.getByteTimeDomainData(dataArray);
        ctx.fillStyle = 'rgba(30, 30, 30, 1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.lineWidth = 2;
        ctx.strokeStyle = 'cyan';
        ctx.beginPath();

        const sliceWidth = canvas.width / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const v = dataArray[i] / 128.0; // Normalize to 0-1
            const y = (v * canvas.height) / 2;

            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                const previousX = x - sliceWidth;
                const previousY = (dataArray[i - 1] / 128.0 * canvas.height) / 2;
                ctx.bezierCurveTo(previousX + sliceWidth / 2, previousY, x - sliceWidth / 2, y, x, y);
            }

            x += sliceWidth;
        }

        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
    };

    draw();
}

async function transcribeAudio(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);

    const response = await fetch('https://api.example.com/transcribe', {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        const transcription = await response.text();
        transcriptionElement.innerText = transcription;
    } else {
        transcriptionElement.innerText = 'Error transcribing audio.';
    }
}
