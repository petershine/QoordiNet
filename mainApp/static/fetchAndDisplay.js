async function fetchAndDisplayData() {
    try {
        showSpinner()
        const response = await fetch('/activities');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const jsonData = await response.json(); // This is your array of dictionaries
        console.log(jsonData)


        const table = document.getElementsByClassName('qoordinet_table')[0].getElementsByTagName('tbody')[0];

        jsonData.forEach(item => {
            const row = table.insertRow();

            Object.values(item).forEach((text, index) => {
                const cell = row.insertCell();

                if (index == 0) {
                    try {
                        const date = new Date(text);

                        if (!isNaN(date.getTime())) {
                            const formattedDate = date.toISOString().slice(0, 10);
                            cell.textContent = formattedDate;
                        } else {
                            cell.textContent = text;
                        }
                    } catch (error) {
                        cell.textContent = text;
                    }
                } else {
                    cell.textContent = text;
                }
            });
        });
    } catch (error) {
        console.error('Fetch error:', error);
    } finally {
        hideSpinner()

        scrollToBottom()
    }
}
