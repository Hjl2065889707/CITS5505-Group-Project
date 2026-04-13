const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");

let uploadedImages = []; // base64 strings

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
    const reader = new FileReader();
    reader.onload = e => {
      uploadedImages.push(e.target.result);

      const img = document.createElement("img");
      img.src = e.target.result;
      img.className = "preview-img";
      imagePreview.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});

/* Submit post */
document.querySelector(".post-btn").addEventListener("click", () => {
  const content = document.querySelector(".post-text").value.trim();
  const location = document.querySelector(".location-input").value.trim();
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
    content: content + (location ? `\n📍 ${location}` : ""),
    images: uploadedImages,
    likes: 0,
    comments: 0,
    tags: [category]
  };

  const existing = JSON.parse(localStorage.getItem("userPosts") || "[]");
  existing.unshift(newPost);
  localStorage.setItem("userPosts", JSON.stringify(existing));

  alert("Post submitted!");
  location.href = "../feed/feed.html";
});
