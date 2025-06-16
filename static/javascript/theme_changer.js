document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("theme-toggle");
    const htmlEl = document.documentElement;

    let currentTheme = '';
    const themeFromStorage = localStorage.getItem("theme");

    if (!themeFromStorage) {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        currentTheme = prefersDark ? "dark" : "light";
        localStorage.setItem("theme", currentTheme);
    } else {
        currentTheme = themeFromStorage;
    }

    htmlEl.setAttribute("data-bs-theme", currentTheme);
    updateButtonIcon(currentTheme);

    toggleBtn.addEventListener("click", () => {
        currentTheme = (currentTheme === "light") ? "dark" : "light";
        htmlEl.setAttribute("data-bs-theme", currentTheme);
        localStorage.setItem("theme", currentTheme);
        updateButtonIcon(currentTheme);
    });

    function updateButtonIcon(theme) {
        toggleBtn.innerText = (theme === "light") ? "🌙" : "☀️";
    }
});