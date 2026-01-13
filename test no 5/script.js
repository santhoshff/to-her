let scene, camera, renderer, particles;
let count = 20000;
let currentState = 'sphere'; // 'sphere', 'morphing', 'text'
let time = 0;

// Speech
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let isListening = false;

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

    const container = document.getElementById('container');
    // Clear any existing canvas in container (user's HTML had a canvas inside id=container, THREE adds its own)
    container.innerHTML = '';
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    camera.position.z = 30;

    createParticles();
    setupEventListeners();
    setupVoice();

    animate();
    updateStatus('Ready');
}

function createParticles() {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const currentPositions = new Float32Array(count * 3);

    const color1 = new THREE.Color(0x64ffda);
    const color2 = new THREE.Color(0x0a192f);

    for (let i = 0; i < count; i++) {
        const phi = Math.acos(-1 + (2 * i) / count);
        const theta = Math.sqrt(count * Math.PI) * phi;
        const r = 10;

        const x = r * Math.sin(phi) * Math.cos(theta);
        const y = r * Math.sin(phi) * Math.sin(theta);
        const z = r * Math.cos(phi);

        positions[i * 3] = x;
        positions[i * 3 + 1] = y;
        positions[i * 3 + 2] = z;

        currentPositions[i * 3] = x;
        currentPositions[i * 3 + 1] = y;
        currentPositions[i * 3 + 2] = z;

        const mixedColor = color1.clone().lerp(color2, Math.random());
        colors[i * 3] = mixedColor.r;
        colors[i * 3 + 1] = mixedColor.g;
        colors[i * 3 + 2] = mixedColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(currentPositions, 3));
    geometry.setAttribute('targetPosition', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.userData = { spherePositions: positions.slice() };

    const material = new THREE.PointsMaterial({
        size: 0.15,
        vertexColors: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        transparent: true,
        opacity: 0.8
    });

    particles = new THREE.Points(geometry, material);
    scene.add(particles);
}

function getTextCoordinates(text) {
    const canvas = document.getElementById('textCanvas');
    if (!canvas) return []; // Safety check
    const ctx = canvas.getContext('2d');

    const fontSize = 120; // Larger font
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = `900 ${fontSize}px 'Inter', sans-serif`;
    ctx.fillStyle = 'white';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, canvas.width / 2, canvas.height / 2);

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    const coords = [];
    const step = 4;

    for (let y = 0; y < canvas.height; y += step) {
        for (let x = 0; x < canvas.width; x += step) {
            if (data[(y * canvas.width + x) * 4 + 3] > 128) {
                const posX = (x - canvas.width / 2) * 0.05;
                const posY = -(y - canvas.height / 2) * 0.05;
                coords.push({ x: posX, y: posY, z: 0 });
            }
        }
    }
    return coords;
}

function morphToText(text) {
    if (currentState === 'morphing') return;
    currentState = 'morphing';
    updateStatus(`Morphing to "${text}"`);

    const textCoords = getTextCoordinates(text);
    const geometry = particles.geometry;
    const attributes = geometry.attributes;

    for (let i = 0; i < count; i++) {
        let tx, ty, tz;
        if (i < textCoords.length) {
            tx = textCoords[i].x;
            ty = textCoords[i].y;
            tz = 0;
        } else {
            // Hide extras
            tx = (Math.random() - 0.5) * 60;
            ty = (Math.random() - 0.5) * 60;
            tz = (Math.random() - 0.5) * 60;
        }

        attributes.targetPosition.array[i * 3] = tx;
        attributes.targetPosition.array[i * 3 + 1] = ty;
        attributes.targetPosition.array[i * 3 + 2] = tz;
    }

    attributes.targetPosition.needsUpdate = true;
    currentState = 'text';

    if (window.gsap) {
        gsap.to(camera.position, { z: 20, duration: 1.5, ease: "power2.out" });
    }
}

function morphToSphere() {
    currentState = 'sphere';
    updateStatus('Active');

    const geometry = particles.geometry;
    const spherePos = geometry.userData.spherePositions;

    for (let i = 0; i < count; i++) {
        geometry.attributes.targetPosition.array[i * 3] = spherePos[i * 3];
        geometry.attributes.targetPosition.array[i * 3 + 1] = spherePos[i * 3 + 1];
        geometry.attributes.targetPosition.array[i * 3 + 2] = spherePos[i * 3 + 2];
    }
    geometry.attributes.targetPosition.needsUpdate = true;

    if (window.gsap) {
        gsap.to(camera.position, { z: 30, duration: 1.5, ease: "power2.out" });
    }
}

function animate() {
    requestAnimationFrame(animate);
    time += 0.01;

    const positions = particles.geometry.attributes.position.array;
    const targets = particles.geometry.attributes.targetPosition.array;
    const speed = 0.08; // Faster snap

    for (let i = 0; i < count; i++) {
        const px = positions[i * 3];
        const py = positions[i * 3 + 1];
        const pz = positions[i * 3 + 2];

        const tx = targets[i * 3];
        const ty = targets[i * 3 + 1];
        const tz = targets[i * 3 + 2]; // Fixed: was using index 2 again in prev code maybe? Checked: it was correct before.

        positions[i * 3] += (tx - px) * speed;
        positions[i * 3 + 1] += (ty - py) * speed;
        positions[i * 3 + 2] += (tz - pz) * speed;

        // Text Jitter
        if (currentState === 'text' && i < positions.length / 3) {
            positions[i * 3] += (Math.random() - 0.5) * 0.02;
            positions[i * 3 + 1] += (Math.random() - 0.5) * 0.02;
        }
    }

    if (currentState === 'sphere') {
        particles.rotation.y = time * 0.1;
        particles.rotation.z = Math.sin(time * 0.2) * 0.1;
    } else {
        particles.rotation.y = Math.sin(time * 0.5) * 0.05;
        particles.rotation.z = 0;
    }

    particles.geometry.attributes.position.needsUpdate = true;
    renderer.render(scene, camera);
}

// Interactions
function setupEventListeners() {
    window.addEventListener('resize', onWindowResize);

    const btn = document.getElementById('typeBtn');
    if (btn) btn.addEventListener('click', handleInput);

    const input = document.getElementById('morphText');
    if (input) input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleInput();
    });

    const mic = document.getElementById('micBtn');
    if (mic) mic.addEventListener('click', toggleListening);
}

async function handleInput() {
    const input = document.getElementById('morphText');
    const text = input.value.trim();
    if (text) {
        morphToSphere(); // Reset visual
        updateStatus("Sending...");

        console.log("Attempting to fetch http://localhost:5000/chat with:", text);

        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            console.log("Response Status:", response.status);

            if (!response.ok) {
                throw new Error(`Server Error: ${response.status}`);
            }

            const data = await response.json();
            console.log("Server Data:", data);

            if (data.reply) {
                updateStatus("Answering");
                speak(data.reply);
            } else {
                updateStatus("No Reply Data");
            }
        } catch (e) {
            console.error("Fetch Error:", e);
            updateStatus(`Err: ${e.message}`); // Show error on screen
            morphToText("Error");
        }

        input.value = '';
    }
}

async function speak(text) {
    updateStatus("Speaking...");
    currentState = 'text'; // Visual: Text State

    try {
        const response = await fetch('http://localhost:5000/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        if (response.ok) {
            const blob = await response.blob();
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);

            audio.onended = () => {
                currentState = 'sphere';
                updateStatus("Listening...");
                // Loop: Auto-listen after answering
                try {
                    recognition.start();
                    document.getElementById('micBtn').classList.add('active');
                } catch (e) { }
            };

            // Handle Interaction Policy often blocking auto-play
            await audio.play().catch(e => {
                console.warn("Autoplay blocked, user interaction needed", e);
                updateStatus("Click Anywhere");
                document.body.addEventListener('click', () => audio.play(), { once: true });
            });

            // Visuals
            const firstWord = text.split(' ')[0].replace(/[^a-zA-Z]/g, '');
            if (firstWord) morphToText(firstWord.substring(0, 5));
        } else {
            browserSpeak(text);
        }
    } catch (e) {
        console.error("TTS Error", e);
        browserSpeak(text);
    }
}

function browserSpeak(text) {
    const synth = window.speechSynthesis;

    // Function to actually speak so we can wait for voices
    const speakNow = () => {
        const utterThis = new SpeechSynthesisUtterance(text);
        const voices = synth.getVoices();

        console.log("Available Voices:", voices.map(v => v.name)); // Debug

        // 1. Target "Zira" (Standard Windows Female)
        let target = voices.find(v => v.name.includes("Zira"));

        // 2. Target "Google US English" (Chrome Female-ish)
        if (!target) target = voices.find(v => v.name.includes("Google US English"));

        // 3. Target any "Female" label
        if (!target) target = voices.find(v => v.name.toLowerCase().includes("female"));

        // 4. Exclude "David" / "Mark" (common male names)
        if (!target) {
            target = voices.find(v =>
                !v.name.includes("David") &&
                !v.name.includes("Mark") &&
                !v.name.includes("Male") &&
                v.lang.startsWith("en")
            );
        }

        if (target) {
            console.log("Selected Voice:", target.name);
            utterThis.voice = target;
            // Slight pitch raise for femininity
            utterThis.pitch = 1.2;
        } else {
            console.warn("No specific female voice found, forcing high pitch.");
            // Force high pitch on whatever default exists (likely male) to mask it
            utterThis.pitch = 1.6;
        }

        utterThis.rate = 1.0;
        currentState = 'text';

        utterThis.onend = () => {
            currentState = 'sphere';
            updateStatus("Listening...");
            try {
                recognition.start();
                document.getElementById('micBtn').classList.add('active');
            } catch (e) { }
        };

        morphToText("EVA");
        synth.speak(utterThis);
    };

    // Ensure voices are loaded
    if (synth.getVoices().length === 0) {
        synth.onvoiceschanged = speakNow;
    } else {
        speakNow();
    }
}

function setupVoice() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.trim();
            document.getElementById('morphText').value = transcript;
            handleInput();
        };

        recognition.onend = () => {
            document.getElementById('micBtn').classList.remove('active');
            isListening = false;
        };
    }
}

function toggleListening() {
    if (!recognition) return;
    if (isListening) {
        recognition.stop();
    } else {
        isListening = true;
        recognition.start();
        document.getElementById('micBtn').classList.add('active');
        updateStatus("Listening...");
    }
}

function updateStatus(text) {
    const el = document.getElementById('statusText');
    if (el) el.textContent = text;
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

init();
