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

    // Handle Create Form
    const createForm = document.getElementById('createForm');
    createForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = {
            title: document.getElementById('createTitle').value,
            author: document.getElementById('createAuthor').value,
            genres: document.getElementById('createGenres').value.split(',').map(g => g.trim()),
            year: parseInt(document.getElementById('createYear').value),
            language: document.getElementById('createLanguage').value,
            pages: parseInt(document.getElementById('createPages').value),
            status: document.getElementById('createStatus').value
        };

        fetch('/create_book/', {
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
                alert('Book created successfully!');
            } else {
                alert('Error creating book: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error creating book');
        });
    });


    // Handle Update Form
    const updateForm = document.getElementById('updateForm');
    updateForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Get all form inputs
        const formData = {
            id: parseInt(document.getElementById('updateId').value)
        };

        // Only add fields that have values
        const title = document.getElementById('updateTitle').value;
        const author = document.getElementById('updateAuthor').value;
        const genres = document.getElementById('updateGenres').value;
        const year = document.getElementById('updateYear').value;
        const language = document.getElementById('updateLanguage').value;
        const pages = document.getElementById('updatePages').value;
        const status = document.getElementById('updateStatus').value;

        if (title) formData.title = title;
        if (author) formData.author = author;
        if (genres) formData.genres = genres.split(',').map(g => g.trim());
        if (year) formData.year = parseInt(year);
        if (language) formData.language = language;
        if (pages) formData.pages = parseInt(pages);
        if (status) formData.status = status;

        fetch('/update_book/', {
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
                alert('Book updated successfully!');
                
                // Optionally display the updated book data
                if (data.book) {
                    console.log('Updated book:', data.book);
                }
                
            } else {
                alert('Error updating book: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating book');
        });
    });

    // Get book form handler
    const getBookForm = document.getElementById('getBookForm');
    const bookDetails = document.getElementById('bookDetails');
    const cleanButton = document.getElementById('cleanBookDetails');

    // Function to clean book details
    function cleanBookDisplay() {
        // Hide the details container
        bookDetails.style.display = 'none';
        
        // Clear all the text content
        document.getElementById('bookTitle').textContent = '';
        document.getElementById('bookAuthor').textContent = '';
        document.getElementById('bookGenres').textContent = '';
        document.getElementById('bookYear').textContent = '';
        document.getElementById('bookLanguage').textContent = '';
        document.getElementById('bookPages').textContent = '';
        document.getElementById('bookStatus').textContent = '';
        
        // Clear the input field
        document.getElementById('getBookId').value = '';

    }

    // Add click handler for clean button
    cleanButton.addEventListener('click', cleanBookDisplay);

    // Update the existing get book form handler
    getBookForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const bookId = document.getElementById('getBookId').value;
        
        fetch(`/get_book/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update the book details display
                    document.getElementById('bookTitle').textContent = data.book.title;
                    document.getElementById('bookAuthor').textContent = data.book.author;
                    document.getElementById('bookGenres').textContent = data.book.genres.join(', ');
                    document.getElementById('bookYear').textContent = data.book.year;
                    document.getElementById('bookLanguage').textContent = data.book.language;
                    document.getElementById('bookPages').textContent = data.book.pages;
                    document.getElementById('bookStatus').textContent = data.book.status;
                    
                    // Show the details container
                    bookDetails.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // Handle Delete Form
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const bookId = document.getElementById('deleteId').value;
        fetch(`/delete_book/${bookId}/`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                deleteForm.reset();
                alert('Book deleted successfully!');
            } else {
                alert('Error deleting book: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting book');
        });
    });

    // Search functionality
    const searchInput = document.getElementById('clientSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchText = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.client-table tbody tr');
            tableRows.forEach(row => {
                const title = row.querySelector('.book-title').textContent.toLowerCase();
                row.style.display = title.includes(searchText) ? '' : 'none';
            });
        });
    }

    updateTableBtn.addEventListener('click', function() {
        drawTable();
    });

    function drawTable() {
        const tableBody = document.querySelector('.client-table tbody');
        tableBody.innerHTML = '';

        fetch('/get_books/')
            .then(response => response.json())
            .then(books => {
                books.forEach(book => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${book.id}</td>
                        <td class="book-title">${book.title}</td>
                        <td>${book.author}</td>
                        <td>${book.genres.join(', ')}</td>
                        <td>${book.year}</td>
                        <td>${book.language}</td>
                        <td>${book.pages}</td>
                        <td>${book.status}</td>
                    `;
                    tableBody.appendChild(row);
                });

                table.style.display = 'table';
                searchContainer.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching book data:', error);
            });
    }


    const backendCheckBtn = document.getElementById('backendCheckBtn');
    backendCheckBtn.addEventListener('click', function() {
        backendCheckBtn.style.backgroundColor = "grey";
        backendCheckBtn.textContent = `processing...`
        fetch('/backend_health_check/')
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
                alert('Error checking backend health');
            });
    });

    
    document.getElementById('fillUpdateForm').addEventListener('click', function() {
        const bookId = document.getElementById('updateId').value;
        if (!bookId) {
            alert('Please enter a book ID first');
            return;
        }

        fetch(`/get_book/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const book = data.book;
                    document.getElementById('updateTitle').value = book.title;
                    document.getElementById('updateAuthor').value = book.author;
                    document.getElementById('updateGenres').value = book.genres.join(', ');
                    document.getElementById('updateYear').value = book.year;
                    document.getElementById('updateLanguage').value = book.language;
                    document.getElementById('updatePages').value = book.pages;
                    document.getElementById('updateStatus').value = book.status;
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error fetching book data');
            });
    });

});
