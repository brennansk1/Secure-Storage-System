// static/js/scripts.js

// Auto-hide flash messages after 5 seconds
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000); // 5 seconds
});
