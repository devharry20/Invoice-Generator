const changingTextElement = document.getElementById('changing-text');

const phrases = ['highly customisable', 'hassle free', 'easily saveable'];

let currentIndex = 0;

function changeText() {
    changingTextElement.textContent = phrases[currentIndex];

    currentIndex = (currentIndex + 1) % phrases.length;
}

function addRow() {
    const table = document.getElementById("invoice-items").getElementsByTagName("tbody")[0];
    const newRow = table.insertRow();
    newRow.innerHTML = `
      <td><input type="text" name="description[]" required></td>
      <td><input type="number" name="quantity[]" min="1" required></td>
      <td><input type="number" name="unit_price[]" step="0.01" required></td>
    `;
}

setInterval(changeText, 2000);