const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");

let uploadedImages = []; // base64 strings
let selectedLatitude = null;
let selectedLongitude = null;
const MAX_IMAGE_BYTES = 2 * 1024 * 1024;
const MAX_TOTAL_IMAGE_CHARS = 10 * 1024 * 1024;

function initLocationMap() {
  const mapEl = document.getElementById("locationMap");
  if (!mapEl || typeof L === "undefined") return;

  const coordinatesEl = document.getElementById("selectedCoordinates");
  const locationInput = document.getElementById("postLocation");
  const map = L.map(mapEl).setView([-31.9523, 115.8613], 12);
  let marker = null;

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19
  }).addTo(map);

  map.on("click", (event) => {
    selectedLatitude = Number(event.latlng.lat.toFixed(6));
    selectedLongitude = Number(event.latlng.lng.toFixed(6));

    if (marker) {
      marker.setLatLng(event.latlng);
    } else {
      marker = L.marker(event.latlng).addTo(map);
    }

    coordinatesEl.textContent = `${selectedLatitude}, ${selectedLongitude}`;

    if (!locationInput.value.trim()) {
      locationInput.value = `Map point (${selectedLatitude}, ${selectedLongitude})`;
    }
  });
}

initLocationMap();

/* Image upload preview */
imageInput.addEventListener("change", () => {
  imagePreview.innerHTML = "";
  uploadedImages = [];

  const files = Array.from(imageInput.files);
  if (files.length === 0) {
    imagePreview.innerHTML = "<div class='preview-box'>Preview</div>";
    return;
  }

  files.forEach(file => {
    if (file.size > MAX_IMAGE_BYTES) {
      alert(`${file.name} is too large. Please choose images under 2MB.`);
      return;
    }

    const reader = new FileReader();
    reader.onload = e => {
      const imageData = e.target.result;
      const nextTotalSize = uploadedImages.join("").length + imageData.length;

      if (nextTotalSize > MAX_TOTAL_IMAGE_CHARS) {
        alert("Selected images are too large to save. Please remove some images.");
        return;
      }

      uploadedImages.push(imageData);

      const img = document.createElement("img");
      img.src = imageData;
      img.className = "preview-img";
      imagePreview.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});

/* Submit post */
document.querySelector(".post-btn").addEventListener("click", async () => {
  const submitButton = document.querySelector(".post-btn");
  const content = document.querySelector(".post-text").value.trim();
  const locationName = document.querySelector(".location-input").value.trim();
  const category = document.querySelector(".category-select").value;
  const species = document.getElementById("postSpecies").value.trim();
  const weightValue = document.getElementById("postWeight").value;
  const bait = document.getElementById("postBait").value.trim();
  const weightKg = weightValue ? Number(weightValue) : null;

  if (!content) {
    alert("Please write something before posting.");
    return;
  }

  if (!category || category === "Select Category") {
    alert("Please select a category.");
    return;
  }

  if (weightKg !== null && (Number.isNaN(weightKg) || weightKg < 0)) {
    alert("Please enter a valid weight.");
    return;
  }

  const postData = {
    content,
    photos: uploadedImages,
    category,
    species: species || null,
    weightKg,
    bait: bait || null,
    locationName: locationName || null,
    latitude: selectedLatitude,
    longitude: selectedLongitude
  };

  submitButton.disabled = true;
  submitButton.textContent = "Posting...";

  try {
    const response = await fetch("/api/posts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(postData)
    });

    const result = await response.json().catch(() => ({}));

    if (!response.ok) {
      alert(result.error || "Unable to submit this post. Please try again.");
      return;
    }

    alert("Post submitted!");
    location.href = submitButton.dataset.feedUrl || "/";
  } catch (err) {
    console.error("Failed to submit post:", err);
    alert("Unable to submit this post. Please try again.");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Post";
  }
});
