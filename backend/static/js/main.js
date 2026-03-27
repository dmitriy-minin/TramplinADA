/* ============================================
   ТРАМПЛИН — main.js
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ---- Burger menu ----
  const burger = document.getElementById('navBurger');
  const navLinks = document.querySelector('.nav-links');
  if (burger && navLinks) {
    burger.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      burger.classList.toggle('open');
    });
    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!burger.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        burger.classList.remove('open');
      }
    });
  }

  // ---- Auto-dismiss alerts after 5s ----
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.4s';
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 400);
    }, 5000);
  });

  // ---- Active nav link on scroll (anchor links) ----
  const sidebarLinks = document.querySelectorAll('.sidebar-nav a[href^="#"]');
  if (sidebarLinks.length) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          sidebarLinks.forEach(function (link) {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + entry.target.id) {
              link.classList.add('active');
            }
          });
        }
      });
    }, { threshold: 0.3 });

    sidebarLinks.forEach(function (link) {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) observer.observe(target);
    });
  }

  // ---- Card hover on opp-list view ----
  function applyListView() {
    document.querySelectorAll('.opp-list .opp-card').forEach(function (card) {
      card.style.flexDirection = 'row';
      card.style.flexWrap = 'wrap';
      card.style.alignItems = 'center';
      card.style.gap = '16px';
    });
  }

  // ---- Confirm delete forms ----
  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!confirm(form.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // ---- Salary range display ----
  const salaryMin = document.querySelector('input[name="salary_min"]');
  const salaryMax = document.querySelector('input[name="salary_max"]');
  if (salaryMin && salaryMax) {
    function formatSalary(val) {
      return val ? parseInt(val).toLocaleString('ru-RU') : '';
    }
    [salaryMin, salaryMax].forEach(function (input) {
      input.addEventListener('blur', function () {
        // no-op: just keep values
      });
    });
  }

  // ---- Tag badge toggle on forms ----
  document.querySelectorAll('.tag-checkbox').forEach(function (cb) {
    const label = cb.nextElementSibling;
    if (!label) return;
    function update() {
      if (cb.checked) {
        label.style.borderColor = 'var(--primary)';
        label.style.opacity = '1';
        label.style.fontWeight = '700';
      } else {
        label.style.borderColor = 'transparent';
        label.style.opacity = '0.65';
        label.style.fontWeight = '600';
      }
    }
    update();
    cb.addEventListener('change', update);
  });

  // ---- Smooth scroll for anchor links ----
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      const id = a.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ---- List/Grid view persistence ----
  const viewKey = 'tramplin_view_pref';
  const savedView = localStorage.getItem(viewKey);
  if (savedView && window.setView) {
    window.setView(savedView);
  }
  // Wrap setView to save preference
  if (window.setView) {
    const origSetView = window.setView;
    window.setView = function (v) {
      origSetView(v);
      localStorage.setItem(viewKey, v);
    };
  }

});

// ---- AJAX favorite toggle ----
function toggleFavorite(pk, btn) {
  fetch('/opportunities/' + pk + '/favorite/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    },
  })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      if (data.ok) {
        btn.textContent = data.is_favorite ? '❤️ В избранном' : '🤍 В избранное';
        btn.classList.toggle('btn-primary', data.is_favorite);
        btn.classList.toggle('btn-ghost', !data.is_favorite);
      }
    })
    .catch(function () {});
}

function getCookie(name) {
  let v = null;
  document.cookie.split(';').forEach(function (c) {
    c = c.trim();
    if (c.startsWith(name + '=')) v = decodeURIComponent(c.slice(name.length + 1));
  });
  return v;
}
