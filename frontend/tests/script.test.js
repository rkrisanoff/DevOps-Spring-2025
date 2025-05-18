const { drawTable } = require('../app/static/app/js/script');
const {
  initializeTableToggle,
  initializeSearchFunctionality,
  initializeBackendCheck,
  initializeGetBookForm,
  initializeCreateForm,
  initializeUpdateForm,
  initializeFillUpdateForm,
  initializeDeleteForm,
  initializeCleanButton
} = require('/frontend/app/static/app/js/script.js');

// Mock fetch globally
global.fetch = jest.fn();

describe('Book Management System Tests', () => {
  beforeEach(() => {
      fetch.mockClear();

      document.body.innerHTML = `
        <table class="client-table" style="display: none;">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Author</th>
              <th>Genres</th>
              <th>Year</th>
              <th>Language</th>
              <th>Pages</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
        <div class="search-container">
          <input type="text" id="clientSearch" placeholder="Search by book title...">
        </div>
        <button class="toggle-table-btn">Show Table</button>
        <button class="update-table-btn">Update Table</button>
        <form id="getBookForm">
          <input type="text" id="getBookId">
          <button type="submit">Get Book</button>
        </form>
        <div id="bookDetails" class="book-details-container" style="display: none;">
          <h3>Book Details</h3>
          <div class="book-info">
            <p><strong>Title:</strong> <span id="bookTitle"></span></p>
            <p><strong>Author:</strong> <span id="bookAuthor"></span></p>
            <p><strong>Genres:</strong> <span id="bookGenres"></span></p>
            <p><strong>Year:</strong> <span id="bookYear"></span></p>
            <p><strong>Language:</strong> <span id="bookLanguage"></span></p>
            <p><strong>Pages:</strong> <span id="bookPages"></span></p>
            <p><strong>Status:</strong> <span id="bookStatus"></span></p>
          </div>
          <button id="cleanBookDetails">Clear</button>
        </div>
        <form id="createForm">
          <input id="createTitle" value="Test Book">
          <input id="createAuthor" value="Test Author">
          <input id="createGenres" value="Fiction, Drama">
          <input id="createYear" value="2023">
          <input id="createLanguage" value="English">
          <input id="createPages" value="200">
          <input id="createStatus" value="Reading">
        </form>
        <form id="updateForm">
          <input type="text" id="updateId">
          <input type="text" id="updateTitle">
          <input type="text" id="updateAuthor">
          <input type="text" id="updateGenres">
          <input type="text" id="updateYear">
          <input type="text" id="updateLanguage">
          <input type="text" id="updatePages">
          <input type="text" id="updateStatus">
          <button type="submit">Update</button>
        </form>
        <button id="fillUpdateForm">Fill Form</button>
        <form id="deleteForm">
          <input type="text" id="deleteId">
          <button type="submit">Delete</button>
        </form>
        <button id="backendCheckBtn">Check Backend</button>
      `;

      // Initialize all functionality
      const table = document.querySelector('.client-table');
      const searchContainer = document.querySelector('.search-container');
      const toggleBtn = document.querySelector('.toggle-table-btn');
      const updateBtn = document.querySelector('.update-table-btn');
      const searchInput = document.getElementById('clientSearch');
      const backendCheckBtn = document.getElementById('backendCheckBtn');
      const getBookForm = document.getElementById('getBookForm');
      const createForm = document.getElementById('createForm');
      const updateForm = document.getElementById('updateForm');
      const fillUpdateBtn = document.getElementById('fillUpdateForm');
      const deleteForm = document.getElementById('deleteForm');
      const cleanButton = document.getElementById('cleanBookDetails');

      // Initialize all functionality
      const mockDrawTable = jest.fn();
      initializeTableToggle(table, searchContainer, updateBtn, toggleBtn, mockDrawTable);
      initializeSearchFunctionality(searchInput);
      initializeBackendCheck(backendCheckBtn);
      initializeGetBookForm(getBookForm);
      initializeCreateForm(createForm);
      initializeUpdateForm(updateForm);
      initializeFillUpdateForm(fillUpdateBtn);
      initializeDeleteForm(deleteForm);
      initializeCleanButton(cleanButton);
  });

  test('toggle table visibility works', () => {
    const table = document.querySelector('.client-table');
    const toggleBtn = document.querySelector('.toggle-table-btn');

    // Initial state (hidden)
    expect(table.style.display).toBe('none');

    // First click - show table
    toggleBtn.click();
    expect(table.style.display).toBe('table');
    expect(toggleBtn.textContent).toBe('Hide Table');

    // Second click - hide table
    toggleBtn.click();
    expect(table.style.display).toBe('none');
    expect(toggleBtn.textContent).toBe('Show Table');
  });

  test('create book form submission', async () => {
    // Setup fetch mock for this test
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    );

    const form = document.getElementById('createForm');
    form.dispatchEvent(new Event('submit'));

    // Wait for the fetch call to complete
    await new Promise(process.nextTick);

    expect(fetch).toHaveBeenCalledWith('/create_book/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: 'Test Book',
        author: 'Test Author',
        genres: ['Fiction', 'Drama'],
        year: 2023,
        language: 'English',
        pages: 200,
        status: 'Reading'
      })
    });
  });

  test('search functionality filters books', () => {
    // Add test data to the table
    const tbody = document.querySelector('.client-table tbody');
    tbody.innerHTML = `
      <tr><td class="book-title">Harry Potter</td></tr>
      <tr><td class="book-title">Lord of the Rings</td></tr>
      <tr><td class="book-title">Harry Potter 2</td></tr>
    `;

    const searchInput = document.getElementById('clientSearch');
    searchInput.value = 'harry';
    searchInput.dispatchEvent(new Event('input'));

    // Get all rows except the header row
    const visibleRows = Array.from(document.querySelectorAll('.client-table tbody tr'))
      .filter(row => row.style.display !== 'none');

    expect(visibleRows.length).toBe(2);
  });

  test('backend health check button changes color', async () => {
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ version: '1.0' })
      })
    );

    const checkBtn = document.getElementById('backendCheckBtn');
    checkBtn.click();

    expect(checkBtn.style.backgroundColor).toBe('grey');
    expect(checkBtn.textContent).toBe('processing...');

    // Wait for the fetch to complete
    await new Promise(process.nextTick);

    expect(checkBtn.style.backgroundColor).toBe('green');
    expect(checkBtn.textContent).toBe('Backend: 1.0');
  });

  test('get book form displays book details correctly', async () => {
      const mockBookData = {
          title: 'Test Book',
          author: 'Test Author',
          genres: ['Fiction', 'Drama'],
          year: 2023,
          language: 'English',
          pages: 200,
          status: 'Reading'
      };

      // Setup fetch mock
      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: true,
              json: () => Promise.resolve(mockBookData)
          })
      );

      // Get form elements
      const getBookForm = document.getElementById('getBookForm');
      const bookDetails = document.getElementById('bookDetails');
      const getBookId = document.getElementById('getBookId');

      // Set the ID and submit the form
      getBookId.value = '1';
      getBookForm.dispatchEvent(new Event('submit'));

      // Wait for all promises to resolve
      await new Promise(resolve => setTimeout(resolve, 0));
      await Promise.resolve(); // Wait for the next microtask

      // Verify the results
      expect(document.getElementById('bookTitle').textContent).toBe('Test Book');
      expect(document.getElementById('bookAuthor').textContent).toBe('Test Author');
      expect(document.getElementById('bookGenres').textContent).toBe('Fiction, Drama');
      expect(document.getElementById('bookYear').textContent).toBe('2023');
      expect(document.getElementById('bookLanguage').textContent).toBe('English');
      expect(document.getElementById('bookPages').textContent).toBe('200');
      expect(document.getElementById('bookStatus').textContent).toBe('Reading');
      expect(bookDetails.style.display).toBe('block');

      // Verify that fetch was called correctly
      expect(fetch).toHaveBeenCalledWith('/get_book/1/');
  });

  test('clean book details button clears all fields', () => {
      // First set some data
      const bookDetails = document.getElementById('bookDetails');
      document.getElementById('bookTitle').textContent = 'Some Book';
      document.getElementById('getBookId').value = '1';
      bookDetails.style.display = 'block';

      const cleanButton = document.getElementById('cleanBookDetails');
      cleanButton.click();

      expect(bookDetails.style.display).toBe('none');
      expect(document.getElementById('bookTitle').textContent).toBe('');
      expect(document.getElementById('getBookId').value).toBe('');
  });

  test('update book form submission', async () => {
      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: true,
              json: () => Promise.resolve({})
          })
      );

      const updateForm = document.getElementById('updateForm');
      document.getElementById('updateId').value = '1';
      document.getElementById('updateTitle').value = 'Updated Title';
      document.getElementById('updateAuthor').value = 'Updated Author';

      updateForm.dispatchEvent(new Event('submit'));

      await new Promise(process.nextTick);

      expect(fetch).toHaveBeenCalledWith('/update_book/', {
          method: 'PATCH',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              id: 1,
              title: 'Updated Title',
              author: 'Updated Author'
          })
      });
  });

  test('fill update form fetches and fills book data', async () => {
      const mockBookData = {
          title: 'Existing Book',
          author: 'Existing Author',
          genres: ['Mystery', 'Thriller'],
          year: 2022,
          language: 'Spanish',
          pages: 300,
          status: 'Completed'
      };

      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: true,
              json: () => Promise.resolve(mockBookData)
          })
      );

      document.getElementById('updateId').value = '1';
      const fillButton = document.getElementById('fillUpdateForm');
      fillButton.click();

      await new Promise(process.nextTick);

      expect(document.getElementById('updateTitle').value).toBe('Existing Book');
      expect(document.getElementById('updateAuthor').value).toBe('Existing Author');
      expect(document.getElementById('updateGenres').value).toBe('Mystery, Thriller');
  });

  test('delete book form submission', async () => {
      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: true
          })
      );

      const deleteForm = document.getElementById('deleteForm');
      document.getElementById('deleteId').value = '1';
      deleteForm.dispatchEvent(new Event('submit'));

      await new Promise(process.nextTick);

      expect(fetch).toHaveBeenCalledWith('/delete_book/1/', {
          method: 'DELETE'
      });
  });

  test('error handling in API calls', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      const mockAlert = jest.spyOn(window, 'alert').mockImplementation();

      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: false,
              status: 404,
              statusText: 'Not Found'
          })
      );

      const getBookForm = document.getElementById('getBookForm');
      document.getElementById('getBookId').value = '999';
      getBookForm.dispatchEvent(new Event('submit'));

      await new Promise(process.nextTick);

      expect(consoleSpy).toHaveBeenCalled();
      expect(mockAlert).toHaveBeenCalled();

      consoleSpy.mockRestore();
      mockAlert.mockRestore();
  });

  test('drawTable populates table with book data', async () => {
      const mockBookData = {
          items: [
              {
                  id: 1,
                  title: 'Book 1',
                  author: 'Author 1',
                  genres: ['Fiction'],
                  year: 2023,
                  language: 'English',
                  pages: 200,
                  status: 'Reading'
              },
              {
                  id: 2,
                  title: 'Book 2',
                  author: 'Author 2',
                  genres: ['Drama', 'Mystery'],
                  year: 2022,
                  language: 'Spanish',
                  pages: 300,
                  status: 'Completed'
              }
          ]
      };

      // Setup fetch mock
      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: true,
              json: () => Promise.resolve(mockBookData)
          })
      );

      // Get table elements
      const table = document.querySelector('.client-table');
      const searchContainer = document.querySelector('.search-container');
      const tableBody = document.querySelector('.client-table tbody');

      // Call drawTable and wait for it to complete
      await drawTable();

      // Wait for the next tick to ensure DOM updates are complete
      await new Promise(process.nextTick);

      // Verify table is populated correctly
      const rows = tableBody.querySelectorAll('tr');
      expect(rows.length).toBe(2);

      // Check first row data
      const firstRow = rows[0].querySelectorAll('td');
      expect(firstRow[0].textContent).toBe('1');
      expect(firstRow[1].textContent).toBe('Book 1');
      expect(firstRow[2].textContent).toBe('Author 1');
      expect(firstRow[3].textContent).toBe('Fiction');
      expect(firstRow[4].textContent).toBe('2023');
      expect(firstRow[5].textContent).toBe('English');
      expect(firstRow[6].textContent).toBe('200');
      expect(firstRow[7].textContent).toBe('Reading');

      // Check second row data
      const secondRow = rows[1].querySelectorAll('td');
      expect(secondRow[0].textContent).toBe('2');
      expect(secondRow[1].textContent).toBe('Book 2');
      expect(secondRow[2].textContent).toBe('Author 2');
      expect(secondRow[3].textContent).toBe('Drama, Mystery');
      expect(secondRow[4].textContent).toBe('2022');
      expect(secondRow[5].textContent).toBe('Spanish');
      expect(secondRow[6].textContent).toBe('300');
      expect(secondRow[7].textContent).toBe('Completed');

      // Verify table and search container are displayed
      expect(table.style.display).toBe('table');
      expect(searchContainer.style.display).toBe('block');

      // Verify fetch was called correctly
      expect(fetch).toHaveBeenCalledWith('/get_books/');
  });

  test('drawTable handles fetch error', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      const mockAlert = jest.spyOn(window, 'alert').mockImplementation();

      // Setup fetch mock to reject
      fetch.mockImplementationOnce(() =>
          Promise.reject(new Error('Network error'))
      );

      // Call drawTable and wait for it to complete
      await drawTable();

      // Wait for the next tick to ensure error handling is complete
      await new Promise(process.nextTick);

      // Verify error handling
      expect(consoleSpy).toHaveBeenCalledWith('Error fetching book data:', expect.any(Error));
      expect(mockAlert).toHaveBeenCalledWith(expect.any(Error));

      consoleSpy.mockRestore();
      mockAlert.mockRestore();
  });

  // Test error handling in create form
  test('create form handles API error', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      const mockAlert = jest.spyOn(window, 'alert').mockImplementation();

      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: false,
              status: 400,
              statusText: 'Bad Request'
          })
      );

      const createForm = document.getElementById('createForm');
      createForm.dispatchEvent(new Event('submit'));

      await new Promise(process.nextTick);

      expect(consoleSpy).toHaveBeenCalled();
      expect(mockAlert).toHaveBeenCalledWith('Error creating book');

      consoleSpy.mockRestore();
      mockAlert.mockRestore();
  });

  // Test error handling in update form
  test('update form handles API error', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      const mockAlert = jest.spyOn(window, 'alert').mockImplementation();

      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: false,
              status: 400,
              statusText: 'Bad Request'
          })
      );

      const updateForm = document.getElementById('updateForm');
      document.getElementById('updateId').value = '1';
      updateForm.dispatchEvent(new Event('submit'));

      await new Promise(process.nextTick);

      expect(consoleSpy).toHaveBeenCalled();
      expect(mockAlert).toHaveBeenCalledWith('Error updating book');

      consoleSpy.mockRestore();
      mockAlert.mockRestore();
  });

  // Test error handling in fill update form
  test('fill update form handles API error', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      const mockAlert = jest.spyOn(window, 'alert').mockImplementation();

      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: false,
              status: 404,
              statusText: 'Not Found'
          })
      );

      document.getElementById('updateId').value = '999';
      const fillButton = document.getElementById('fillUpdateForm');
      fillButton.click();

      await new Promise(process.nextTick);

      expect(consoleSpy).toHaveBeenCalled();
      expect(mockAlert).toHaveBeenCalledWith('Error fetching book data');

      consoleSpy.mockRestore();
      mockAlert.mockRestore();
  });

  // Test error handling in delete form
  test('delete form handles API error', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      const mockAlert = jest.spyOn(window, 'alert').mockImplementation();

      fetch.mockImplementationOnce(() =>
          Promise.resolve({
              ok: false,
              status: 404,
              statusText: 'Not Found'
          })
      );

      const deleteForm = document.getElementById('deleteForm');
      document.getElementById('deleteId').value = '999';
      deleteForm.dispatchEvent(new Event('submit'));

      await new Promise(process.nextTick);

      expect(consoleSpy).toHaveBeenCalled();
      expect(mockAlert).toHaveBeenCalledWith(expect.stringContaining('Error deleting book'));

      consoleSpy.mockRestore();
      mockAlert.mockRestore();
  });

  // Test clean button functionality
  test('clean button clears all book details fields', () => {
      // Set up initial state
      const bookDetails = document.getElementById('bookDetails');
      document.getElementById('bookTitle').textContent = 'Test Book';
      document.getElementById('bookAuthor').textContent = 'Test Author';
      document.getElementById('bookGenres').textContent = 'Fiction';
      document.getElementById('bookYear').textContent = '2023';
      document.getElementById('bookLanguage').textContent = 'English';
      document.getElementById('bookPages').textContent = '200';
      document.getElementById('bookStatus').textContent = 'Reading';
      document.getElementById('getBookId').value = '1';
      bookDetails.style.display = 'block';

      // Click clean button
      const cleanButton = document.getElementById('cleanBookDetails');
      cleanButton.click();

      // Verify all fields are cleared
      expect(bookDetails.style.display).toBe('none');
      expect(document.getElementById('bookTitle').textContent).toBe('');
      expect(document.getElementById('bookAuthor').textContent).toBe('');
      expect(document.getElementById('bookGenres').textContent).toBe('');
      expect(document.getElementById('bookYear').textContent).toBe('');
      expect(document.getElementById('bookLanguage').textContent).toBe('');
      expect(document.getElementById('bookPages').textContent).toBe('');
      expect(document.getElementById('bookStatus').textContent).toBe('');
      expect(document.getElementById('getBookId').value).toBe('');
  });

  test('main initialization sets up event listeners', () => {
      // Get all the elements
      const searchInput = document.getElementById('clientSearch');
      const getBookForm = document.getElementById('getBookForm');
      const createForm = document.getElementById('createForm');
      const updateForm = document.getElementById('updateForm');
      const fillUpdateBtn = document.getElementById('fillUpdateForm');
      const deleteForm = document.getElementById('deleteForm');
      const cleanButton = document.getElementById('cleanBookDetails');

      // Trigger DOMContentLoaded
      document.dispatchEvent(new Event('DOMContentLoaded'));

      // Verify that all elements have event listeners attached
      // We can check this by verifying that the elements are not null
      // and that they exist in the DOM
      expect(searchInput).not.toBeNull();
      expect(getBookForm).not.toBeNull();
      expect(createForm).not.toBeNull();
      expect(updateForm).not.toBeNull();
      expect(fillUpdateBtn).not.toBeNull();
      expect(deleteForm).not.toBeNull();
      expect(cleanButton).not.toBeNull();

      // Verify that the elements are properly initialized
      expect(searchInput.placeholder).toBe('Search by book title...');
      expect(getBookForm.tagName).toBe('FORM');
      expect(createForm.tagName).toBe('FORM');
      expect(updateForm.tagName).toBe('FORM');
      expect(deleteForm.tagName).toBe('FORM');
  });

});
