<template>
  <footer class="footer">
    <div class="footer-content">
      <p>&copy; 2026 WG Pentesting Suite. Todos los derechos reservados.</p>
      <div class="footer-links">
        <a href="#">Términos de Auditoría</a>
        <a href="#">Acuerdo de Confidencialidad (NDA)</a>
        <a href="#">Políticas de Uso Ético</a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid var(--glass-border);
  padding: 30px 20px;
  margin-top: 60px;
  background: rgba(5, 5, 7, 0.95);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.footer-links {
  display: flex;
  gap: 15px;
}

.footer-links a {
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: var(--text-white);
}
</style>