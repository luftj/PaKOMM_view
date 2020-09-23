var mymap = L.map('mapid').setView([53.565, 10.0], 13);

L.tileLayer('http://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'osm',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);


L.geoJSON(gebiet).addTo(mymap);


function onMapClick(e) {
    console.log("click at " + e.latlng);
}

mymap.on('click', onMapClick);
var dataLayerGroup = new L.LayerGroup().addTo(mymap);

// var geojsonMarkerOptions = {
//     radius: 8,
//     fillColor: "#ff7800",
//     color: "#000",
//     weight: 1,
//     opacity: 1,
//     fillOpacity: 0.8
// };

function onEachFeature(feature, layer) {
    if (feature.properties) {
        layer.bindPopup("<b>added in VR:</b><br>"+Object.entries(feature.properties).join("<br>"));
    }
}

function replaceLayer(json) {
    dataLayerGroup.clearLayers();
    for(let i=0; i < json.features.length; ++i)
    {
        geojsonFeature = json.features[i]
        L.geoJSON(geojsonFeature,{
            //     pointToLayer: function (feature, latlng) {
            //         return L.circleMarker(latlng, geojsonMarkerOptions);
            //     }
            onEachFeature: onEachFeature
        }).addTo(dataLayerGroup);
    }
}

setInterval(function() {
    fetch("http://localhost:5000/get_geojson")
        .then(response => response.json())
        .then(json => replaceLayer(json))
}, 5000);