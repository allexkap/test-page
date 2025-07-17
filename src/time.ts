// src/time.ts

function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const el = document.getElementById('output');
    if (el) {
        el.textContent = timeString;
    }
}

setInterval(updateTime, 1000);
window.onload = updateTime;
