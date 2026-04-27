const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");

let uploadedImages = []; // base64 strings
const MAX_IMAGE_BYTES = 500 * 1024;
const MAX_TOTAL_IMAGE_CHARS = 2 * 1024 * 1024;

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
      alert(`${file.name} is too large. Please choose images under 500KB.`);
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
document.querySelector(".post-btn").addEventListener("click", () => {
  const content = document.querySelector(".post-text").value.trim();
  const postLocation = document.querySelector(".location-input").value.trim();
  const category = document.querySelector(".category-select").value;

  if (!content) {
    alert("Please write something before posting.");
    return;
  }

  if (!category || category === "Select Category") {
    alert("Please select a category.");
    return;
  }

  const newPost = {
    id: Date.now(),
    username: "You",
    avatar: "https://i.pravatar.cc/150?img=10",
    time: "Just now",
    content: content + (postLocation ? `\n📍 ${postLocation}` : ""),
    images: uploadedImages,
    likes: 0,
    comments: 0,
    tags: [category]
  };

  const existing = JSON.parse(localStorage.getItem("userPosts") || "[]");
  existing.unshift(newPost);

  try {
    localStorage.setItem("userPosts", JSON.stringify(existing));
  } catch (err) {
    console.error("Failed to save post:", err);
    alert("Unable to save this post. Please use smaller images or remove some images.");
    return;
  }

  alert("Post submitted!");
  location.href = "../feed/feed.html";
});
