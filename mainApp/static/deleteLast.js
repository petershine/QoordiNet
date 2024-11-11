async function deleteLast(buttonElement) {
    try {
        showSpinner()
        const response = await fetch('/delete_last?days=0', {
            method: 'DELETE'
        });
        console.log(response)
    } catch (error) {
        console.error('Fetch error:', error);
    } finally {
        hideSpinner()
    }
}