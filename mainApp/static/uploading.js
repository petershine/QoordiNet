document.getElementById('build_database_submit').addEventListener('click', function() {
    const form = this.form;
    const formId = form.getAttribute('id');
    const endpointUrl = form.dataset.endpoint; // assuming you use a data attribute to specify the endpoint
    uploadFile(formId, endpointUrl);
});

async function uploadFile(formId, endpointUrl) {
    console.log('formId', formId)
    console.log('endpointUrl', endpointUrl)

    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const fileField = form.querySelector('input[type="file"]');

    formData.append('csv_file', fileField.files[0]);
    console.log('formData', formData)

    try {
        const response = await fetch(endpointUrl, {
            method: 'POST',
            body: formData
        });
        console.log('response', response)

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        } else {
            console.log('(begin .json()...)')
            const result = await response.json();
            console.log('Success:', result);
            // Handle success - e.g., display a success message
        }
    } catch (error) {
        console.error('Error:', error);
        // Handle errors - e.g., display an error message
    }
}
