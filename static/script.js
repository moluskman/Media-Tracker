async function searchDatabase() {
    const query = document.getElementById('search-form').querySelector('input[type="search"]').value;
    const response = await fetch(`/api/search?q=${query}`);
    const results = await response.json();
    displayResults(results);

    console.log(data.results);
}
