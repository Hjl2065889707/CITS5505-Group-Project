/**
 * settings.js — Logic for the Settings page.
 *
 * Handles:
 *   - Avatar upload (preview + API)
 *   - Profile update (username + bio)
 *   - Password change
 *   - Logout
 *   - Toast notifications
 */

document.addEventListener('DOMContentLoaded', () => {
  // ── DOM Elements ──
  const avatarInput = document.getElementById('avatarUpload');
  const avatarPreview = document.getElementById('avatarPreview');
  const saveProfileBtn = document.getElementById('saveProfileBtn');
  const changePasswordBtn = document.getElementById('changePasswordBtn');
  const logoutBtn = document.getElementById('logoutBtn');

  // ── Avatar Upload ──
  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener('change', handleAvatarUpload);
  }

  // ── Save Profile ──
  if (saveProfileBtn) {
    saveProfileBtn.addEventListener('click', handleSaveProfile);
  }

  // ── Change Password ──
  if (changePasswordBtn) {
    changePasswordBtn.addEventListener('click', handleChangePassword);
  }

  // ── Logout ──
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }
});


// ── Avatar Upload ────────────────────────────────────────────────────

async function handleAvatarUpload(event) {
  const file = event.target.files[0];
  const preview = document.getElementById('avatarPreview');

  if (!file) return;

  // Client-side type check
  if (!file.type.startsWith('image/')) {
    showToast('Please select a valid image file.', 'error');
    return;
  }

  // Client-side size check (5 MB)
  if (file.size > 5 * 1024 * 1024) {
    showToast('Image must be under 5MB.', 'error');
    return;
  }

  // Show local preview immediately
  const reader = new FileReader();
  reader.onload = (e) => { preview.src = e.target.result; };
  reader.readAsDataURL(file);

  // Upload to server
  const formData = new FormData();
  formData.append('avatar', file);

  try {
    const response = await fetch('/api/users/me/avatar', {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      showToast(data.error || 'Failed to upload avatar.', 'error');
      return;
    }

    showToast('Avatar updated!', 'success');

  } catch (error) {
    console.error('Avatar upload error:', error);
    showToast('Failed to upload avatar.', 'error');
  }
}


// ── Save Profile ─────────────────────────────────────────────────────

async function handleSaveProfile() {
  const btn = document.getElementById('saveProfileBtn');
  const username = document.getElementById('username').value.trim();
  const bio = document.getElementById('bio').value.trim();

  // Client-side validation
  if (username.length < 3 || username.length > 50) {
    showToast('Username must be 3-50 characters.', 'error');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Saving...';

  try {
    const response = await fetch('/api/users/me', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      body: JSON.stringify({ username, bio })
    });

    const data = await response.json();

    if (!response.ok) {
      // Handle field-specific errors
      const errorMsg = typeof data.error === 'object'
        ? Object.values(data.error).join(', ')
        : data.error;
      showToast(errorMsg || 'Failed to save changes.', 'error');
      return;
    }

    showToast('Profile updated!', 'success');

  } catch (error) {
    console.error('Save profile error:', error);
    showToast('Failed to save changes.', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Save Changes';
  }
}


// ── Change Password ──────────────────────────────────────────────────

async function handleChangePassword() {
  const btn = document.getElementById('changePasswordBtn');
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  // Client-side validation
  if (!currentPassword) {
    showToast('Please enter your current password.', 'error');
    return;
  }

  if (newPassword.length < 6) {
    showToast('New password must be at least 6 characters.', 'error');
    return;
  }

  if (newPassword !== confirmPassword) {
    showToast('New passwords do not match.', 'error');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Changing...';

  try {
    const response = await fetch('/api/users/me/password', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      body: JSON.stringify({ currentPassword, newPassword })
    });

    const data = await response.json();

    if (!response.ok) {
      showToast(data.error || 'Failed to change password.', 'error');
      return;
    }

    showToast('Password changed successfully!', 'success');

    // Clear the fields
    document.getElementById('currentPassword').value = '';
    document.getElementById('newPassword').value = '';
    document.getElementById('confirmPassword').value = '';

  } catch (error) {
    console.error('Change password error:', error);
    showToast('Failed to change password.', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Change Password';
  }
}


// ── Logout ───────────────────────────────────────────────────────────

function handleLogout() {
  if (confirm('Are you sure you want to log out?')) {
    window.location.href = '/logout';
  }
}


// ── Toast ────────────────────────────────────────────────────────────

let toastTimeout = null;

function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  if (!toast) return;

  // Clear any existing timeout
  if (toastTimeout) clearTimeout(toastTimeout);

  // Reset classes
  toast.className = 'toast';
  toast.classList.add(`toast--${type}`);
  toast.textContent = message;

  // Trigger show
  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  // Auto-hide after 3 seconds
  toastTimeout = setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}
