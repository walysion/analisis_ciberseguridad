<template>
  <header class="header glass-panel">
    <div class="nav-container">
      <div class="brand">
        <span class="logo-box">WG</span>
        <div class="brand-text">
          <span class="title">WG CYBER SUITE</span>
          <span class="subtitle">Enterprise Security Platform</span>
        </div>
      </div>

      <nav class="nav-links">
        <a href="#" class="active">Pentesting Web</a>
        <a href="#" class="locked">Phishing Sim 🔒</a>
        <a href="#" class="locked">Dark Web 🔒</a>
      </nav>

      <div class="user-profile">
        <span class="avatar">WG</span>
        <span class="role">Admin (Walter Alexis)</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-box {
  background: var(--red-accent);
  color: white;
  font-weight: 800;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 1rem;
  box-shadow: 0 0 15px var(--red-glow);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.title {
  display: block;
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: 1px;
}

.subtitle {
  display: block;
  font-size: 0.65rem;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a.active {
  color: var(--text-white);
  border-bottom: 2px solid var(--red-accent);
  padding-bottom: 4px;
}

.nav-links a.locked {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-links a:not(.locked):hover {
  color: var(--text-white);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  background: #1e293b;
  color: white;
  padding: 6px 10px;
  border-radius: 50%;
  font-size: 0.8rem;
  font-weight: 700;
}

.role {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
}
</style>