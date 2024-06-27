// Waits for the HTML document to be fully loaded and parsed
document.addEventListener("DOMContentLoaded", () => {
    const navigateTo = (url) => {
        if (!url) {
            url = "home"; // Default to "home" if the URL is empty
        }
        if (location.pathname !== `/${url}`) { // Checks if the new URL is different from current PATH
            history.pushState(null, null, url);
            loadContent(url); // Load content asociated with new URL
        }
    };

    const loadContent = async (url) => {
        try {
            // Ensure the URL path is correct
            const response = await fetch(`pages/${url}.html`);
            if (!response.ok) { // URL is incorrect
                throw new Error('Network response was not ok');
            }
            const content = await response.text();
            document.getElementById("app").innerHTML = content; // Update HTML with new content
            attachLinkHandlers();
        } catch (error) {
            console.error('Failed to load content:', error);
            document.getElementById("app").innerHTML = "<p>Error loading page.</p>";
        }
    };

    const attachLinkHandlers = () => {
        document.querySelectorAll('[data-link]').forEach(link => { // Handles click event handlers
            link.removeEventListener('click', linkHandler); // Prevent multiple event listeners
            link.addEventListener('click', linkHandler);
        });
    };

    const linkHandler = (e) => { // Prevents default behaviour (reload page)
        e.preventDefault();
        const url = e.target.getAttribute('data-link');
        navigateTo(url);
    };

    window.onpopstate = () => {
        loadContent(location.pathname.slice(1) || "home");
    };

    // Initial load
    loadContent(location.pathname.slice(1) || "home");
    attachLinkHandlers();
});
