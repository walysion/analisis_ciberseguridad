<template>
  <div class="hero-container">
    <div class="hero-content">
      <div class="status-badge">
        <span class="pulse-dot"></span> WG Engine v5.0 Online
      </div>
      
      <h1 class="hero-title">
        Auditoría <span class="text-red">Pentesting</span>
      </h1>
      <p class="hero-subtitle">
        Ingresa el dominio corporativo. Encontraremos puertos abiertos, fugas de datos y vulnerabilidades perimetrales antes que los atacantes.
      </p>

      <div class="search-box">
        <span class="icon-lock">🔒</span>
        <input 
          type="text" 
          v-model="targetUrl" 
          placeholder="ejemplo: https://empresa-objetivo.cl" 
          @keyup.enter="handleAudit"
        />
        <button class="btn-audit" @click="handleAudit">Auditar Ahora</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const targetUrl = ref('')
const emit = defineEmits(['request-audit'])

const handleAudit = () => {
  if (!targetUrl.value) return alert('Por favor, ingresa una URL válida.')
  emit('request-audit', targetUrl.value)
}
</script>

<style scoped>
.hero-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 20px;
}

.hero-content {
  max-width: 800px;
  width: 100%;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(20, 20, 25, 0.8);
  border: 1px solid var(--glass-border);
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 25px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: var(--green-pass, #10b981);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--green-pass, #10b981);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.8; }
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 20px;
  line-height: 1.1;
}

.text-red {
  color: var(--red-accent);
  text-shadow: 0 0 25px var(--red-glow);
}

.hero-subtitle {
  font-size: 1.1rem;
  color: var(--text-muted);
  margin-bottom: 40px;
  line-height: 1.6;
}

.search-box {
  display: flex;
  background: rgba(10, 10, 15, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  padding: 8px;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}

.icon-lock {
  padding: 0 15px;
  display: flex;
  align-items: center;
  font-size: 1.2rem;
  opacity: 0.5;
}

.search-box input {
  flex: 1;
  background: transparent;
  border: none;
  color: white;
  font-size: 1.1rem;
  outline: none;
}

.search-box input::placeholder {
  color: #475569;
}

.btn-audit {
  background: var(--red-accent);
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-audit:hover {
  background: #ef4444;
  box-shadow: 0 0 20px var(--red-glow);
}
</style>