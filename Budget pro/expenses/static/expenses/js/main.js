// Toggle password visibility function
// Toggles the visibility of a password field between text and password types
// @param {string} fieldId - The ID of the password field to toggle
// @param {string} buttonId - The ID of the button that triggers the toggle
function togglePasswordVisibility(fieldId, buttonId) {
    const passwordField = document.getElementById(fieldId);
    const toggleButton = document.getElementById(buttonId);
    
    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleButton.textContent = "Hide";
    } else {
        passwordField.type = "password";
        toggleButton.textContent = "Show";
    }
}

// Confirm deletion function
// Shows a confirmation dialog before deleting an item
// @param {string} message - Custom confirmation message (optional)
// @returns {boolean} - True if user confirms, false otherwise
function confirmDelete(message) {
    return confirm(message || "Are you sure you want to delete this item?");
}

// Initialize tooltips and apply category colors when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Apply category colors from data attributes to elements
    var categoryElements = document.querySelectorAll('.category-color');
    categoryElements.forEach(function(element) {
        var color = element.getAttribute('data-category-color');
        if (color) {
            element.style.backgroundColor = color;
        }
    });
});

// Form validation function
// Adds client-side form validation to forms with the 'needs-validation' class
(function() {
    'use strict';
    window.addEventListener('load', function() {
        var forms = document.getElementsByClassName('needs-validation');
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

// Chart initialization function
// Placeholder function for initializing charts if needed
// Currently, charts are initialized directly in the template
function initializeCharts() {
    // This function can be used to initialize charts if needed
    // Currently, charts are initialized directly in the template
}