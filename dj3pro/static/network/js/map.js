const map = L.map('map').setView([43.31386963946401, 45.69987759512445], 13)
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  attribution:
    '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map)

// To add a marker on the map
// L.marker([43.3153684414614, 45.70811733876792])
//   .addTo(map)
//   .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
//   .openPopup()

// FeatureGroup is to store editable layers
const drawnItems = new L.FeatureGroup()
map.addLayer(drawnItems)
const drawControl = new L.Control.Draw({
  edit: {
    featureGroup: drawnItems,
  },
})
map.addControl(drawControl)

// just to start draw on the map
// ===============================
// map.on('draw:created', (e) => {
//   const type = e.layerType,
//     layer = e.layer
//   drawnItems.addLayer(layer)
//   // =============================
// })

map.on('draw:created', (e) => {
  const layer = e.layer
  feature = layer.feature = layer.feature || {}

  feature.type = feature.type || 'Feature'
  const props = (feature.properties = feature.properties || {})
  drawnItems.addLayer(layer)
})
