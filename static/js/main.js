// Add any client-side functionality here
document.addEventListener('DOMContentLoaded', function() {
    // Flash messages auto-hide after 3 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 3000);
    });
});