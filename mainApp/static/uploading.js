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
        }

        // Check the response type
        const contentType = response.headers.get("content-type");

        if (contentType && contentType.includes("application/json")) {
            // Handle JSON response
            const result = await response.json();
            console.log('JSON Response:', result);
        } else if (response.redirected) {
            // Handle redirection
            console.log('Redirected to:', response.url);
            // You may want to follow the redirect or take other actions here
        } else {
            // Handle other content types (e.g., text)
            const textResult = await response.text();
            console.log('Text Response:', textResult);
        }
    } catch (error) {
        console.error('Error:', error);
        // Handle errors - e.g., display an error message
    }
}
