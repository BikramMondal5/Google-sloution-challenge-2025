document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    
    if (form) {
        // Form validation
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const temperature = parseFloat(document.getElementById('temperature').value);
            const rainfall = parseFloat(document.getElementById('rainfall').value);
            
            if (temperature < 0 || temperature > 50) {
                alert('Temperature must be between 0°C and 50°C');
                return;
            }
            
            if (rainfall < 0 || rainfall > 1000) {
                alert('Rainfall must be between 0mm and 1000mm');
                return;
            }
            
            // Add loading state
            form.classList.add('loading');
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
            
            // Submit the form
            form.submit();
        });
        
        // Add tooltips to form fields
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // Initialize any Bootstrap components
        const toastElList = [].slice.call(document.querySelectorAll('.toast'));
        toastElList.map(function (toastEl) {
            return new bootstrap.Toast(toastEl);
        });
    }
});
