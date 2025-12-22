const video = document.getElementById('webcam');
const canvas = document.getElementById('captureCanvas');
const ctx = canvas.getContext('2d');
const detectBtn = document.getElementById('detectBtn');
const autoBtn = document.getElementById('autoBtn');
const startCameraBtn = document.getElementById('startCameraBtn');
const cameraPrompt = document.getElementById('cameraPrompt');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const resultArea = document.getElementById('resultArea');
const confList = document.getElementById('confList');
const scanFrame = document.getElementById('scanFrame');
const capturedArea = document.getElementById('capturedArea');

let stream = null;
let autoInterval = null;
let isAuto = false;

// Start Camera
startCameraBtn.addEventListener('click', startCamera);

async function startCamera() {
    startCameraBtn.disabled = true;
    startCameraBtn.innerHTML = '<span class="spinner"></span> Starting...';

    try {
        // Try different camera configs
        const configs = [
            { video: { facingMode: { exact: 'environment' }, width: 640, height: 480 } },
            { video: { facingMode: 'user', width: 640, height: 480 } },
            { video: true }
        ];

        for (const config of configs) {
            try {
                stream = await navigator.mediaDevices.getUserMedia(config);
                break;
            } catch (e) {
                continue;
            }
        }

        if (!stream) throw new Error('No camera access');

        video.srcObject = stream;
        await video.play();

        cameraPrompt.classList.add('hidden');
        detectBtn.disabled = false;
        setStatus('Camera ready! Show a katakana character', 'ok');

    } catch (err) {
        console.error('Camera error:', err);
        startCameraBtn.disabled = false;
        startCameraBtn.innerHTML = '🎥 Try Again';

        if (err.name === 'NotAllowedError') {
            setStatus('Camera blocked. Allow in browser settings.', 'error');
        } else if (err.name === 'NotFoundError') {
            setStatus('No camera found on device.', 'error');
        } else {
            setStatus('Camera error: ' + err.message, 'error');
        }
    }
}

// Detect
detectBtn.addEventListener('click', detect);

// Auto toggle
autoBtn.addEventListener('click', () => {
    if (isAuto) stopAuto();
    else startAuto();
});

function startAuto() {
    if (!stream) {
        setStatus('Start camera first!', 'warning');
        return;
    }
    isAuto = true;
    autoBtn.classList.add('active');
    autoBtn.textContent = '⏹ Stop';
    scanFrame.classList.add('active');
    autoInterval = setInterval(detect, 1200);
    setStatus('Auto-detecting...', 'ok');
}

function stopAuto() {
    isAuto = false;
    autoBtn.classList.remove('active');
    autoBtn.textContent = '🔄 Auto';
    scanFrame.classList.remove('active');
    clearInterval(autoInterval);
    setStatus('Auto stopped', 'ok');
}

async function detect() {
    if (!stream) {
        setStatus('Start camera first!', 'warning');
        return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL('image/png');

    try {
        detectBtn.disabled = true;
        detectBtn.innerHTML = '<span class="spinner"></span>';

        const res = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        });

        const data = await res.json();

        if (data.success) {
            // Display both captured and preprocessed images
            capturedArea.innerHTML = `
                <div style="display:flex; gap:clamp(10px, 3vw, 20px); justify-content:center; flex-wrap:wrap; align-items:center; padding:10px;">
                    <div style="text-align:center; flex:1; min-width:100px; max-width:180px;">
                        <div style="opacity:0.7; font-size:clamp(0.7em, 2.5vw, 0.85em); margin-bottom:8px;">📷 Captured</div>
                        <img src="${imageData}" alt="Captured" style="width:100%; max-width:150px; aspect-ratio:1; object-fit:contain; border-radius:12px; border:2px solid rgba(88,204,2,0.3); background:#1a1a1a;">
                    </div>
                    <div style="font-size:clamp(16px, 4vw, 24px); opacity:0.5; display:none;">→</div>
                    <div style="text-align:center; flex:1; min-width:100px; max-width:180px;">
                        <div style="opacity:0.7; font-size:clamp(0.7em, 2.5vw, 0.85em); margin-bottom:8px;">🔬 Preprocessed</div>
                        <img src="${data.preprocessed_image}" alt="Preprocessed" style="width:100%; max-width:150px; aspect-ratio:1; image-rendering:pixelated; border-radius:12px; border:2px solid rgba(28,176,246,0.5); background:#1a1a1a;">
                    </div>
                </div>
            `;
            showResult(data);
            setStatus(`Detected: ${data.top_prediction.kana} (${data.top_prediction.romaji})`, 'ok');
        } else {
            setStatus('Error: ' + data.error, 'error');
        }
    } catch (err) {
        setStatus('Server connection failed', 'error');
    } finally {
        detectBtn.disabled = false;
        detectBtn.innerHTML = '⚡ Detect';
    }
}

function showResult(data) {
    const top = data.top_prediction;

    resultArea.innerHTML = `
        <div class="result-show">
            <div class="result-kana">${top.kana}</div>
            <div class="result-romaji">${top.romaji}</div>
            <div class="result-confidence">${top.confidence.toFixed(1)}% confident</div>
        </div>
    `;

    confList.classList.remove('hidden');
    confList.innerHTML = data.predictions.map((p, i) => `
        <div class="conf-item ${i === 0 ? 'top' : ''}">
            <span class="conf-kana">${p.kana}</span>
            <div class="conf-info">
                <div class="conf-name">${p.romaji}</div>
                <div class="conf-bar">
                    <div class="conf-fill" style="width:${p.confidence}%"></div>
                </div>
            </div>
            <span class="conf-percent">${p.confidence.toFixed(1)}%</span>
        </div>
    `).join('');
}

function setStatus(msg, type) {
    statusText.textContent = msg;
    statusDot.className = 'status-dot';
    if (type === 'error') statusDot.classList.add('error');
    if (type === 'warning') statusDot.classList.add('warning');
}

// Health check
fetch('/health')
    .then(r => r.json())
    .then(d => console.log('Server healthy:', d))
    .catch(() => setStatus('Server not responding', 'error'));

// Auto-start if permissions already granted
if (location.hostname === '127.0.0.1') {
    navigator.permissions?.query({ name: 'camera' })
        .then(r => { if (r.state === 'granted') startCamera(); })
        .catch(() => {});
}
