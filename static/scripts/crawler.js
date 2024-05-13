document.getElementById("crawlerForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = {
        seed_url: document.getElementById("seed_url").value
        .split(",")
        .map(url => url.trim()),
        keywords: document.getElementById("keywords").value.split(",").map(kw => kw.trim())
    };

    try {
        const response = await fetch("/crawl", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });
        
        console.log(response)
        if (response.ok) {
            window.location.href = "/result";
        } else {
            throw new Error('Server error or invalid response.');
        }
    }
    catch (error) {
    }
});