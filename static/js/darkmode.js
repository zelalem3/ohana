document.addEventListener('DOMContentLoaded', function() {
  const toggleDarkModeButton = document.getElementById('toggle-dark-mode');

  if (toggleDarkModeButton) {
    toggleDarkModeButton.addEventListener('click', toggleDarkMode);
  }

  const darkModeEnabled = localStorage.getItem('darkMode') === 'enabled';

  // Add the dark-mode class to the body if dark mode is enabled
  if (darkModeEnabled) {
    document.body.classList.add('dark-mode');
  }

  function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');

    // Save the user's preference in local storage
    if (document.body.classList.contains('dark-mode')) {
      localStorage.setItem('darkMode', 'enabled');
    } else {
      localStorage.setItem('darkMode', 'disabled');
    }
  }
});
