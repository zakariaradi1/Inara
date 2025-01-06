document.addEventListener('DOMContentLoaded', function() {
    const mode = localStorage.getItem('mode');
    if (mode === 'night') {
        enableNightMode();
    } else {
        enableLightMode();
    }

    // Add event listeners to buttons
    document.querySelector('.toggle-night-mode').addEventListener('click', enableNightMode);
    document.querySelector('.toggle-light-mode').addEventListener('click', enableLightMode);
});

function enableNightMode() {
    document.body.classList.add('night-mode');
    document.body.classList.remove('light-mode');
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.classList.add('night-mode');
        button.classList.remove('light-mode');
    });
    localStorage.setItem('mode', 'night');
}

function enableLightMode() {
    document.body.classList.add('light-mode');
    document.body.classList.remove('night-mode');
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.classList.add('light-mode');
        button.classList.remove('night-mode');
    });
    localStorage.setItem('mode', 'light');
}