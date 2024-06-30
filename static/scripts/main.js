async function addGroup() {
    const groupId = document.getElementById('groupIdInput').value;
    if (!groupId) return;

    const response = await fetch('/groups', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ group_id: groupId }),
    });

    if (response.ok) {
        alert('Group ID added successfully!');
        loadGroups();
    } else {
        alert('Failed to add Group ID.');
    }
}

async function loadGroups() {
    const response = await fetch('/groups');
    const groups = await response.json();

    const groupList = document.getElementById('groupList');
    const groupSelect = document.getElementById('groupSelect');

    groupList.innerHTML = '';
    groupSelect.innerHTML = '';

    groups.forEach(group => {
        const listItem = document.createElement('li');
        listItem.textContent = group.group_id;
        groupList.appendChild(listItem);

        const optionItem = document.createElement('option');
        optionItem.value = group.group_id;
        optionItem.textContent = group.group_id;
        groupSelect.appendChild(optionItem);
    });
}

async function sendMessage() {
    const groupId = document.getElementById('groupSelect').value;
    const message = document.getElementById('messageInput').value;
    if (!groupId || !message) return;

    const response = await fetch('/zap', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ group_id: groupId, message: message }),
    });

    if (response.ok) {
        alert('Message sent successfully!');
    } else {
        alert('Failed to send message.');
    }
}

async function sendMessageToAll() {
    const message = document.getElementById('messageInput').value;
    if (!message) return;

    const response = await fetch('/zap_all', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });

    if (response.ok) {
        const data = await response.json();
        updateLog(data.log);
        updateProgress(data.progress);
    } else {
        alert('Failed to send message to all groups.');
    }
}

function updateProgress(value) {
    const progressBar = document.getElementById('progressBar');
    progressBar.value = value;
}

function updateLog(logs) {
    const logContainer = document.getElementById('log');
    logContainer.innerHTML = logs.join('<br>');
}

document.addEventListener('DOMContentLoaded', loadGroups);
