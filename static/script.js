async function searchDatabase() {
    const query = document.getElementById('search-form').querySelector('input[type="search"]').value;

    const response = await fetch(`/api/search?q=${query}`);
    const dataObj = await response.json();

    displayResults(dataObj);

    console.log(dataObj.results);
}

const mediaForm = document.getElementById('search-form');
mediaForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await searchDatabase();
});
