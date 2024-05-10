document.getElementById("crawlerForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = {
            seed_url: document.getElementById("seed_url").value,
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

            const result = await response.json();
            document.getElementById("response").innerHTML = `<p>${result.message}</p>`;
        } catch (error) {
            document.getElementById("response").innerHTML = `<p style="color: red;">Error occurred: ${error.message}</p>`;
        }
});
