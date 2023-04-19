document.addEventListener('DOMContentLoaded', () => {
  const arrivalTime = document.querySelector('#arrival_time');

  setInterval(() => {
    fetch('/time')
      .then(response => response.json())
      .then(data => {
        const { minutes1, seconds1 } = data;
        arrivalTime.textContent = `${minutes1}분 ${seconds1}초`;
      });
  }, 1000);
});
