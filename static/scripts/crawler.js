document.getElementById('crawlForm').onsubmit = function(event) {
    event.preventDefault();  // Prevent the default form submission behavior
    
    // Gather data from the form
    const seedUrl = document.getElementById('seed_url').value;
    const keywordsInput = document.getElementById('keywords').value;
    const keywords = keywordsInput.split(',').map(item => item.trim());  // Clean the keywords

    // Use fetch API to send a POST request to your Flask server
    fetch('/crawl', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ seed_url: seedUrl, keywords: keywords })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();  // Parse JSON data from the response
    })
    .then(data => {
        // Redirect to the results page if the request was successful
        window.location.href = "/result";  // Ensure the route is correct as per your Flask setup
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Error:', error);
        alert('There was a problem with your fetch operation: ' + error.message);
    });
};
