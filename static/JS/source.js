let searchInputPages = document.getElementById("input-pages");
let searchInputName = document.getElementById("input-item");
let loadingOverlay = document.getElementById("loadingOverlay"); 
let resultsT

searchInputPages.addEventListener("input", function (event) {
    const inputValue = searchInputPages.value.replace(/\D/g, '');
    
    if (searchInputPages.value >20) {
        searchInputPages.value = "20"
    }
    
});

// document.getElementById("myButton").addEventListener("click", function(event) {
//   event.preventDefault();
//   document.getElementById("loading-overlay").style.display = "block";
//   // Submit the form using JavaScript
//   document.getElementById("form").submit();
// });

// document.addEventListener("DOMContentLoaded", function() {
//   // Hide the loading animation when the response is received
//   document.getElementById("loading-overlay").style.display = "none";
// });

// document.getElementById("myButton").addEventListener("click", function(event) {
//     event.preventDefault();
//     loadingOverlay.style.visibility = true;
    

// });
