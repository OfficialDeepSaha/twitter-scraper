// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the search type select element
    const searchTypeSelect = document.getElementById('search_type');
    const queryInput = document.getElementById('query');
    const queryHelp = document.getElementById('query_help');
    
    // Update placeholder and help text based on search type
    if (searchTypeSelect) {
        searchTypeSelect.addEventListener('change', function() {
            updateQueryPlaceholder();
        });
        
        // Set initial placeholder
        updateQueryPlaceholder();
    }
    
    function updateQueryPlaceholder() {
        const searchType = searchTypeSelect.value;
        
        if (searchType === 'keyword') {
            queryInput.placeholder = 'Enter keyword (e.g., climate change)';
            queryHelp.textContent = 'Enter any word or phrase to search for in tweets.';
        } else if (searchType === 'hashtag') {
            queryInput.placeholder = 'Enter hashtag (e.g., climate or #climate)';
            queryHelp.textContent = 'For hashtags, the # symbol is optional.';
        } else if (searchType === 'user') {
            queryInput.placeholder = 'Enter username (e.g., elonmusk or @elonmusk)';
            queryHelp.textContent = 'For users, the @ symbol is optional.';
        }
    }
    
    // Add date validation for the date range
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (startDateInput && endDateInput) {
        endDateInput.addEventListener('change', function() {
            // If end date is before start date, clear end date
            if (startDateInput.value && endDateInput.value) {
                const startDate = new Date(startDateInput.value);
                const endDate = new Date(endDateInput.value);
                
                if (endDate < startDate) {
                    alert('End date cannot be before start date.');
                    endDateInput.value = '';
                }
            }
        });
        
        startDateInput.addEventListener('change', function() {
            // If start date is after end date, clear end date
            if (startDateInput.value && endDateInput.value) {
                const startDate = new Date(startDateInput.value);
                const endDate = new Date(endDateInput.value);
                
                if (endDate < startDate) {
                    endDateInput.value = '';
                }
            }
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
});
