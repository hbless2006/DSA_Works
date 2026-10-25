document.addEventListener("DOMContentLoaded", () => {
    const audio = document.getElementById("ambientAudio");
    const player = document.querySelector(".music-player");
    const toggle = document.getElementById("musicToggle");
    const previous = document.getElementById("musicPrevious");
    const next = document.getElementById("musicNext");
    const volume = document.getElementById("musicVolume");
    const progress = document.getElementById("musicProgress");
    const title = document.getElementById("musicTitle");
    const status = document.getElementById("musicStatus");
    const currentTime = document.getElementById("musicCurrentTime");
    const duration = document.getElementById("musicDuration");
    const tracks = Array.from(document.querySelectorAll("#musicTracks [data-file]"))
        .map((item) => ({
            title: item.dataset.title,
            file: item.dataset.file
        }));

    let currentTrack = 0;
    let pendingRestore = null;
    const storageKey = "portfolioMusicPlayer";
    let savedState = null;
    try {
        savedState = JSON.parse(sessionStorage.getItem(storageKey) || "null");
    } catch (error) {
        savedState = null;
    }
    if (savedState && Number.isFinite(savedState.volume)) {
        volume.value = savedState.volume;
    }
    audio.volume = Number(volume.value);

    function savePlayerState() {
        sessionStorage.setItem(storageKey, JSON.stringify({
            track: currentTrack,
            time: pendingRestore
                ? pendingRestore.time
                : (Number.isFinite(audio.currentTime) ? audio.currentTime : 0),
            playing: pendingRestore ? pendingRestore.playing : !audio.paused,
            volume: audio.volume
        }));
    }

    function formatTime(seconds) {
        if (!Number.isFinite(seconds)) return "0:00";
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60).toString().padStart(2, "0");
        return `${minutes}:${remainingSeconds}`;
    }

    function setTrack(index, autoplay = false, startTime = 0) {
        currentTrack = (index + tracks.length) % tracks.length;
        const track = tracks[currentTrack];
        pendingRestore = { time: startTime, playing: autoplay };
        audio.src = "/static/music/" + encodeURIComponent(track.file);
        title.textContent = track.title;
        currentTime.textContent = "0:00";
        duration.textContent = "0:00";
        progress.value = 0;
        status.textContent = autoplay ? "Playing" : "Ready to play";
        audio.load();
    }

    toggle.addEventListener("click", async () => {
        if (audio.paused) {
            try {
                await audio.play();
            } catch (error) {
                status.textContent = "Unable to play this track";
            }
        } else {
            audio.pause();
        }
    });

    previous.addEventListener("click", () => setTrack(currentTrack - 1, !audio.paused));
    next.addEventListener("click", () => setTrack(currentTrack + 1, !audio.paused));

    volume.addEventListener("input", () => {
        audio.volume = Number(volume.value);
        savePlayerState();
    });

    progress.addEventListener("input", () => {
        if (Number.isFinite(audio.duration)) {
            audio.currentTime = (Number(progress.value) / 100) * audio.duration;
            savePlayerState();
        }
    });

    audio.addEventListener("play", () => {
        player.classList.add("is-playing");
        toggle.setAttribute("aria-label", "Pause music");
        status.textContent = "Playing";
        savePlayerState();
    });

    audio.addEventListener("pause", () => {
        player.classList.remove("is-playing");
        toggle.setAttribute("aria-label", "Play music");
        if (audio.currentSrc) status.textContent = "Paused";
        savePlayerState();
    });

    audio.addEventListener("loadedmetadata", () => {
        duration.textContent = formatTime(audio.duration);
        if (pendingRestore) {
            const restore = pendingRestore;
            pendingRestore = null;
            audio.currentTime = Math.min(restore.time, audio.duration || restore.time);
            currentTime.textContent = formatTime(audio.currentTime);
            if (Number.isFinite(audio.duration) && audio.duration > 0) {
                progress.value = (audio.currentTime / audio.duration) * 100;
            }

            if (restore.playing) {
                audio.play().catch(() => {
                    status.textContent = "Tap play to continue";
                    savePlayerState();
                });
            } else {
                status.textContent = "Paused";
                savePlayerState();
            }
        }
    });

    audio.addEventListener("timeupdate", () => {
        currentTime.textContent = formatTime(audio.currentTime);
        if (Number.isFinite(audio.duration) && audio.duration > 0) {
            progress.value = (audio.currentTime / audio.duration) * 100;
        }
        savePlayerState();
    });

    audio.addEventListener("ended", () => setTrack(currentTrack + 1, true));

    window.addEventListener("pagehide", savePlayerState);
    const savedTrack = savedState && Number.isInteger(savedState.track)
        ? savedState.track
        : 0;
    const savedTime = savedState && Number.isFinite(savedState.time)
        ? savedState.time
        : 0;
    setTrack(savedTrack, Boolean(savedState && savedState.playing), savedTime);

    const background = document.querySelector(".dream-background");
    if (background) {
        for (let i = 0; i < 16; i++) {
            const sparkle = document.createElement("span");
            sparkle.className = "generated-sparkle";
            sparkle.textContent = i % 2 === 0 ? "✧" : "·";
            sparkle.style.left = Math.random() * 100 + "%";
            sparkle.style.animationDelay = Math.random() * 12 + "s";
            sparkle.style.animationDuration = (8 + Math.random() * 10) + "s";
            sparkle.style.fontSize = (10 + Math.random() * 14) + "px";
            background.appendChild(sparkle);
        }
    }
});
