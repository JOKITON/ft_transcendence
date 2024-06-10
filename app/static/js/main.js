document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    const links = document.querySelectorAll('[data-link]');
    const cache = {};

    const loadCSS = () => {
        const existingLink = document.getElementById('page-css');
        if (existingLink) {
            existingLink.parentNode.removeChild(existingLink);
        }
        const link = document.createElement('link');
        link.id = 'page-css';
        link.rel = 'stylesheet';
        link.href = `css/styles.css`;
        document.head.appendChild(link);
    };

    const navigate = async (page) => {
        if (cache[page]) {
            app.innerHTML = cache[page];
            loadCSS();
        } else {
            try {
                const response = await fetch(`pages/${page}.html`);
                const html = await response.text();
                cache[page] = html;
                app.innerHTML = html;
                loadCSS();
            } catch (error) {
                app.innerHTML = '<h1>Page not found</h1>';
            }
        }
    };

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const page = event.target.getAttribute('href');
            navigate(page);
            history.pushState(null, '', page);
        });

        link.addEventListener('mouseover', (event) => {
            const page = event.target.getAttribute('href');
            if (!cache[page]) {
                fetch(`pages/${page}.html`)
                    .then(response => response.text())
                    .then(html => {
                        cache[page] = html;
                    });
            }
        });
    });

    window.addEventListener('popstate', () => {
        const path = location.pathname.substring(1);
        navigate(path || 'home');
    });

    navigate('home');
});
