// Main JavaScript for Parkinson's Disease Prediction App

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    
    // Form submission handler
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    // Sample data buttons
    const sampleButtons = document.querySelectorAll('.sample-btn');
    sampleButtons.forEach(button => {
        button.addEventListener('click', loadSampleData);
    });
    
    // Clear form button
    const clearButton = document.getElementById('clearForm');
    if (clearButton) {
        clearButton.addEventListener('click', clearFormData);
    }
    
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        // Hide previous results and errors
        hideElement(resultDiv);
        hideElement(errorDiv);
        
        // Validate form
        if (!validateForm()) {
            return;
        }
        
        // Show loading
        showElement(loadingDiv);
        
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/predict/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams(data)
            });
            
            const result = await response.json();
            
            hideElement(loadingDiv);
            
            if (result.success) {
                displayResult(result);
            } else {
                displayError(result);
            }
            
        } catch (error) {
            hideElement(loadingDiv);
            displayError({ error: 'Network error. Please try again.' });
        }
    }
    
    function validateForm() {
        const inputs = form.querySelectorAll('.form-control');
        let isValid = true;
        
        inputs.forEach(input => {
            // Remove previous validation classes
            input.classList.remove('is-invalid');
            
            // Check if value is empty
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            }
            
            // Check if value is within valid range
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);
            const value = parseFloat(input.value);
            
            if (!isNaN(min) && value < min) {
                input.classList.add('is-invalid');
                isValid = false;
            }
            
            if (!isNaN(max) && value > max) {
                input.classList.add('is-invalid');
                isValid = false;
            }
        });
        
        if (!isValid) {
            displayError({ error: 'Please fill in all fields with valid values within the specified ranges.' });
        }
        
        return isValid;
    }
    
    function displayResult(result) {
        const resultClass = result.prediction === 1 ? 'result-danger' : 'result-success';
        const resultTitle = result.prediction_label;
        const confidence = result.confidence.toFixed(1);
        
        resultDiv.className = `result-section ${resultClass} fade-in`;
        resultDiv.innerHTML = `
            <div class="result-title">${resultTitle}</div>
            <div class="result-confidence">Confidence: ${confidence}%</div>
            <div class="probability-bars">
                <div class="probability-item">
                    <div class="probability-label">Healthy</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${result.probabilities.healthy}%"></div>
                    </div>
                    <div>${result.probabilities.healthy.toFixed(1)}%</div>
                </div>
                <div class="probability-item">
                    <div class="probability-label">Parkinson's</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${result.probabilities.parkinsons}%"></div>
                    </div>
                    <div>${result.probabilities.parkinsons.toFixed(1)}%</div>
                </div>
            </div>
            <div style="margin-top: 1.5rem;">
                <button class="btn btn-secondary" onclick="clearFormData()">Try Another Prediction</button>
            </div>
        `;
        
        showElement(resultDiv);
        
        // Scroll to result
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    function displayError(result) {
        let errorMessage = result.error || 'An unknown error occurred.';
        
        // Display field-specific errors if available
        if (result.errors) {
            errorMessage += '<ul>';
            for (const [field, errors] of Object.entries(result.errors)) {
                const fieldLabel = document.querySelector(`label[for="${field}"]`);
                const fieldName = fieldLabel ? fieldLabel.textContent : field;
                errorMessage += `<li><strong>${fieldName}:</strong> ${errors.join(', ')}</li>`;
                
                // Add validation classes to form fields
                const input = document.getElementById(field);
                if (input) {
                    input.classList.add('is-invalid');
                }
            }
            errorMessage += '</ul>';
        }
        
        errorDiv.innerHTML = `
            <div class="alert alert-danger">
                <strong>Error:</strong> ${errorMessage}
            </div>
        `;
        
        showElement(errorDiv);
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    async function loadSampleData(e) {
        const sampleType = e.target.dataset.sample;
        
        try {
            const response = await fetch('/sample-data/');
            const data = await response.json();
            
            if (data.samples && data.samples.length > 0) {
                const sample = data.samples.find(s => 
                    s.name.toLowerCase().includes(sampleType.toLowerCase())
                ) || data.samples[0];
                
                // Fill form with sample data
                Object.entries(sample.data).forEach(([field, value]) => {
                    const input = document.getElementById(field);
                    if (input) {
                        input.value = value;
                        input.classList.remove('is-invalid');
                    }
                });
                
                // Show success message
                showNotification(`Sample data loaded: ${sample.name}`, 'success');
                
                // Hide any previous results
                hideElement(resultDiv);
                hideElement(errorDiv);
            }
            
        } catch (error) {
            showNotification('Failed to load sample data', 'danger');
        }
    }
    
    function clearFormData() {
        if (form) {
            form.reset();
            
            // Remove validation classes
            const inputs = form.querySelectorAll('.form-control');
            inputs.forEach(input => {
                input.classList.remove('is-invalid');
            });
            
            // Hide results
            hideElement(resultDiv);
            hideElement(errorDiv);
            
            showNotification('Form cleared', 'info');
        }
    }
    
    function showElement(element) {
        if (element) {
            element.style.display = 'block';
        }
    }
    
    function hideElement(element) {
        if (element) {
            element.style.display = 'none';
        }
    }
    
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} fade-in`;
        notification.innerHTML = `
            <strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> ${message}
            <button type="button" class="close" onclick="this.parentElement.remove()" style="float: right; background: none; border: none; font-size: 1.2rem; cursor: pointer;">&times;</button>
        `;
        
        // Insert at the top of the main content
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.insertBefore(notification, mainContent.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 5000);
            
            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Add input formatting
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                // Format to appropriate decimal places
                const step = parseFloat(this.step) || 1;
                const decimalPlaces = step < 1 ? step.toString().split('.')[1].length : 0;
                this.value = value.toFixed(decimalPlaces);
            }
        });
        
        // Remove validation class on input
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
    
    // Add smooth scroll for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe all cards
    const cards = document.querySelectorAll('.card, .info-card');
    cards.forEach(card => {
        observer.observe(card);
    });
});

// Utility functions
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

function validateRange(value, min, max) {
    const num = parseFloat(value);
    return !isNaN(num) && num >= min && num <= max;
}
