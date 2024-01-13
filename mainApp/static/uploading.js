document.getElementById('build_database_submit').addEventListener('click', function () {
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
        showSpinner()
        const response = await fetch(endpointUrl, {
            method: 'POST',
            body: formData,
            // redirect: 'manual'
        });
        console.log('response', response)

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }


        if (response.redirected) {
            console.log('Redirected to:', response.url);
            window.location.href = response.url;
            return
        }


        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            const result = await response.json();
            console.log('JSON Response:', result);
        } else {
            const textResult = await response.text();
            console.log('Text Response:', textResult);
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideSpinner()
    }
}
