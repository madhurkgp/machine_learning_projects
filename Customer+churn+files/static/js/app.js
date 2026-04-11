// Customer Churn Prediction App JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultCard = document.getElementById('resultCard');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    
    // Form validation
    const validators = {
        creditScore: (value) => {
            const num = parseInt(value);
            return num >= 300 && num <= 850;
        },
        age: (value) => {
            const num = parseInt(value);
            return num >= 18 && num <= 100;
        },
        tenure: (value) => {
            const num = parseInt(value);
            return num >= 0 && num <= 10;
        },
        balance: (value) => {
            const num = parseFloat(value);
            return num >= 0;
        },
        numProducts: (value) => {
            const num = parseInt(value);
            return num >= 1 && num <= 4;
        },
        estimatedSalary: (value) => {
            const num = parseFloat(value);
            return num >= 0;
        }
    };
    
    // Show error message
    function showError(message) {
        errorDiv.innerHTML = `
            <div class="alert alert-danger">
                <strong>Error:</strong> ${message}
            </div>
        `;
        errorDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
        resultCard.classList.remove('show');
    }
    
    // Clear error message
    function clearError() {
        errorDiv.style.display = 'none';
    }
    
    // Validate form
    function validateForm(formData) {
        const errors = [];
        
        if (!validators.creditScore(formData.credit_score)) {
            errors.push('Credit Score must be between 300 and 850');
        }
        
        if (!validators.age(formData.age)) {
            errors.push('Age must be between 18 and 100');
        }
        
        if (!validators.tenure(formData.tenure)) {
            errors.push('Tenure must be between 0 and 10 years');
        }
        
        if (!validators.balance(formData.balance)) {
            errors.push('Balance must be a positive number');
        }
        
        if (!validators.numProducts(formData.num_products)) {
            errors.push('Number of Products must be between 1 and 4');
        }
        
        if (!validators.estimatedSalary(formData.estimated_salary)) {
            errors.push('Estimated Salary must be a positive number');
        }
        
        return errors;
    }
    
    // Format currency
    function formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }
    
    // Get risk level color
    function getRiskLevelColor(riskLevel) {
        switch(riskLevel.toLowerCase()) {
            case 'low': return 'success';
            case 'medium': return 'warning';
            case 'high': return 'danger';
            default: return 'secondary';
        }
    }
    
    // Show prediction result
    function showResult(data) {
        clearError();
        loadingDiv.style.display = 'none';
        
        const riskColor = getRiskLevelColor(data.risk_level);
        
        resultCard.innerHTML = `
            <div class="result-header">
                <h2 class="result-title">${data.result_text}</h2>
                <span class="result-badge badge-${riskColor}">${data.risk_level} Risk</span>
            </div>
            
            <div class="result-details">
                <div class="detail-item">
                    <div class="detail-value">${data.confidence}%</div>
                    <div class="detail-label">Confidence</div>
                </div>
                <div class="detail-item">
                    <div class="detail-value">${data.probability_churn}%</div>
                    <div class="detail-label">Churn Probability</div>
                </div>
                <div class="detail-item">
                    <div class="detail-value">${data.probability_stay}%</div>
                    <div class="detail-label">Retention Probability</div>
                </div>
            </div>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.confidence}%"></div>
                </div>
                <div class="progress-label">
                    <span>Prediction Confidence</span>
                    <span>${data.confidence}%</span>
                </div>
            </div>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.probability_churn}%; background: linear-gradient(90deg, #ef4444, #dc2626);"></div>
                </div>
                <div class="progress-label">
                    <span>Churn Risk</span>
                    <span>${data.probability_churn}%</span>
                </div>
            </div>
        `;
        
        resultCard.classList.add('show');
        
        // Smooth scroll to result
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    // Handle form submission
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            clearError();
            
            // Get form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Convert checkbox values
            data.has_cr_card = formData.has('has_cr_card') ? 1 : 0;
            data.is_active_member = formData.has('is_active_member') ? 1 : 0;
            
            // Validate form
            const errors = validateForm(data);
            if (errors.length > 0) {
                showError(errors.join('<br>'));
                return;
            }
            
            // Show loading
            loadingDiv.style.display = 'block';
            resultCard.classList.remove('show');
            
            try {
                const response = await fetch('/predict/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showResult(result);
                } else {
                    showError(result.error || 'Prediction failed. Please try again.');
                }
            } catch (error) {
                showError('Network error. Please check your connection and try again.');
            }
        });
    }
    
    // Load sample data
    const sampleDataBtn = document.getElementById('loadSampleData');
    if (sampleDataBtn) {
        sampleDataBtn.addEventListener('click', async function() {
            try {
                const response = await fetch('/sample-data/');
                const data = await response.json();
                
                if (response.ok) {
                    // Fill form with sample data
                    document.getElementById('credit_score').value = data.credit_score;
                    document.getElementById('geography').value = data.geography;
                    document.getElementById('gender').value = data.gender;
                    document.getElementById('age').value = data.age;
                    document.getElementById('tenure').value = data.tenure;
                    document.getElementById('balance').value = data.balance;
                    document.getElementById('num_products').value = data.num_products;
                    document.getElementById('has_cr_card').checked = data.has_cr_card === 1;
                    document.getElementById('is_active_member').checked = data.is_active_member === 1;
                    document.getElementById('estimated_salary').value = data.estimated_salary;
                    
                    // Show success message
                    const successDiv = document.createElement('div');
                    successDiv.className = 'alert alert-success fade-in';
                    successDiv.innerHTML = '<strong>Success!</strong> Sample data loaded. You can now submit the form for prediction.';
                    
                    const formContainer = document.querySelector('.prediction-form');
                    formContainer.parentNode.insertBefore(successDiv, formContainer);
                    
                    // Remove success message after 3 seconds
                    setTimeout(() => {
                        successDiv.remove();
                    }, 3000);
                } else {
                    showError('Failed to load sample data.');
                }
            } catch (error) {
                showError('Network error while loading sample data.');
            }
        });
    }
    
    // Clear form
    const clearFormBtn = document.getElementById('clearForm');
    if (clearFormBtn) {
        clearFormBtn.addEventListener('click', function() {
            form.reset();
            clearError();
            resultCard.classList.remove('show');
            loadingDiv.style.display = 'none';
        });
    }
    
    // Real-time validation
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });
    
    // Validate individual field
    function validateField(field) {
        const fieldName = field.name;
        const value = field.value;
        
        field.classList.remove('error', 'success');
        
        if (validators[fieldName] && value) {
            if (validators[fieldName](value)) {
                field.classList.add('success');
                return true;
            } else {
                field.classList.add('error');
                return false;
            }
        }
        
        return true;
    }
    
    // Add CSS classes for validation states
    const style = document.createElement('style');
    style.textContent = `
        .form-input.success, .form-select.success {
            border-color: var(--success-color);
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
        }
        
        .form-input.error, .form-select.error {
            border-color: var(--danger-color);
            box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
        }
        
        .form-input.error:focus, .form-select.error:focus {
            border-color: var(--danger-color);
            box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
        }
    `;
    document.head.appendChild(style);
});

// Helper function to get CSRF token
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

// Add number formatting for currency inputs
document.addEventListener('DOMContentLoaded', function() {
    const balanceInput = document.getElementById('balance');
    const salaryInput = document.getElementById('estimated_salary');
    
    function formatNumberInput(input) {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value) && value > 0) {
                // Store the actual value
                this.dataset.actualValue = value;
                // Display formatted version (optional)
                // this.value = value.toLocaleString();
            }
        });
        
        input.addEventListener('focus', function() {
            // Restore actual value when editing
            if (this.dataset.actualValue) {
                this.value = this.dataset.actualValue;
            }
        });
    }
    
    if (balanceInput) formatNumberInput(balanceInput);
    if (salaryInput) formatNumberInput(salaryInput);
});
