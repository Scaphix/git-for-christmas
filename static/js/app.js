const API_BASE_URL = '/api';

// --- Global UI Elements ---
const statusMessage = document.getElementById('statusMessage');
const playerListUl = document.getElementById('players-ul');
const playerIdInput = document.getElementById('player-id');
const playerNameInput = document.getElementById('player-name');
const lookupIdInput = document.getElementById('lookup-id');
const giverDisplay = document.getElementById('giver-display');
const recipientDisplay = document.getElementById('recipient-display');
const playerListContainer = document.getElementById('playerList');


// --- Utility Functions ---

/** Handles common API fetching, error checks, and JSON parsing. */
async function apiCall(endpoint, method = 'GET', data = null) {
    const config = {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: data ? JSON.stringify(data) : null,
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const result = await response.json();

        if (response.ok) {
            return { success: true, data: result };
        } else {
            // Server returned a known error (e.g., 400 Bad Request)
            return { success: false, error: result.error || result.message || 'Unknown API Error' };
        }
    } catch (error) {
        // Network error (e.g., server unreachable)
        return { success: false, error: `Network Error: ${error.message}` };
    }
}

/** Displays a status or error message on the UI. */
function displayMessage(message, isError = false) {
    if (!statusMessage) return;
    statusMessage.textContent = message;
    statusMessage.classList.remove('hidden', 'bg-red-500/10', 'text-red-700', 'bg-green-500/10', 'text-green-700');
    
    statusMessage.classList.add(isError ? 'bg-red-500/10 text-red-700' : 'bg-green-500/10 text-green-700');
    
    setTimeout(() => statusMessage.classList.add('hidden'), 5000);
}


// --- Main Application Logic ---

async function registerPlayer() {
    const userId = playerIdInput?.value.trim();
    const name = playerNameInput?.value.trim();

    if (!userId || !name) {
        return displayMessage('Please enter both a Unique Player ID and a Display Name.', true);
    }

    const result = await apiCall('/register/', 'POST', { user_id: userId, name: name });

    if (result.success) {
        displayMessage(result.data.message, false);
        playerIdInput.value = '';
        playerNameInput.value = '';
        fetchPlayers();
    } else {
        displayMessage(`Registration Error: ${result.error}`, true);
    }
}

async function fetchPlayers() {
    if (!playerListUl) return;

    const result = await apiCall('/players/');

    if (result.success) {
        const players = result.data.players || [];
        
        // Update the count display
        const countElement = playerListContainer?.querySelector('p:not(.text-sm)');
        if (countElement) countElement.textContent = `Registered Players: ${players.length}`;
        
        // Update the list content
        if (players.length > 0) {
            playerListUl.innerHTML = players.map(p => 
                `<li class="p-2 border-b border-gray-200 last:border-b-0"><span class="font-bold text-gray-800">${p.name}</span> <span class="text-xs text-gray-500">(ID: ${p.user_id})</span></li>`
            ).join('');
        } else {
            playerListUl.innerHTML = '<li class="p-2 text-gray-500">No players registered yet.</li>';
        }

    } else {
        displayMessage(`Failed to fetch players: ${result.error}`, true);
    }
}

async function runMatching() {
    // replace confirm() with a custom modal UI
    if (!confirm("Are you sure you want to run the Secret Santa Match? This will reset all existing matches.")) {
        return;
    }

    displayMessage('Running matching algorithm...', false);
    const result = await apiCall('/run/', 'POST');

    if (result.success) {
        displayMessage(result.data.message, false);
    } else {
        displayMessage(`Matching Error: ${result.error}`, true);
    }
}

async function lookupMatch() {
    if (!lookupIdInput || !giverDisplay || !recipientDisplay) return;

    const userId = lookupIdInput.value.trim();
    
    giverDisplay.textContent = 'Looking up match...';
    recipientDisplay.textContent = '...';

    if (!userId) {
        giverDisplay.textContent = 'Please enter your Unique Player ID.';
        return;
    }

    const result = await apiCall(`/lookup/?user_id=${userId}`);

    if (result.success) {
        giverDisplay.textContent = `Hello, ${result.data.giver_name}!`;
        recipientDisplay.textContent = `🎁 Your Secret Recipient is: ${result.data.recipient_name}!`;
        displayMessage('Match successfully revealed!', false);
    } else {
        giverDisplay.textContent = `Error finding match for ID: ${userId}`;
        recipientDisplay.textContent = result.error;
        displayMessage(`Lookup Failed: ${result.error}`, true);
    }
}


// --- Initialization ---

window.onload = () => {
    if (statusMessage) statusMessage.classList.add('hidden'); 
    if (playerListUl) fetchPlayers();
};