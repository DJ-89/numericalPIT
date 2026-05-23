document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('richardsonForm');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error-message');
    const calculateBtn = document.querySelector('.btn-calculate');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        resultsDiv.style.display = 'none';
        errorDiv.style.display = 'none';
        
        const funcStr = document.getElementById('function').value.trim();
        const x = parseFloat(document.getElementById('x').value);
        const h = parseFloat(document.getElementById('h').value);
        const levels = parseInt(document.getElementById('levels').value);
        
        if (!funcStr) return showError('Please enter a function.');
        if (isNaN(x)) return showError('Please enter a valid number for x.');
        if (isNaN(h) || h <= 0) return showError('Step size must be a positive number.');
        if (isNaN(levels) || levels < 1 || levels > 10) return showError('Levels must be between 1 and 10.');
        
        const requestData = { function: funcStr, x: x, h: h, levels: levels };
        
        calculateBtn.classList.add('loading');
        calculateBtn.textContent = 'Calculating...';
        calculateBtn.disabled = true;
        
        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            if (!response.ok) throw new Error(data.error || 'An error occurred');
            
            displayResults(data);
        } catch (error) {
            showError(error.message);
        } finally {
            calculateBtn.classList.remove('loading');
            calculateBtn.textContent = 'Calculate';
            calculateBtn.disabled = false;
        }
    });
    
    function displayResults(data) {
        document.getElementById('res-function').textContent = data.function;
        document.getElementById('res-x').textContent = data.x;
        document.getElementById('res-h').textContent = data.h0;
        document.getElementById('res-best').textContent = data.best_estimate;
        
        const headerRow = document.getElementById('table-header');
        headerRow.innerHTML = '<th>h</th>';
        for (let i = 0; i < data.table[0].length; i++) {
            // FIXED: Using standard HTML sub tags instead of dynamic unicode escapes
            headerRow.innerHTML += `<th>D<sub>${i}</sub></th>`;
        }
        
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';
        
        let currentH = data.h0;
        for (let i = 0; i < data.table.length; i++) {
            const row = document.createElement('tr');
            
            const hCell = document.createElement('td');
            hCell.textContent = currentH.toPrecision(4);
            row.appendChild(hCell);
            
            for (let j = 0; j < data.table[i].length; j++) {
                const cell = document.createElement('td');
                cell.textContent = data.table[i][j];
                row.appendChild(cell);
            }
            
            tableBody.appendChild(row);
            currentH /= 2;
        }
        
        const diagonalList = document.getElementById('diagonal-list');
        diagonalList.innerHTML = '';
        data.diagonal.forEach((val, idx) => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>D<sub>${idx}</sub></strong> = ${val}`;
            diagonalList.appendChild(li);
        });
        
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
        
        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
});