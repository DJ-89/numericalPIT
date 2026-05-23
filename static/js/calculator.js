/**
 * Richardson Extrapolation Calculator - Client-side JavaScript
 * Handles form submission, API communication, and result display
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('richardsonForm');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error-message');
    
    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Hide previous results and errors
        resultsDiv.style.display = 'none';
        errorDiv.style.display = 'none';
        
        // Get form values
        const funcStr = document.getElementById('function').value.trim();
        const x = parseFloat(document.getElementById('x').value);
        const h = parseFloat(document.getElementById('h').value);
        const levels = parseInt(document.getElementById('levels').value);
        
        // Basic validation
        if (!funcStr) {
            showError('Please enter a function.');
            return;
        }
        
        if (isNaN(x)) {
            showError('Please enter a valid number for x.');
            return;
        }
        
        if (isNaN(h) || h <= 0) {
            showError('Step size must be a positive number.');
            return;
        }
        
        if (isNaN(levels) || levels < 1 || levels > 10) {
            showError('Number of levels must be between 1 and 10.');
            return;
        }
        
        // Prepare request data
        const requestData = {
            function: funcStr,
            x: x,
            h: h,
            levels: levels
        };
        
        // Show loading state
        form.classList.add('loading');
        
        try {
            // Make API request
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'An error occurred');
            }
            
            // Display results
            displayResults(data);
            
        } catch (error) {
            showError(error.message);
        } finally {
            form.classList.remove('loading');
        }
    });
    
    /**
     * Display calculation results
     * @param {Object} data - Response data from the server
     */
    function displayResults(data) {
        // Update summary information
        document.getElementById('res-function').textContent = data.function;
        document.getElementById('res-x').textContent = data.x;
        document.getElementById('res-h').textContent = data.h0;
        document.getElementById('res-best').textContent = data.best_estimate;
        
        // Build table header based on number of levels
        const headerRow = document.getElementById('table-header');
        headerRow.innerHTML = '<th>h</th>';
        for (let i = 0; i < data.table[0].length; i++) {
            headerRow.innerHTML += `<th>D\u208${i}</th>`;
        }
        
        // Build table body
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';
        
        let currentH = data.h0;
        for (let i = 0; i < data.table.length; i++) {
            const row = document.createElement('tr');
            
            // Step size column
            const hCell = document.createElement('td');
            hCell.textContent = currentH.toPrecision(6);
            row.appendChild(hCell);
            
            // Data columns
            for (let j = 0; j < data.table[i].length; j++) {
                const cell = document.createElement('td');
                cell.textContent = data.table[i][j];
                row.appendChild(cell);
            }
            
            tableBody.appendChild(row);
            currentH /= 2;
        }
        
        // Display diagonal elements
        const diagonalList = document.getElementById('diagonal-list');
        diagonalList.innerHTML = '';
        data.diagonal.forEach((val, idx) => {
            const li = document.createElement('li');
            li.textContent = `D\u208${idx} = ${val}`;
            diagonalList.appendChild(li);
        });
        
        // Display errors
        const errorList = document.getElementById('error-list');
        errorList.innerHTML = '';
        if (data.errors && data.errors.length > 0) {
            data.errors.forEach((err, idx) => {
                const li = document.createElement('li');
                li.textContent = `Error (${idx + 1}): ${err}`;
                errorList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Not enough levels to calculate errors';
            errorList.appendChild(li);
        }
        
        // Show results container
        resultsDiv.style.display = 'block';
        
        // Scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    /**
     * Display error message
     * @param {string} message - Error message to display
     */
    function showError(message) {
        errorDiv.textContent = 'Error: ' + message;
        errorDiv.style.display = 'block';
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
