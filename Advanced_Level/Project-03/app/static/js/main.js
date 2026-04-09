// PyBlog Main JS

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });

  // Character counter for comment textarea
  const commentBox = document.querySelector('textarea[name="content"]');
  if (commentBox) {
    const counter = document.createElement('small');
    counter.className = 'text-muted d-block text-end mt-1';
    commentBox.parentNode.insertBefore(counter, commentBox.nextSibling);
    commentBox.addEventListener('input', () => {
      counter.textContent = `${commentBox.value.length} / 1000 characters`;
    });
  }

  // Confirm delete buttons
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // Active nav link highlight
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});
