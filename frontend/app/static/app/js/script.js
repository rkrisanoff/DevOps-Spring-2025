let currentPage = 1;
const itemsPerPage = 10;
let totalPages = 1;
let currentTableType = 'client'; // or 'recommendations'
let totalItems = 0; // Add this to track total number of items

function drawTable() {
    const tableBody = document.querySelector('.client-table tbody');
    const recommendationsTable = document.querySelector('.recommendations-table');
    const clientPagination = document.querySelector('.client-pagination');
    const recommendationsPagination = document.querySelector('.recommendations-pagination');

    tableBody.innerHTML = '';
    recommendationsTable.style.display = 'none';
    recommendationsPagination.style.display = 'none';
    currentTableType = 'client';

    const offset = (currentPage - 1) * itemsPerPage;
    const limit = itemsPerPage;

    fetch(`/get_books/?offset=${offset}&limit=${limit}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const items = data.items;
            totalItems = data.total || items.length; // Get total from API or fallback to items length
            totalPages = Math.ceil(totalItems / itemsPerPage);

            displayPage(items, tableBody);
            updatePagination('client');

            const table = document.querySelector('.client-table');
            const searchContainer = document.querySelector('.search-container');
            table.style.display = 'table';
            searchContainer.style.display = 'block';
            clientPagination.style.display = 'flex';
        })
        .catch(error => {
            console.error('Error fetching book data:', error);
            alert(error);
        });
}

function drawRecommendations(bookId) {
    const clientTable = document.querySelector('.client-table');
    const recommendationsTable = document.querySelector('.recommendations-table');
    const recommendationsBody = recommendationsTable.querySelector('tbody');
    const clientPagination = document.querySelector('.client-pagination');
    const recommendationsPagination = document.querySelector('.recommendations-pagination');

    recommendationsBody.innerHTML = '';
    clientTable.style.display = 'none';
    clientPagination.style.display = 'none';
    currentTableType = 'recommendations';

    const offset = (currentPage - 1) * itemsPerPage;
    const limit = itemsPerPage;

    fetch(`/get_recommendations/${bookId}/?offset=${offset}&limit=${limit}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const items = data.similar_books;
            totalItems = data.total || items.length; // Get total from API or fallback to items length
            totalPages = Math.ceil(totalItems / itemsPerPage);

            displayPage(items, recommendationsBody);
            updatePagination('recommendations');

            recommendationsTable.style.display = 'table';
            const searchContainer = document.querySelector('.search-container');
            searchContainer.style.display = 'block';
            recommendationsPagination.style.display = 'flex';
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
            alert(error);
        });
}

function displayPage(items, tableBody) {
    tableBody.innerHTML = ''; // Clear the table body

    items.forEach(book => {
        const row = document.createElement('tr');
        if (currentTableType === 'client') {
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
        } else {
            row.innerHTML = `
                <td>${book.id}</td>
                <td class="book-title">${book.title}</td>
                <td>${book.author}</td>
                <td>${book.genres.join(', ')}</td>
                <td>${book.publication_year}</td>
                <td>${book.pages}</td>
                <td>${(book.similarity * 100).toFixed(2)}%</td>
            `;
        }
        tableBody.appendChild(row);
    });
}

function updatePagination(tableType) {
    const pagination = document.querySelector(`.${tableType}-pagination`);
    const pageInfo = pagination.querySelector('.page-info');
    const prevButton = pagination.querySelector('.prev-page');
    const nextButton = pagination.querySelector('.next-page');

    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    prevButton.disabled = currentPage === 1;
    nextButton.disabled = currentPage === totalPages;
}

function initializeTableControls(table, searchContainer, closeTableBtn, showRecommendationsBtn, showTableBtn) {
    // Show table button
    showTableBtn.addEventListener('click', function() {
        currentPage = 1; // Reset to first page
        const recommendationsTable = document.querySelector('.recommendations-table');
        recommendationsTable.style.display = 'none';
        table.style.display = 'table';
        searchContainer.style.display = 'block';
        drawTable();
    });

    // Close table button
    closeTableBtn.addEventListener('click', function() {
        const recommendationsTable = document.querySelector('.recommendations-table');
        table.style.display = 'none';
        recommendationsTable.style.display = 'none';
        searchContainer.style.display = 'none';
    });

    // Show recommendations button
    showRecommendationsBtn.addEventListener('click', function() {
        currentPage = 1; // Reset to first page
        const bookId = document.getElementById('recommendationBookId').value;
        if (!bookId) {
            alert('Please enter a book ID first');
            return;
        }

        searchContainer.style.display = 'block';
        drawRecommendations(bookId);
    });

    // Add pagination handlers
    document.querySelectorAll('.pagination').forEach(pagination => {
        const prevButton = pagination.querySelector('.prev-page');
        const nextButton = pagination.querySelector('.next-page');

        prevButton.addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                if (currentTableType === 'client') {
                    drawTable();
                } else {
                    const bookId = document.getElementById('recommendationBookId').value;
                    drawRecommendations(bookId);
                }
            }
        });

        nextButton.addEventListener('click', function() {
            if (currentPage < totalPages) {
                currentPage++;
                if (currentTableType === 'client') {
                    drawTable();
                } else {
                    const bookId = document.getElementById('recommendationBookId').value;
                    drawRecommendations(bookId);
                }
            }
        });
    });
}

function initializeSearchFunctionality(searchInput) {
    searchInput.addEventListener('input', function() {
        const searchText = this.value.toLowerCase();
        const clientTableRows = document.querySelectorAll('.client-table tbody tr');
        const recommendationsTableRows = document.querySelectorAll('.recommendations-table tbody tr');

        // Search in regular table
        clientTableRows.forEach(row => {
            const title = row.querySelector('.book-title').textContent.toLowerCase();
            row.style.display = title.includes(searchText) ? '' : 'none';
        });

        // Search in recommendations table
        recommendationsTableRows.forEach(row => {
            const title = row.querySelector('.book-title').textContent.toLowerCase();
            row.style.display = title.includes(searchText) ? '' : 'none';
        });
    });
}

function initializeBackendCheck(backendCheckBtn) {
    backendCheckBtn.addEventListener('click', function() {
        backendCheckBtn.style.backgroundColor = "grey";
        backendCheckBtn.textContent = "processing...";
        fetch('/backend_health_check/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                backendCheckBtn.style.backgroundColor = 'green';
                backendCheckBtn.textContent = `Backend: ${data.version}`;
            })
            .catch(error => {
                backendCheckBtn.style.backgroundColor = 'red';
                console.error('Error:', error);
                alert('Error checking backend health');
            });
    });
}

function initializeGetBookForm(getBookForm) {
    getBookForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const bookId = document.getElementById('getBookId').value;
        const bookDetails = document.getElementById('bookDetails');

        fetch(`/get_book/${bookId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('bookTitle').textContent = data.title;
                document.getElementById('bookAuthor').textContent = data.author;
                document.getElementById('bookGenres').textContent = data.genres.join(', ');
                document.getElementById('bookYear').textContent = data.year;
                document.getElementById('bookLanguage').textContent = data.language;
                document.getElementById('bookPages').textContent = data.pages;
                document.getElementById('bookStatus').textContent = data.status;

                bookDetails.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                alert(error);
            });
    });
}

function initializeCreateForm(createForm) {
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
        .then(response => {
            if (!response.ok) {
                throw new Error(`Status: ${response.status}`);
            }
            createForm.reset();
            return response.json();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error creating book');
        });
    });
}

function initializeUpdateForm(updateForm) {
    updateForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const updateID = document.getElementById('updateId').value;
        const formData = {
            id: parseInt(updateID)
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
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Status: ${response.status}`);
            }
            updateForm.reset();
            return response.json();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating book');
        });
    });
}

function initializeFillUpdateForm(fillInToUpdateBtn) {
    fillInToUpdateBtn.addEventListener('click', function() {
        const bookId = document.getElementById('updateId').value;
        if (!bookId) {
            alert('Please enter a book ID first');
            return;
        }

        fetch(`/get_book/${bookId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Status: ${response.status}`);
                }
                return response.json();
            })
            .then(book => {
                document.getElementById('updateTitle').value = book.title;
                document.getElementById('updateAuthor').value = book.author;
                document.getElementById('updateGenres').value = book.genres.join(', ');
                document.getElementById('updateYear').value = book.year;
                document.getElementById('updateLanguage').value = book.language;
                document.getElementById('updatePages').value = book.pages;
                document.getElementById('updateStatus').value = book.status;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error fetching book data');
            });
    });
}

function initializeDeleteForm(deleteForm) {
    deleteForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const bookId = parseInt(document.getElementById('deleteId').value);
        fetch(`/delete_book/${bookId}/`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Status: ${response.status}`);
            }
            deleteForm.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting book ' + error);
        });
    });
}

function initializeCleanButton(cleanButton) {
    cleanButton.addEventListener('click', function(e) {
        e.preventDefault();
        const bookDetails = document.getElementById('bookDetails');
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
    });
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeTableControls,
        drawTable,
        initializeSearchFunctionality,
        initializeBackendCheck,
        initializeGetBookForm,
        initializeCreateForm,
        initializeUpdateForm,
        initializeFillUpdateForm,
        initializeDeleteForm,
        initializeCleanButton
    };
}

// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.client-table');
    const searchContainer = document.querySelector('.search-container');
    const closeTableBtn = document.querySelector('.close-table-btn');
    const showRecommendationsBtn = document.querySelector('.show-recommendations-btn');
    const showTableBtn = document.querySelector('.show-table-btn');

    initializeTableControls(table, searchContainer, closeTableBtn, showRecommendationsBtn, showTableBtn);

    const searchInput = document.getElementById('clientSearch');
    initializeSearchFunctionality(searchInput);

    const backendCheckBtn = document.getElementById('backendCheckBtn');
    initializeBackendCheck(backendCheckBtn);

    // Handle Create Form
    const createForm = document.getElementById('createForm');
    initializeCreateForm(createForm);

    // Handle Update Form
    const updateForm = document.getElementById('updateForm');
    initializeUpdateForm(updateForm);

    // Fill-In in update form
    const fillInToUpdateBtn = document.getElementById('fillUpdateForm');
    initializeFillUpdateForm(fillInToUpdateBtn);

    // Get book form
    const getBookForm = document.getElementById('getBookForm');
    initializeGetBookForm(getBookForm);

    // Add click handler for clean button
    const cleanBookDetailsField = document.getElementById('cleanBookDetails');
    initializeCleanButton(cleanBookDetailsField);

    // Handle Delete Form
    const deleteForm = document.getElementById('deleteForm');
    initializeDeleteForm(deleteForm);
});
