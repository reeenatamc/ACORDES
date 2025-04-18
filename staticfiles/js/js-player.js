const audio = document.getElementById('audioPlayer');
  const toggleBtn = document.getElementById('togglePlayBtn');
  const toggleIcon = document.getElementById('toggleIcon');
  const progressBar = document.getElementById('progressBar');
  const currentTime = document.getElementById('currentTime');
  const duration = document.getElementById('duration');

  function formatTime(seconds) {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${min}:${sec}`;
  }

  toggleBtn.addEventListener('click', () => {
    if (audio.paused) {
      audio.play();
      toggleIcon.classList.remove("bi-play-fill");
      toggleIcon.classList.add("bi-pause-fill");
    } else {
      audio.pause();
      toggleIcon.classList.remove("bi-pause-fill");
      toggleIcon.classList.add("bi-play-fill");
    }
  });

  audio.addEventListener('loadedmetadata', () => {
    duration.textContent = formatTime(audio.duration);
  });

  audio.addEventListener('timeupdate', () => {
    const percent = (audio.currentTime / audio.duration) * 100;
    progressBar.style.width = `${percent}%`;
    currentTime.textContent = formatTime(audio.currentTime);
  });

  audio.addEventListener("ended", () => {
    toggleIcon.classList.remove("bi-pause-fill");
    toggleIcon.classList.add("bi-play-fill");
  });