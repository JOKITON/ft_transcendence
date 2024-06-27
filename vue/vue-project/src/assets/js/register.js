document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        const result = await response.json();
        const messages = document.getElementById('messages');
        messages.innerHTML = '';
        if (response.ok) {
            messages.innerHTML = `<p>${result.message}</p>`;
            form.reset();
        } else {
            Object.entries(result.errors).forEach(([field, errors]) => {
                errors.forEach(error => {
                    messages.innerHTML += `<p>${error}</p>`;
                });
            });
        }
    });
});
