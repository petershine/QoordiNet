function embedContent(url, targetElementId) {
    const embeddedContent = document.getElementById(targetElementId);

    if (!targetElementId) {
        console.error('Element with ID "${targetElementId}" not found!');
        return;
    }

    fetch(url)
        .then(response => response.text())
        .then(html => {
            embeddedContent.innerHTML = html;
        })
        .catch(error => {
            console.error('Error fetching embedded content:', error);
        });
}