function createMarkerIcon(count) {
  return L.divIcon({
    className: "custom-marker",
    html: `
      <div class="marker-pin">
        ${count > 1 ? `<span class="marker-count">${count}</span>` : ""}
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 38]
  });
}

// Group Rendering
export function renderMarkers(layer, groups, onMarkerClick) {
  groups.forEach(group => {
    const { latitude, longitude } = group[0].catchDetails.location;

    const marker = L.marker([latitude, longitude], {
      icon: createMarkerIcon(group.length)
    });

    marker.on("click", (e) => {
      L.DomEvent.stopPropagation(e);
      onMarkerClick(group);
    });

    layer.addLayer(marker);
  });
}