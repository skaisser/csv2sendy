// Global variables
let processedData = null;
let columnConfig = [];
let tableData = [];
let dropZone = document.getElementById('dropZone');
let fileInput = document.getElementById('fileInput');
let loading = document.querySelector('.loading');

// Initialize drag and drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('active');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('active');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('active');
    const file = e.dataTransfer.files[0];
    if (file) {
        processFile(file);
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
});

// Process the uploaded file
function processFile(file) {
    if (!file.name.endsWith('.csv')) {
        alert('Please upload a CSV file');
        return;
    }

    // Set default tag value from filename
    const tagValue = file.name.replace('.csv', '');
    document.getElementById('tagValue').value = tagValue;

    loading.style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'  // Include cookies for session handling
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        tableData = data.data;
        initializeColumnConfig(data.headers);
        updateTable();
        document.getElementById('previewSection').style.display = 'block';
        loading.style.display = 'none';
    })
    .catch(error => {
        alert('Error processing file: ' + error.message);
        loading.style.display = 'none';
    });
}

// Initialize column configuration
function initializeColumnConfig(headers) {
    console.log('Initializing column config with headers:', headers);
    
    // Define preferred order and display names for Sendy.co
    const columnMappings = {
        'first_name': 'Name',
        'email': 'Email',
        'phone_number': 'Phone',
        'last_name': 'Last_name'
    };
    
    // Define default checked columns (all can be unchecked except email)
    const defaultCheckedColumns = ['first_name', 'email', 'phone_number', 'last_name'];
    const mandatoryColumns = ['email'];
    
    // Create column config
    columnConfig = headers.map((header, index) => ({
        originalName: header,
        displayName: columnMappings[header] || header,
        included: defaultCheckedColumns.includes(header) || header === 'email',
        order: index
    }));
    
    console.log('Column config created:', columnConfig);
    
    // Create column management UI
    const columnList = document.getElementById('columnList');
    columnList.innerHTML = '';
    
    columnConfig.forEach((config, index) => {
        const li = document.createElement('li');
        li.className = 'column-item glass-effect border border-white/20 p-4 rounded-xl flex items-center gap-4 cursor-move transition-all duration-300 hover:shadow-md';
        li.setAttribute('data-id', index);
        li.innerHTML = `
            <span class="handle cursor-move text-neutral/40 hover:text-neutral/60"><i class="bi bi-grip-vertical"></i></span>
            <input type="checkbox" class="rounded-lg border-gray-300 text-primary focus:ring-primary w-5 h-5" 
                   ${config.included ? 'checked' : ''} 
                   ${mandatoryColumns.includes(config.originalName) ? 'disabled' : ''}
                   onchange="updateColumnConfig(${index}, 'included', this.checked)">
            <input type="text" class="flex-1 rounded-xl border-gray-200 focus:border-primary focus:ring-primary glass-effect" 
                   value="${config.displayName}" 
                   onchange="updateColumnConfig(${index}, 'displayName', this.value)">
        `;
        columnList.appendChild(li);
    });

    // Initialize Sortable
    if (window.columnSortable) {
        window.columnSortable.destroy();
    }
    
    window.columnSortable = new Sortable(columnList, {
        animation: 150,
        handle: '.handle',
        ghostClass: 'opacity-50',
        onEnd: function(evt) {
            const items = Array.from(columnList.children);
            columnConfig = items.map((item, index) => {
                const originalIndex = parseInt(item.getAttribute('data-id'));
                const config = columnConfig[originalIndex];
                config.order = index;
                return config;
            });
            console.log('Updated column config:', columnConfig);
            updateTable();
        }
    });
    
    // Initial table update
    updateTable();
}

// Update column configuration
function updateColumnConfig(index, property, value) {
    columnConfig[index][property] = value;
    updateTable();
}

// Update table display
function updateTable() {
    console.log('Updating table with config:', columnConfig);
    const headers = document.getElementById('tableHeaders');
    const body = document.getElementById('tableBody');
    
    // Clear existing content
    headers.innerHTML = '';
    body.innerHTML = '';
    
    // Sort columns by order
    const sortedColumns = [...columnConfig].sort((a, b) => a.order - b.order);
    console.log('Sorted columns:', sortedColumns);
    
    // Add headers
    sortedColumns.forEach(config => {
        if (config.included) {
            const th = document.createElement('th');
            th.className = 'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider';
            th.textContent = config.displayName;
            headers.appendChild(th);
        }
    });
    
    // Add rows
    if (tableData && tableData.length > 0) {
        tableData.slice(0, 10).forEach(row => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-gray-50';
            
            sortedColumns.forEach(config => {
                if (config.included) {
                    const td = document.createElement('td');
                    td.className = 'px-6 py-4 whitespace-nowrap text-sm text-gray-900';
                    td.textContent = row[config.originalName] || '';
                    tr.appendChild(td);
                }
            });
            
            body.appendChild(tr);
        });
    }
}

// Initialize download button
document.getElementById('downloadButton').addEventListener('click', async () => {
    console.log('Download button clicked');
    
    try {
        // Show loading state
        const button = document.getElementById('downloadButton');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-hourglass-split animate-spin mr-2"></i> Processing...';
        button.disabled = true;

        // Get form data
        const tagValue = document.getElementById('tagValue').value;
        const removeDuplicates = document.getElementById('removeDuplicates').checked;
        const removeEmpty = document.getElementById('removeEmpty').checked;

        // Get the sorted and filtered column configuration
        const sortedColumns = [...columnConfig].sort((a, b) => a.order - b.order)
            .filter(config => config.included)
            .map(config => ({
                originalName: config.originalName,
                displayName: config.displayName
            }));

        console.log('Sending download request with columns:', sortedColumns);

        const formData = new FormData();
        formData.append('columns', JSON.stringify(sortedColumns));
        formData.append('tag', tagValue);
        formData.append('remove_duplicates', removeDuplicates);
        formData.append('remove_empty', removeEmpty);

        const response = await fetch('/download', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Download failed');
        }

        // Create a blob from the response and trigger download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'processed.csv';
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Reset button
        button.innerHTML = originalText;
        button.disabled = false;
        
    } catch (error) {
        console.error('Download error:', error);
        alert('Error downloading file: ' + error.message);
        
        // Reset button on error
        const button = document.getElementById('downloadButton');
        button.innerHTML = '<i class="bi bi-download mr-2"></i> Download Processed File';
        button.disabled = false;
    }
});

// Download processed file
async function downloadProcessedFile() {
    const downloadUrl = document.getElementById('downloadLink').href;
    try {
        const response = await fetch(downloadUrl);
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to download file');
        }
        
        // Get filename from Content-Disposition header or use a default
        const contentDisposition = response.headers.get('Content-Disposition');
        const filename = contentDisposition
            ? contentDisposition.split('filename=')[1].replace(/['"]/g, '')
            : 'processed.csv';
            
        // Create blob from response
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        
        // Create temporary link and click it
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        showError('Error downloading file: ' + error.message);
    }
}

// Filter handlers
document.getElementById('removeDuplicates').addEventListener('change', updateTable);
document.getElementById('removeEmpty').addEventListener('change', updateTable);
