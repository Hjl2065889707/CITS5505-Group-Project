function createMarkerIcon(count, isActive = false) {
  const content = count > 1
    ? `<span class="marker-count">${count}</span>`
    : `<span class="marker-symbol"><i class="fa-solid fa-fish"></i></span>`;

  return L.divIcon({
    className: "custom-marker",
    html: `
      <div class="marker-pin ${isActive ? "marker-pin--active" : ""}">
        ${content}
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 38]
  });
}

// Group Rendering
export function renderMarkers(layer, groups, onMarkerClick, selectedPostId = null) {
  groups.forEach(group => {
    const { latitude, longitude } = group[0];
    const isActive = selectedPostId !== null && group.some(post => String(post.id) === String(selectedPostId));

    const marker = L.marker([latitude, longitude], {
      icon: createMarkerIcon(group.length, isActive)
    });

    marker.on("click", (e) => {
      L.DomEvent.stopPropagation(e);
      onMarkerClick(group);
    });

    layer.addLayer(marker);
  });
}