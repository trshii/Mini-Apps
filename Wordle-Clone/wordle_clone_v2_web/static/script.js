async function submitGuess() {
    const input = document.getElementById('guess-input');
    const guess = input.value.toLowerCase();
    
    if (guess.length !== 5) {
        alert('Word must be 5 letters long!');
        return;
    }

    // Send guess to Python (Flask)
    const response = await fetch('/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ guess: guess })
    });

    const data = await response.json();
    updateBoard(guess, data.verdict);

    if (data.is_game_over){
        if (data.won){
            alert("You win!")
        } else {
            alert(`You lost! The word was: ${data.target}`)
        }
        input.disabled = true
    }

    input.value = ''; // Clear input
}

let currentRow = 0;

function updateBoard(guess, verdict) {
    const row = document.getElementById(`row-${currentRow}`);
    const tiles = row.getElementsByClassName('tile')

    for (let i = 0; i < 5; i++) {
        const tile = tiles[i]
        tile.innerText = guess[i]
        tile.classList.add(verdict[i])
    }

    currentRow++;
}