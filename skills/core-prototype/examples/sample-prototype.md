# Sample Prototype Output

This is an example of what a high-quality, static HTML/CSS/JS prototype should look like when delivered. It uses realistic copy, placeholder images, CSS Custom Properties, and responsive design with a working mobile sidebar.

## `prototype/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Acme Corp Dashboard Mockup</title>
  <link rel="stylesheet" href="styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
  <div class="layout">
    <!-- Overlay for mobile sidebar -->
    <div class="sidebar-overlay" id="sidebarOverlay"></div>
    
    <aside class="sidebar" id="sidebar">
      <div class="logo">Acme Corp</div>
      <nav class="nav-links">
        <a href="#" class="active">Dashboard</a>
        <a href="#">Projects</a>
        <a href="#">Team</a>
        <a href="#">Settings</a>
      </nav>
    </aside>
    <main class="content">
      <header class="header">
        <div class="header-left">
          <button class="menu-toggle" id="menuToggle">☰</button>
          <h1>Welcome back, Jane</h1>
        </div>
        <button class="btn btn-primary">New Project</button>
      </header>
      <section class="metrics-grid">
        <div class="card">
          <h3>Total Revenue</h3>
          <p class="metric">$24,500</p>
        </div>
        <div class="card">
          <h3>Active Projects</h3>
          <p class="metric">12</p>
        </div>
        <div class="card">
          <h3>Team Members</h3>
          <p class="metric">8</p>
        </div>
      </section>
      <section class="recent-activity">
        <h2>Recent Activity</h2>
        <div class="activity-list">
          <div class="activity-item">
            <img src="https://placehold.co/40x40" alt="Avatar" class="avatar">
            <div class="activity-text">
              <p><strong>Mark Smith</strong> uploaded a new design for Project X.</p>
              <span class="time">2 hours ago</span>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>

  <script src="app.js"></script>
</body>
</html>
```

## `prototype/styles.css`

```css
:root {
  --primary: #2563eb;
  --bg-main: #f8fafc;
  --bg-sidebar: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --border: #e2e8f0;
  --font-sans: 'Inter', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-sans); background: var(--bg-main); color: var(--text-main); overflow-x: hidden; }

.layout {
  display: grid;
  grid-template-columns: 1fr; /* Mobile first */
  min-height: 100vh;
}

/* Sidebar - Hidden on mobile by default */
.sidebar { 
  background: var(--bg-sidebar); 
  border-right: 1px solid var(--border); 
  padding: 1.5rem; 
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: 240px;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: 50;
}
.sidebar.open { transform: translateX(0); }

.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 40;
}
.sidebar-overlay.open { display: block; }

.logo { font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem; }
.nav-links a { display: block; padding: 0.75rem 1rem; color: var(--text-muted); text-decoration: none; border-radius: 6px; margin-bottom: 0.5rem;}
.nav-links a.active, .nav-links a:hover { background: var(--bg-main); color: var(--primary); font-weight: 500; }

/* Content */
.content { padding: 1.5rem; width: 100%; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem; }
.header-left { display: flex; align-items: center; gap: 1rem; }
.menu-toggle { background: none; border: 1px solid var(--border); border-radius: 4px; padding: 0.5rem; font-size: 1.2rem; cursor: pointer; display: block; }
h1 { font-size: 1.5rem; }
.btn { background: var(--primary); color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; white-space: nowrap; }

/* Grid */
.metrics-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; margin-bottom: 3rem; }
.card { background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border); }
.card h3 { font-size: 0.875rem; color: var(--text-muted); font-weight: 500; }
.metric { font-size: 2rem; font-weight: 600; margin-top: 0.5rem; }

/* Activity */
.activity-item { display: flex; align-items: center; gap: 1rem; padding: 1rem 0; border-bottom: 1px solid var(--border); }
.avatar { border-radius: 50%; }
.time { font-size: 0.875rem; color: var(--text-muted); }

/* Tablet & Desktop Breakpoints */
@media (min-width: 768px) {
  .layout { grid-template-columns: 240px 1fr; }
  .sidebar { transform: translateX(0); position: sticky; }
  .menu-toggle { display: none; }
  .sidebar-overlay { display: none !important; }
  .metrics-grid { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
  .content { padding: 2rem; }
  h1 { font-size: 2rem; }
}
```

## `prototype/app.js`

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menuToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  function toggleMenu() {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('open');
  }

  menuToggle.addEventListener('click', toggleMenu);
  overlay.addEventListener('click', toggleMenu);
});
```
