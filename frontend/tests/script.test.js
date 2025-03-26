const {
    initializeTableToggle,
    initializeSearchFunctionality,
    initializeBackendCheck
} = require('../app/static/app/js/script.js');

// Mock fetch globally
global.fetch = jest.fn();

describe('Book Management System Tests', () => {
    // Clear all mocks before each test
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
        <button id="backendCheckBtn">Check Backend</button>
      `;

      // Initialize all functionality
      const table = document.querySelector('.client-table');
      const searchContainer = document.querySelector('.search-container');
      const toggleBtn = document.querySelector('.toggle-table-btn');
      const updateBtn = document.querySelector('.update-table-btn');
      const searchInput = document.getElementById('clientSearch');
      const backendCheckBtn = document.getElementById('backendCheckBtn');

      // Mock drawTable function
      const mockDrawTable = jest.fn();
      initializeTableToggle(table, searchContainer, updateBtn, toggleBtn, mockDrawTable);
      initializeSearchFunctionality(searchInput);
      initializeBackendCheck(backendCheckBtn);

      // Initialize form event listeners
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
        });
      });
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
  });
