<template>
  <div class="public-wrapper">
    <!-- Navbar Público -->
    <header class="public-header glass-panel">
      <div class="nav-container">
        <div class="brand">
          <span class="logo-box">WG</span>
          <div class="brand-text">
            <span class="title">WG PENTESTING</span>
            <span class="subtitle">Cybersecurity Consulting</span>
          </div>
        </div>
        <button class="btn-login" @click="$emit('go-login')">
          Acceso Clientes 🔒
        </button>
      </div>
    </header>

    <!-- Contenido Comercial -->
    <main class="public-main">
      <section class="hero-section">
        <h1 class="main-title">Protege tu infraestructura antes de que sea el <span class="text-red">próximo titular.</span></h1>
        <p class="main-subtitle">
          Auditorías perimetrales de grado militar para empresas. Descubrimos tus brechas de seguridad antes de que los ciberdelincuentes las exploten.
        </p>
      </section>

      <section class="info-grid">
        <div class="info-card">
          <div class="icon">🏴‍☠️</div>
          <h3>Amenaza Ransomware</h3>
          <p>El secuestro de datos (Ransomware) puede paralizar su empresa por semanas. Identificamos los puertos y servicios expuestos que usan los atacantes para infiltrarse y cifrar sus discos.</p>
        </div>

        <div class="info-card">
          <div class="icon">⏳</div>
          <h3>Auditorías Recurrentes</h3>
          <p>Un sistema seguro hoy puede ser vulnerable mañana. Cada día nacen ataques "Zero-Day". Recomendamos análisis mensuales para garantizar que las nuevas tecnologías no abran brechas imprevistas.</p>
        </div>

        <div class="info-card">
          <div class="icon">🤝</div>
          <h3>Transparencia y NDA</h3>
          <p>Operamos bajo estrictos Acuerdos de Confidencialidad (NDA) y estándares éticos. Sus datos, infraestructura y los resultados de nuestras auditorías están protegidos militarmente.</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
const emit = defineEmits(['go-login'])
</script>

<style scoped>
.public-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.public-header {
  position: fixed;
  top: 0; left: 0; width: 100%;
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
}

.title { display: block; font-weight: 700; font-size: 1.1rem; }
.subtitle { display: block; font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 2px;}

.btn-login {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-login:hover {
  background: white;
  color: black;
}

.public-main {
  flex: 1;
  padding: 150px 20px 80px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  max-width: 900px;
  margin: 0 auto 80px;
}

.main-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 25px;
}

.text-red {
  color: var(--red-accent);
  text-shadow: 0 0 20px var(--red-glow);
}

.main-subtitle {
  font-size: 1.2rem;
  color: var(--text-muted);
  line-height: 1.6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.info-card {
  background: rgba(15, 15, 20, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 30px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.info-card .icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.info-card h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: white;
}

.info-card p {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
}
</style>