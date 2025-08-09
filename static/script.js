document.addEventListener('DOMContentLoaded', () => {
    const wordDisplay = document.getElementById('word-display');
    const definitionDisplay = document.getElementById('definition-display'); // Get the new element
    const revealLetterBtn = document.getElementById('reveal-letter-btn');
    const revealWordBtn = document.getElementById('reveal-word-btn');
    const nextWordBtn = document.getElementById('next-word-btn');
    const messageArea = document.getElementById('message-area');

    // --- Main UI Update Function ---
    // A single function to update all parts of the UI from the server response
    function updateUI(data) {
        if (data.slots) {
            updateWordDisplay(data.slots);
            checkGameButtons(data.slots);
        }
        if (data.definition) {
            updateDefinitionDisplay(data.definition);
        }
        if (data.message) {
            showMessage(data.message);
        }
    }

    // Function to update the word display (slots)
    function updateWordDisplay(slots) {
        wordDisplay.innerHTML = ''; // Clear previous slots
        if (slots && slots.length > 0) {
            slots.forEach((letter, index) => {
                const slotElement = document.createElement('span');
                slotElement.className = 'letter-slot';
                slotElement.textContent = letter;
                wordDisplay.appendChild(slotElement);
            
                // Add click-to-reveal functionality only for unrevealed letters
                if (letter === '_') {
                    slotElement.style.cursor = 'pointer'; // Indicate it's clickable
                    slotElement.addEventListener('click', () => revealSpecificLetter(index));
                }
            });
        } else {
            wordDisplay.textContent = "Game Over or No Word Loaded";
        }
    }
    
    // Function to update the definition display
    function updateDefinitionDisplay(definition) {
        definitionDisplay.textContent = definition;
    }

    // Function to enable/disable buttons based on game state
    function checkGameButtons(slots) {
        const isWordFullyRevealed = slots && slots.every(letter => letter !== '_');
        const noWordLoaded = !slots || slots.length === 0;

        revealLetterBtn.disabled = isWordFullyRevealed || noWordLoaded;
        revealWordBtn.disabled = isWordFullyRevealed || noWordLoaded;
    }

    // Function to display messages
    function showMessage(message, isError = false) {
        messageArea.textContent = message;
        messageArea.style.color = isError ? 'red' : 'green';
        setTimeout(() => messageArea.textContent = '', 4000); // Clear message after 4 seconds
    }

    // --- API Call Functions ---

    // Function to reveal a specific letter by index
    async function revealSpecificLetter(index) {
        try {
            const response = await fetch('/reveal_letter_at_index', {
                method: 'POST',
                body: JSON.stringify({ index: index }),
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            updateUI(data); // Use the main UI updater
        } catch (error) {
            console.error('Error revealing specific letter:', error);
            showMessage('Error revealing letter.', true);
        }
    }

    // Fetch initial word state
    async function loadInitialWord() {
        try {
            const response = await fetch('/get_current_word_state', { method: 'GET' });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            updateUI(data); // Use the main UI updater
        } catch (error) {
            console.error('Error loading initial word:', error);
            showMessage('Could not load game. Please try refreshing.', true);
            updateWordDisplay([]); // Show no word loaded
        }
    }

    // Generic fetch handler for button clicks
    async function handleButtonClick(endpoint) {
        try {
            const response = await fetch(endpoint, { method: 'POST' });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            updateUI(data); // Use the main UI updater
        } catch (error) {
            console.error(`Error with endpoint ${endpoint}:`, error);
            showMessage('An error occurred.', true);
        }
    }

    // Event Listeners
    revealLetterBtn.addEventListener('click', () => handleButtonClick('/reveal_letter'));
    revealWordBtn.addEventListener('click', () => handleButtonClick('/reveal_word'));
    nextWordBtn.addEventListener('click', () => {
        // Clear definition immediately on "Next Word"
        updateDefinitionDisplay("Yeni kelime yükleniyor...");
        handleButtonClick('/next_word');
    });

    // Load the first word when the page loads
    loadInitialWord();
});
