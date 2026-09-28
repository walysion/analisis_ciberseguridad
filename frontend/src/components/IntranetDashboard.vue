<template>
  <div class="dashboard-wrapper">
    <div class="dashboard-header">
      <h2>Módulos de Seguridad (Intranet)</h2>
      <p>Selecciona una aplicación de la suite para operar.</p>
    </div>

    <div class="apps-grid">
      <!-- Módulo Activo: Pentesting -->
      <div class="app-card active" @click="$emit('open-app', 'pentesting')">
        <div class="app-icon wg-blue">🌐</div>
        <div class="app-info">
          <h3>Pentesting Web</h3>
          <p>Auditoría de superficie y puertos.</p>
        </div>
      </div>

      <!-- Módulos Futuros (Bloqueados por ahora) -->
      <div class="app-card locked">
        <div class="app-icon wg-purple">🎣</div>
        <div class="app-info">
          <h3>Phishing Sim</h3>
          <p>Simulador de ataques a empleados. (Próximamente)</p>
        </div>
        <div class="lock-badge">🔒</div>
      </div>

      <div class="app-card locked">
        <div class="app-icon wg-dark">🕷️</div>
        <div class="app-info">
          <h3>Dark Web Monitor</h3>
          <p>Rastreo de credenciales filtradas. (Próximamente)</p>
        </div>
        <div class="lock-badge">🔒</div>
      </div>

      <div class="app-card locked">
        <div class="app-icon wg-red">🛡️</div>
        <div class="app-info">
          <h3>Ransomware Shield</h3>
          <p>Análisis de endpoints. (Próximamente)</p>
        </div>
        <div class="lock-badge">🔒</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['open-app'])
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.dashboard-header {
  margin-bottom: 40px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 20px;
}

.dashboard-header h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.dashboard-header p {
  color: var(--text-muted);
}

.apps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
}

.app-card {
  position: relative;
  background: rgba(15, 15, 20, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s;
}

.app-card.active {
  cursor: pointer;
}

.app-card.active:hover {
  transform: translateY(-5px);
  border-color: var(--red-accent);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.app-card.locked {
  opacity: 0.6;
  cursor: not-allowed;
  filter: grayscale(100%);
}

.app-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.wg-blue { background: rgba(59, 130, 246, 0.2); }
.wg-purple { background: rgba(168, 85, 247, 0.2); }
.wg-dark { background: rgba(30, 41, 59, 0.5); }
.wg-red { background: rgba(239, 68, 68, 0.2); }

.app-info h3 {
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.app-info p {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.lock-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 1.2rem;
}
</style>