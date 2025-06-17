document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map centered around Nagpur (as a starting point) with an appropriate zoom level
    var map = L.map('mapContainer').setView([21.1458, 79.0882], 8);
    
    // Load and display tile layer from OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    
    // Define an array of locations with their coordinates and names
    var locations = [
        { name: "Nagpur", coords: [21.1458, 79.0882] },
        { name: "Bhandara", coords: [21.2123, 79.6393] },
        { name: "Amravati", coords: [20.9333, 77.75] },
        { name: "Wardha", coords: [20.7455, 78.6073] },
        { name: "chandigarh", coords: [30.7333, 76.7794] },
    ];
    
    // Add a marker for each location
    locations.forEach(function(location) {
        L.marker(location.coords).addTo(map)
            .bindPopup("<b>" + location.name + "</b>");
    });
});
