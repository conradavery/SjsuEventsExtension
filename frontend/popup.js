document.addEventListener('DOMContentLoaded', () => {
    const eventsContainer = document.getElementById('events');
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    // Fetch events from the Python backend
    fetch('http://127.0.0.1:5000/api/events')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            loading.style.display = 'none';
            if (data.status === 'success') {
                const events = data.events;
                if (events.length === 0) {
                    eventsContainer.innerHTML = '<p>No events for today.</p>';
                    return;
                }
                events.forEach(event => {
                    const eventDiv = document.createElement('div');
                    eventDiv.className = 'event';

                    const title = document.createElement('div');
                    title.className = 'event-title';
                    title.textContent = event.title;
                    eventDiv.appendChild(title);

                    const details = document.createElement('div');
                    details.className = 'event-details';
                    details.innerHTML = `
                        <p><strong>Date:</strong> ${event.date}</p>
                        <p><strong>Category:</strong> ${event.category}</p>
                        <p><strong><i class="fa-solid fa-location-dot"></i> Location:</strong> ${event.location}</p>
                    `;
                    eventDiv.appendChild(details);

                    const link = document.createElement('div');
                    link.className = 'event-link';
                    if (event.link !== "No Link") {
                        const anchor = document.createElement('a');
                        anchor.href = event.link;
                        anchor.textContent = 'View Details';
                        anchor.target = '_blank';
                        link.appendChild(anchor);
                    } else {
                        link.textContent = 'No Link Available';
                    }
                    eventDiv.appendChild(link);

                    eventsContainer.appendChild(eventDiv);
                });
            } else {
                errorDiv.style.display = 'block';
                errorDiv.textContent = `Error: ${data.message}`;
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            errorDiv.style.display = 'block';
            errorDiv.textContent = `Error fetching events: ${error.message}`;
            console.error('Error:', error);
        });
});
