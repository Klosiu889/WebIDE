let darkMode = localStorage.getItem('darkMode');
const darkModeToggle = document.querySelector('#dark-mode-toggle');

const enableDarkMode = () => {
    document.body.classList.add('darkmode');
    localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
    document.body.classList.remove('darkmode');
    localStorage.setItem('darkMode', null);
}

if (darkMode === 'enabled') {
    enableDarkMode();
    if (darkModeToggle.classList.contains('bi-moon')) {
        darkModeToggle.classList.remove('bi-moon');
    }
}
else {
    if (!darkModeToggle.classList.contains('bi-moon')) {
        darkModeToggle.classList.add('bi-moon');
    }
}

darkModeToggle.addEventListener('click', () => {
    darkMode = localStorage.getItem('darkMode');
    darkModeToggle.classList.toggle('bi-moon')
    if (darkMode !== 'enabled') enableDarkMode();
    else disableDarkMode();
});

const tabsButtons = document.querySelectorAll('.tabs-button');

tabsButtons.forEach(tabButton =>
    tabButton.addEventListener("click", () => {
        tabsButtons.forEach(tabButton => tabButton.classList.remove("active"));
        tabButton.classList.toggle("active");
}));
