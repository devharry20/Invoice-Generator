const changingTextElement = document.getElementById('changing-text');

const phrases = ['highly customisable', 'hassle free', 'easily saveable'];

let currentIndex = 0;

function changeText() {
    changingTextElement.textContent = phrases[currentIndex];

    currentIndex = (currentIndex + 1) % phrases.length;
}

setInterval(changeText, 2000);