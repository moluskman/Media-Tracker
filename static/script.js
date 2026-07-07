async function searchDatabase() {
    const query = document.getElementById('search-form').querySelector('input[type="search"]').value;

    const response = await fetch(`/api/search?q=${query}`);
    const dataObj = await response.json();

    displayResults(dataObj);
    console.log(dataObj.results);
}
async function addMediaToDatabase() {
    const newTitle = document.getElementById('media-title').value;
    const newType = document.getElementById('media-type').value;

    if (!newTitle.trim() || !newType.trim()) return;
    const response = await fetch('/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: newTitle,
            type: newType
        })
    });

    const result = await response.json();
    console.log(result);

    document.getElementById('media-title').value = '';
    document.getElementById('media-type').value = '';

    await searchDatabase();
}
function displayResults(dataObj) {
    const listContainer = document.getElementById('media-list');

    listContainer.innerHTML = '';

    const mediaItems = dataObj.results;

    if (mediaItems.length === 0) {
        listContainer.innerHTML = '<p class="empty-message">No media found in your backlog.</p>';
        return;
    }

    mediaItems.forEach(item => {
        const itemCard = document.createElement('div');
        itemCard.className = 'media-card';
        itemCard.innerHTML = `
            <strong>${item.title}</strong>
            <span class="badge">${item.type}</span>
            <small>(${item.status})</small>
        `;
        listContainer.appendChild(itemCard);
    });
}

const searchForm = document.getElementById('search-form');
searchForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await searchDatabase();
});

const addForm = document.getElementById('add-form');
addForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await addMediaToDatabase();
});


document.addEventListener('DOMContentLoaded', async () => {
    await searchDatabase();
});
