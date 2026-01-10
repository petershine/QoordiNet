async function rebuildForAppConfiguration(buttonElement) {
    try {
        showSpinner()
        const response = await fetch('/rebuildForAppConfiguration', {
            method: 'DELETE',
            redirect: "follow"
        })
        console.log(response)
        if (response.redirected) {
            window.location.href = response.url;
        }
        else if (response.ok){
            location.reload()
        }
    } catch (error) {
        console.error('Fetch error:', error);
    } finally {
    }
}