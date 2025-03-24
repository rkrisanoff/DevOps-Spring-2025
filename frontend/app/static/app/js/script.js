document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.client-table');
    const searchContainer = document.querySelector('.search-container');
    const toggleTableBtn = document.querySelector('.toggle-table-btn');
    const updateTableBtn = document.querySelector('.update-table-btn');


    // Event listener for toggling the table visibility
    toggleTableBtn.addEventListener('click', function() {
        if (table.style.display === 'table') {
            table.style.display = 'none'; // Hide the table
            searchContainer.style.display = 'none';
            updateTableBtn.style.display = 'none'; // Hide the update button
            toggleTableBtn.textContent = 'Show Table'; // Update button text
        } else {
            table.style.display = 'table'; // Show the table
            searchContainer.style.display = "block";
            updateTableBtn.style.display = 'inline-block'; // Show the update button
            toggleTableBtn.textContent = 'Hide Table'; // Update button text
        }
    });


    // Add click handlers to table rows
    const tableRows = document.querySelectorAll('.client-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            const clientName = this.querySelector('.client-name').textContent;
            alert(`Selected client: ${clientName}`);
        });
    });

    // Handle Create Form (renamed from Insert Form)
    const createForm = document.getElementById('createForm');
    createForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = {
            name: document.getElementById('createName').value,
            quantity: parseInt(document.getElementById('createQuantity').value)
        };

        fetch('/create_client/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                createForm.reset();
                alert('Client saved successfully!');
            } else {
                alert('Error saving client: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error saving client');
        });
    });


    // Handle Update Form
    const updateForm = document.getElementById('updateForm');
    updateForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = {
            id: parseInt(document.getElementById('updateId').value),
            name: document.getElementById('updateName').value,
            quantity: parseInt(document.getElementById('updateQuantity').value)
        };

        fetch('/update_client/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateForm.reset();
                alert('Client updated successfully!');
            } else {
                alert('Error updating client: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating client');
        });
    });


    // Search functionality
    const searchInput = document.getElementById('clientSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchText = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.client-table tbody tr');
            tableRows.forEach(row => {
                const name = row.querySelector('.client-name').textContent.toLowerCase();
                row.style.display = name.includes(searchText) ? '' : 'none';
            });
        });
    }


    updateTableBtn.addEventListener('click', function() {
        drawTable(); // Call the function to update the table
    });

    function drawTable() {
        const tableBody = document.querySelector('.client-table tbody');
        tableBody.innerHTML = ''; // Clear existing table data

        // Fetch client data from the server
        fetch('/get_clients/')
            .then(response => response.json())
            .then(clients => {
                // Loop through the data and create table rows
                clients.forEach(client => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${client.id}</td>
                        <td class="client-name">${client.name}</td>
                        <td>${client.quantity}</td>
                        <td>${client.created_at}</td>
                        <td>${client.updated_at}</td>
                    `;
                    tableBody.appendChild(row);
                });

                // Show the table after drawing it
                const table = document.querySelector('.client-table');
                table.style.display = 'table'; // Show the table
                document.querySelector('.search-container').style.display = 'block'; // Show the search input
            })
            .catch(error => {
                console.error('Error fetching client data:', error);
            });
    }

    // Add event listener for the color change button
    const backendCheckBtn = document.getElementById('backendCheckBtn');
    backendCheckBtn.addEventListener('click', function() {
        backendCheckBtn.style.backgroundColor = "grey";
        backendCheckBtn.textContent = `processing...`
        fetch('/backend_health_check/') // Call the new endpoint
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    backendCheckBtn.style.backgroundColor = data.color;
                    backendCheckBtn.textContent = `Backend: ${data.msg}`
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error with checking backend health');
            });
    });

});
