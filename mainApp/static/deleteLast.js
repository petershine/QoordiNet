async function deleteLast(buttonElement) {
    try {
        showSpinner()
        const response = await fetch('/delete_last', {
            method: 'DELETE',
            redirect: "follow"
        })
        console.log(response)
        if (response.redirected) {
            window.location.href = response.url;
        }
    } catch (error) {
        console.error('Fetch error:', error);
    } finally {
    }
}