document.addEventListener('DOMContentLoaded', () => {
    // Display version information
    document.getElementById('version-number').textContent = APP_VERSION_OBJ.version;
    document.getElementById('build-number').textContent = APP_VERSION_OBJ.build;

    // DOM Elements
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const cameraInput = document.getElementById('camera-input');
    const captureBtn = document.getElementById('capture-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const uploadForm = document.getElementById('upload-form');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const resultContainer = document.getElementById('result-container');
    const styleDescription = document.getElementById('style-description');
    const loadingContainer = document.getElementById('loading-container');

    // Check if device supports camera
    const supportsCamera = 'mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices;
    
    // Update capture button visibility based on device support
    if (!supportsCamera) {
        captureBtn.style.display = 'none';
    }

    // Handle capture button click
    captureBtn.addEventListener('click', () => {
        // Reset the camera input value to ensure it triggers the camera
        cameraInput.value = '';
        cameraInput.click();
    });

    // Handle camera input change
    cameraInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            handleFiles(this.files);
        }
    });

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('active');
    }

    function unhighlight() {
        dropArea.classList.remove('active');
    }

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // Handle selected files from file input
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                displayPreview(file);
                analyzeBtn.disabled = false;
            } else {
                alert('Please select an image file');
                resetForm();
            }
        }
    }

    function displayPreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get the file from either input
        const file = fileInput.files[0] || cameraInput.files[0];
        
        if (!file) {
            alert('Please select an image first');
            return;
        }

        // Show loading state
        loadingContainer.style.display = 'block';
        resultContainer.style.display = 'none';
        analyzeBtn.disabled = true;

        // Create form data
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Send request to backend
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }

            const data = await response.json();
            
            // Display results with structured format
            displayStyleResults(data);
            resultContainer.style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        } finally {
            // Hide loading state
            loadingContainer.style.display = 'none';
            analyzeBtn.disabled = false;
        }
    });

    function displayStyleResults(data) {
        // Clear previous content
        styleDescription.innerHTML = '';
        document.getElementById('color-grid').innerHTML = '';
        
        // Log received data
        console.log('Received data:', data);
        
        // Check if we have an error message
        if (data.style_title && data.style_title.includes('Error')) {
            styleDescription.innerHTML = `<p class="error-message">${data.style_description}</p>`;
            return;
        }
        
        // Create styled elements for the style title and description
        const titleElement = document.createElement('h3');
        titleElement.className = 'style-title';
        titleElement.textContent = data.style_title;
        
        const descriptionElement = document.createElement('p');
        descriptionElement.className = 'style-text';
        descriptionElement.textContent = data.style_description;
        
        // Add elements to the container
        styleDescription.appendChild(titleElement);
        styleDescription.appendChild(descriptionElement);

        // Display color palette if available
        console.log('Colors data:', data.colors);
        if (data.colors && data.colors.length > 0) {
            const colorGrid = document.getElementById('color-grid');
            console.log('Creating color grid with', data.colors.length, 'colors');
            data.colors.forEach(color => {
                console.log('Processing color:', color);
                const colorItem = document.createElement('div');
                colorItem.className = 'color-item';
                
                const colorSwatch = document.createElement('div');
                colorSwatch.className = 'color-swatch';
                colorSwatch.style.backgroundColor = color.hex;
                
                const colorInfo = document.createElement('div');
                colorInfo.className = 'color-info';
                
                const hexCode = document.createElement('div');
                hexCode.className = 'color-hex';
                hexCode.textContent = color.hex;
                
                const colorName = document.createElement('div');
                colorName.className = 'color-name';
                colorName.textContent = color.name;
                
                colorInfo.appendChild(hexCode);
                colorInfo.appendChild(colorName);
                colorItem.appendChild(colorSwatch);
                colorItem.appendChild(colorInfo);
                colorGrid.appendChild(colorItem);
            });
        } else {
            console.log('No colors data available');
        }
    }

    function resetForm() {
        uploadForm.reset();
        previewContainer.style.display = 'none';
        resultContainer.style.display = 'none';
        analyzeBtn.disabled = true;
    }
});
