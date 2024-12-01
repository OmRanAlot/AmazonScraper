let searchInputPages = document.getElementById("input-pages");
let searchInputName = document.getElementById("input-item");
let loadingOverlay = document.getElementById("loadingOverlay"); 

searchInputPages.addEventListener("input", function (event) {
    const inputValue = searchInputPages.value.replace(/\D/g, '');
    if (searchInputPages.value >20) {
        searchInputPages.value = "0";
    }
    
});




