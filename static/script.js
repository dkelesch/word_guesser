document.addEventListener('DOMContentLoaded', () => {
    const wordDisplay = document.getElementById('word-display');
    const revealLetterBtn = document.getElementById('reveal-letter-btn');
    const revealWordBtn = document.getElementById('reveal-word-btn');
    const nextWordBtn = document.getElementById('next-word-btn');
    const messageArea = document.getElementById('message-area');

    // Function to update the word display (slots)
    function updateWordDisplay(slots) {
        wordDisplay.innerHTML = ''; // Clear previous slots
        if (slots && slots.length > 0) {
            slots.forEach(letter => {
                const slotElement = document.createElement('span');
                slotElement.className = 'letter-slot';
                slotElement.textContent = letter;
                wordDisplay.appendChild(slotElement);
            });
        } else {
            wordDisplay.textContent = "Game Over or No Word Loaded";
        }
        checkGameButtons(slots);
    }

    // Function to enable/disable buttons based on game state
    function checkGameButtons(slots) {
        const isWordFullyRevealed = slots && slots.every(letter => letter !== '_');
        const noWordLoaded = !slots || slots.length === 0;

        revealLetterBtn.disabled = isWordFullyRevealed || noWordLoaded;
        revealWordBtn.disabled = isWordFullyRevealed || noWordLoaded;
        // Next word button is always enabled unless an explicit "game over" state is implemented
    }

    // Function to display messages
    function showMessage(message, isError = false) {
        messageArea.textContent = message;
        messageArea.style.color = isError ? 'red' : 'green';
        setTimeout(() => messageArea.textContent = '', 3000); // Clear message after 3 seconds
    }

    // Fetch initial word state
    async function loadInitialWord() {
        try {
            const response = await fetch('/get_current_word_state', { method: 'GET' });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            updateWordDisplay(data.slots);
            if (data.message) showMessage(data.message);
        } catch (error) {
            console.error('Error loading initial word:', error);
            showMessage('Could not load game. Please try refreshing.', true);
            updateWordDisplay([]); // Show no word loaded
        }
    }

    // Event Listeners
    revealLetterBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/reveal_letter', { method: 'POST' });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            updateWordDisplay(data.slots);
            if (data.message) showMessage(data.message);
        } catch (error) {
            console.error('Error revealing letter:', error);
            showMessage('Error revealing letter.', true);
        }
    });

    revealWordBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/reveal_word', { method: 'POST' });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            updateWordDisplay(data.slots);
             if (data.message) showMessage(data.message);
        } catch (error) {
            console.error('Error revealing word:', error);
            showMessage('Error revealing word.', true);
        }
    });

    nextWordBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/next_word', { method: 'POST' });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            updateWordDisplay(data.slots);
            if (data.message) showMessage(data.message);
            else showMessage(''); // Clear any previous message
        } catch (error) {
            console.error('Error getting next word:', error);
            showMessage('Error getting next word.', true);
        }
    });

    // Load the first word when the page loads
    loadInitialWord();
});