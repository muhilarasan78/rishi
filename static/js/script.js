const stateDistricts = {
    "Andhra Pradesh": ["Visakhapatnam", "Kadapa", "Kurnool", "Chittoor", "Anantapur"],
    "Arunachal Pradesh": ["Tawang", "West Kameng", "Itanagar"],
    "Assam": ["Golaghat", "Kamrup", "Jorhat", "Dibrugarh"],
    "Bihar": ["Gaya", "Patna", "Nalanda", "Vaishali"],
    "Chhattisgarh": ["Bastar", "Raipur", "Bilaspur"],
    "Goa": ["North Goa", "South Goa"],
    "Gujarat": ["Kutch", "Ahmedabad", "Junagadh", "Surat"],
    "Haryana": ["Kurukshetra", "Gurugram", "Ambala"],
    "Himachal Pradesh": ["Shimla", "Kullu", "Kangra", "Lahaul and Spiti"],
    "Jharkhand": ["Latehar", "Ranchi", "East Singhbhum", "Deoghar"],
    "Karnataka": ["Kodagu", "Vijayanagara", "Uttara Kannada", "Chikkamagaluru", "Chamarajanagar", "Bengaluru", "Mysore"],
    "Kerala": ["Idukki", "Alappuzha", "Wayanad", "Thiruvananthapuram", "Thrissur", "Ernakulam", "Kottayam"],
    "Madhya Pradesh": ["Chhatarpur", "Indore", "Bhopal", "Gwalior", "Jabalpur"],
    "Maharashtra": ["Pune", "Mumbai City", "Aurangabad", "Nashik", "Ratnagiri", "Nagpur"],
    "Manipur": ["Imphal West", "Bishnupur", "Churachandpur"],
    "Meghalaya": ["East Khasi Hills", "West Jaintia Hills", "Ri-Bhoi"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
    "Odisha": ["Puri", "Khordha", "Ganjam", "Cuttack"],
    "Punjab": ["Amritsar", "Ludhiana", "Patiala", "Jalandhar"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jaisalmer", "Jodhpur", "Ajmer"],
    "Sikkim": ["East Sikkim", "North Sikkim", "West Sikkim"],
    "Tamil Nadu": ["Nilgiris", "Dindigul", "Chengalpattu", "Salem", "Chennai", "Madurai", "Coimbatore"],
    "Telangana": ["Hyderabad", "Vikarabad", "Mulugu", "Warangal"],
    "Tripura": ["West Tripura", "South Tripura", "Dhalai"],
    "Uttar Pradesh": ["Agra", "Lucknow", "Varanasi", "Prayagraj", "Mathura"],
    "Uttarakhand": ["Nainital", "Dehradun", "Rishikesh", "Almora", "Haridwar"],
    "West Bengal": ["Darjeeling", "Kolkata", "Kalimpong", "South 24 Parganas", "Shantiniketan"]
};

function initStates() {
    const stateSelect = document.getElementById('state');
    if (!stateSelect) return;
    stateSelect.innerHTML = '<option value="All">All Over India</option>';
    Object.keys(stateDistricts).sort().forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        stateSelect.appendChild(option);
    });
}

function updateDistricts() {
    const stateSelect = document.getElementById('state');
    const districtSelect = document.getElementById('district');
    if (!stateSelect || !districtSelect) return;

    const selectedState = stateSelect.value;
    districtSelect.innerHTML = '<option value="All">All Districts</option>';

    if (selectedState !== 'All' && stateDistricts[selectedState]) {
        stateDistricts[selectedState].sort().forEach(dist => {
            const option = document.createElement('option');
            option.value = dist;
            option.textContent = dist;
            districtSelect.appendChild(option);
        });
    }
}

// Helper to set interest from category buttons
function setInterest(interest) {
    const interestInput = document.getElementById('interests');
    interestInput.value = interest === 'All' ? 'Travel' : interest;
    document.getElementById('planner').scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', initStates);

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
        state: document.getElementById('state').value,
        district: document.getElementById('district').value,
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

        // Use Dynamic API Images (Unsplash)
        // Fallback to legacy Image or placeholder
        let imgSrc = "https://via.placeholder.com/800x500?text=No+Image";
        if (place.images && place.images.length > 0) {
            imgSrc = place.images[0];
        } else if (place.Image && place.Image !== "https://via.placeholder.com/800x400?text=No+Image") {
            imgSrc = place.Image;
        }

        const tagsHtml = place.Tags ? place.Tags.split(',').map(tag => `<span class="tag-pill">${tag.trim()}</span>`).join('') : '';

        let itineraryHtml = '';
        if (place.Itinerary) {
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
                            <div style="margin-top:10px; padding:10px; background:#f1f5f9; border-radius:8px; font-weight:600; font-size: 0.85rem;">
                                <i class="fas fa-hotel"></i> Stay: ${day.Hotel}
                            </div>
                        </div>
                    </div>
                `;
            });
        }

        // Use Dynamic Map Link
        const mapLink = place.map ? place.map : (place.Map_Link || `https://www.google.com/maps/search/?api=1&query=${place.name || place.Place}`);

        // text content
        const displayName = place.name || place.Place;
        const description = place.about || place.Description || "Explore this amazing destination.";

        card.innerHTML = `
            <a href="/place/${displayName}" class="card-img-link" style="display: block; position: relative; overflow: hidden;">
                <div class="card-img">
                    <img src="${imgSrc}" alt="${displayName}" 
                        onerror="this.onerror=null; this.src='https://via.placeholder.com/800x500?text=Image+Load+Error'">
                    <div style="position: absolute; bottom: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; pointer-events: none;">
                        <i class="fas fa-images"></i> View Gallery
                    </div>
                </div>
            </a>
            <div class="card-body">
                <a href="/place/${displayName}" style="text-decoration: none; color: inherit;">
                    <h3 class="card-title hover-underline">${displayName}</h3>
                </a>
                <div class="tag-list">${tagsHtml}</div>
                <p class="card-desc">${description}</p>
                
                <div class="itinerary-section">
                    <h4><i class="fas fa-route"></i> Your Personalized Plan</h4>
                    ${itineraryHtml}
                </div>

                <!-- Review Section -->
                <div style="margin-top: 1rem; padding: 0.75rem; background: #fffbe6; border-left: 4px solid #f59e0b; border-radius: 4px;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.25rem;">
                        <span style="font-weight: 700; font-size: 0.9rem; margin-right: 0.5rem;">Traveler Review:</span>
                        <div style="color: #f59e0b; font-size: 0.8rem;">
                            ${getStarRating(place.Rating || 4.5)}
                        </div>
                    </div>
                    <p style="font-style: italic; font-size: 0.9rem; color: #4b5563;">"${place.Review || "A wonderful place to visit!"}"</p>
                </div>

                <div style="margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e2e8f0; padding-top: 1rem;">
                    <span style="font-weight: 800; color: var(--primary); font-size: 1.1rem;">₹${place.Price_Day}/day</span>
                    <a href="${mapLink}" target="_blank" style="color: var(--primary); text-decoration: none; font-weight: 700;">
                        <i class="fas fa-map-marked-alt"></i> Maps
                    </a>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

function getStarRating(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let html = '';
    for (let i = 0; i < fullStars; i++) {
        html += '<i class="fas fa-star"></i>';
    }
    if (hasHalfStar) {
        html += '<i class="fas fa-star-half-alt"></i>';
    }
    // Fill remaining with empty stars if needed? detailed usually just shows positive.
    return html;
}
