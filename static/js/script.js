// Helper to set interest from category buttons
function setInterest(interest) {
    const interestInput = document.getElementById('interests');
    interestInput.value = interest === 'All' ? 'Travel' : interest;
    document.getElementById('planner').scrollIntoView({ behavior: 'smooth' });
}

document.getElementById('tripForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const plannerResults = document.getElementById('results');
    const container = document.getElementById('recommendations-container');
    const submitBtn = document.querySelector('.submit-btn');
    const originalText = submitBtn.innerHTML;

    // Show loading state
    submitBtn.innerHTML = 'Planning your trip... <i class="fas fa-spinner fa-spin"></i>';
    submitBtn.disabled = true;

    const formData = {
        budget: document.getElementById('budget').value,
        place: document.getElementById('place').value,
        days: document.getElementById('days').value,
        interests: document.getElementById('interests').value
    };

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        plannerResults.classList.remove('hidden');
        renderResults(data);
        plannerResults.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

function renderResults(data) {
    const container = document.getElementById('recommendations-container');
    container.innerHTML = '';

    if (data.length === 0) {
        container.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
                <p>No matching destinations found. Try broadening your criteria.</p>
            </div>
        `;
        return;
    }

    data.forEach((place, index) => {
        const card = document.createElement('div');
        card.className = 'destination-card';

        const dynamicImg = `https://source.unsplash.com/featured/800x600?${place.Place.split(' ')[0].toLowerCase()},travel&sig=${index}`;
        const tagsHtml = place.Tags.split(',').map(tag => `<span class="tag-pill">${tag.trim()}</span>`).join('');

        let itineraryHtml = '';
        place.Itinerary.forEach((day, dIdx) => {
            itineraryHtml += `
                <div class="day-item ${dIdx === 0 ? 'active' : ''}">
                    <div class="day-header" onclick="this.parentElement.classList.toggle('active')">
                        <span>Day ${day.Day}: Overview</span>
                        <i class="fas fa-chevron-down"></i>
                    </div>
                    <div class="day-body">
                        <p><strong>Morning:</strong> ${day.Morning}</p>
                        <p><strong>Afternoon:</strong> ${day.Afternoon}</p>
                        <p><strong>Evening:</strong> ${day.Evening}</p>
                        <p><strong>Night:</strong> ${day.Night}</p>
                        <div style="margin-top:10px; padding:10px; background:#f1f5f9; border-radius:8px; font-weight:600; font-size: 0.85rem;">
                            <i class="fas fa-hotel"></i> Stay: ${day.Hotel}
                        </div>
                    </div>
                </div>
            `;
        });

        card.innerHTML = `
            <div class="card-img">
                <img src="${dynamicImg}" alt="${place.Place}" onerror="this.src='https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=800&q=80'">
            </div>
            <div class="card-body">
                <h3 class="card-title">${place.Place}</h3>
                <div class="tag-list">${tagsHtml}</div>
                <p class="card-desc">${place.Description}</p>
                
                <div class="itinerary-section">
                    <h4><i class="fas fa-route"></i> Your Personalized Plan</h4>
                    ${itineraryHtml}
                </div>

                <div style="margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e2e8f0; padding-top: 1rem;">
                    <span style="font-weight: 800; color: var(--primary); font-size: 1.1rem;">₹${place.Price_Day}/day</span>
                    <a href="https://www.google.com/maps/search/?api=1&query=${place.Place}" target="_blank" style="color: var(--primary); text-decoration: none; font-weight: 700;">
                        <i class="fas fa-map-marked-alt"></i> Maps
                    </a>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}
