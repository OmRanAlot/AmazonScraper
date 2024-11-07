let searchInputPages = document.getElementById("input-pages");
let searchInputName = document.getElementById("input-item");

searchInputPages.addEventListener("input", function (event) {
    const inputValue = searchInputPages.value;
    searchInputPages.value = inputValue.replace(/\D/g, '');
    if (searchInputPages.value >20) {
        searchInputPages.value = "20"
    }
    
});