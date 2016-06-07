var homemap = L.map('cartoterra-home-map-id', { zoomControl: false }).setView([20, 0], 1);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors",
    minZoom: 1,
    maxZoom: 20
}).addTo(homemap);
