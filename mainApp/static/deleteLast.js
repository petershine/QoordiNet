async function deleteLast(buttonElement) {
    try {
        showSpinner()
        const response = await fetch('/delete_last?days=0', {
            method: 'DELETE'
        });
        const jsonData = await response.json(); // This is your array of dictionaries
        console.log(jsonData)
    } catch (error) {
        console.error('Fetch error:', error);
    } finally {
        hideSpinner()
    }
}