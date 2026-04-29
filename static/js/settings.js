document.addEventListener('DOMContentLoaded', () => {
    // ---------------------------------------------------------
    // DOM Elements Selection
    // ---------------------------------------------------------
    const avatarInput = document.getElementById('avatarUpload');
    const avatarPreview = document.getElementById('avatarPreview');
    const saveBtn = document.querySelector('.save-btn');
    const logoutBtn = document.querySelector('.logout-btn');

    // ---------------------------------------------------------
    // Avatar Upload Logic
    // ---------------------------------------------------------
    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            
            if (file) {
                // Add an additional check to assure only image types are processed
                if (!file.type.startsWith('image/')) {
                    console.error('Error: Selected file is not an image.');
                    alert('Please select a valid image file (PNG, JPG, etc).');
                    return;
                }

                // Use FileReader to display the image locally for preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                    console.log('Success: Avatar image replaced in UI preview.');
                    
                    // TODO: Implement backend upload logic later
                    // 1. Create a FormData instance and append the 'file' object.
                    // 2. Fetch/POST to backend API (e.g., /api/user/avatar).
                    // 3. Handle loading state and gracefully handle upload failure.
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ---------------------------------------------------------
    // Save Changes Logic
    // ---------------------------------------------------------
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const username = document.getElementById('username').value;
            const bio = document.getElementById('bio').value;

            console.log('Action: Save Changes clicked.');
            console.log(`Payload ready for backend -> Username: "${username}", Bio: "${bio}"`);

            // TODO: Implement profile update logic later
            // 1. Validate username and bio inputs locally.
            // 2. Send JSON payload to backend PUT/PATCH endpoint (e.g., /api/user/profile).
            // 3. Display success/error UI toast message based on backend response.
        });
    }

    // ---------------------------------------------------------
    // Logout Logic
    // ---------------------------------------------------------
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            console.log('Action: Logout button clicked.');
            
            // TODO: Implement proper logout logic later
            // 1. Alert/Confirm dialog to ensure the user really wants to log out.
            // 2. Fetch POST to /api/auth/logout to clear server-side session cookies.
            // 3. Clear local storage/session storage (tokens, user cache).
            // 4. Redirect user back to the landing page or login page (window.location.href = '/login').
        });
    }
});
