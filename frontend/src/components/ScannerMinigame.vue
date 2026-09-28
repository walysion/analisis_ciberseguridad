<template>
  <div class="scanner-wrapper">
    <div class="header-scan">
      <h2>Auditoría Ofensiva en Curso</h2>
      <p>Nuestros motores están analizando la superficie de ataque del objetivo...</p>
    </div>

    <!-- Consola de Auditoría Avanzada -->
    <div class="hacker-terminal">
      <div class="terminal-header">
        <div class="terminal-dots">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
        </div>
        <span class="terminal-title">WG PENTESTING ENGINE v5.0 - LIVE TERMINAL</span>
        <span class="status-indicator">
          {{ isFinished ? 'ESCANEO FINALIZADO' : 'EJECUTANDO PAYLOADS...' }}
          <span v-if="!isFinished" class="pulse"></span>
        </span>
      </div>

      <div class="terminal-body" ref="terminalBody">
        <!-- Logs de simulación rápida -->
        <div v-if="!isFinished" class="live-logs">
          <div v-for="(log, idx) in activeLogs" :key="idx" class="log-line">
            <span class="log-time">[{{ log.time }}]</span>
            <span class="log-module" :class="log.color">{{ log.module }}</span>
            <span class="log-message">{{ log.text }}</span>
          </div>
          <div class="cursor-blink">_</div>
        </div>
        
        <!-- Resultados Reales desde FastAPI -->
        <div v-else class="real-logs">
          <div class="scan-complete-banner">
            > SISTEMA COMPROMETIDO. ANÁLISIS DE SUPERFICIE COMPLETADO.
          </div>
          <div class="hint-text no-print">💡 Haz clic en los eventos FAIL/WARN para inspeccionar los detalles técnicos.</div>
          
          <div 
            v-for="(log, idx) in result.logs" 
            :key="idx" 
            class="log-row interactive-log" 
            :class="log.tipo.toLowerCase()"
            @click="openLogDetails(log)"
          >
            <span class="badge-tag">{{ log.tipo }}</span>
            <span class="log-text">{{ log.mensaje }}</span>
          </div>
          
          <div class="action-row">
            <button class="btn-report" @click="$emit('view-report')">Generar Reporte y Cotización Oficial 📄</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Técnico de Detalles (Vuelve la tarjeta interactiva) -->
    <div v-if="selectedLog" class="modal-backdrop" @click.self="selectedLog = null">
      <div class="modal-card">
        <div class="modal-header">
          <h3>🔍 Inspección de Evento de Seguridad</h3>
          <button class="btn-close" @click="selectedLog = null">✖</button>
        </div>
        <div class="modal-body">
          <div class="event-tag" :class="selectedLog.tipo.toLowerCase()">{{ selectedLog.tipo }}</div>
          <p class="event-msg">{{ selectedLog.mensaje }}</p>
          <div class="modal-recommendation">
            <strong>Recomendación del Motor WG:</strong>
            <p>Se recomienda transferir esta evidencia al reporte comercial oficial para detallar la solución técnica y el impacto empresarial según el estándar OWASP.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  result: Object,
  isFinished: Boolean
})

const emit = defineEmits(['view-report'])

// Lógica de simulación técnica de la terminal
const terminalBody = ref(null)
const activeLogs = ref([])
let simInterval = null

const technicalPhrases = [
  { module: '[NMAP]', text: 'Iniciando escaneo SYN Stealth en puertos 1-65535...', color: 'text-blue' },
  { module: '[DNS]', text: 'Enumerando subdominios y volcando registros TXT...', color: 'text-gray' },
  { module: '[SSL]', text: 'Verificando cifrados débiles y certificados expirados...', color: 'text-gray' },
  { module: '[HTTP]', text: 'Bypass de WAF perimetral (Web Application Firewall)...', color: 'text-yellow' },
  { module: '[DIRB]', text: 'Buscando directorios ocultos (/admin, /.git, /backup)...', color: 'text-blue' },
  { module: '[PAYLOAD]', text: 'Inyectando vectores SQLi en parámetros GET...', color: 'text-red' },
  { module: '[AUTH]', text: 'Ejecutando fuerza bruta en panel de login (Diccionario: top10k)...', color: 'text-red' },
  { module: '[OWASP]', text: 'Analizando cabeceras X-Frame-Options y CSP...', color: 'text-green' },
  { module: '[MEMORY]', text: '0x00A1F3 0x88 0xFF 0x12 0xAA ... Volcado de respuesta', color: 'text-gray' }
]

const generateLog = () => {
  if (props.isFinished) return
  
  const now = new Date()
  const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}.${now.getMilliseconds().toString().padStart(3, '0')}`
  
  const randomPhrase = technicalPhrases[Math.floor(Math.random() * technicalPhrases.length)]
  
  activeLogs.value.push({
    time: timeStr,
    module: randomPhrase.module,
    text: randomPhrase.text,
    color: randomPhrase.color
  })

  // Mantener solo los últimos 50 logs para rendimiento
  if (activeLogs.value.length > 50) {
    activeLogs.value.shift()
  }

  // Auto-scroll al fondo
  nextTick(() => {
    if (terminalBody.value) {
      terminalBody.value.scrollTop = terminalBody.value.scrollHeight
    }
  })
}

// Lógica para el Modal Interactivo de Logs
const selectedLog = ref(null)

const openLogDetails = (log) => {
  // Solo abrir el modal si el log no es de tipo INFO o PASS genérico (opcional)
  // Aquí permitimos que se abra para FAIL y WARN principalmente
  if (log.tipo !== 'INFO') {
    selectedLog.value = log
  }
}

onMounted(() => {
  // Generar un log rápido cada 200 ms
  simInterval = setInterval(() => {
    if (!props.isFinished) {
      generateLog()
    }
  }, 200)
})

onUnmounted(() => {
  if (simInterval) clearInterval(simInterval)
})
</script>

<style scoped>
.scanner-wrapper {
  max-width: 1000px;
  margin: 0 auto;
}

.header-scan {
  text-align: center;
  margin-bottom: 25px;
}

.header-scan h2 { font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; }
.header-scan p { color: var(--text-muted); font-size: 1.1rem; }

.hacker-terminal {
  background: #050507;
  border: 1px solid var(--border-accent);
  border-radius: 10px;
  font-family: 'JetBrains Mono', monospace;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.8);
}

.terminal-header {
  background: #0a0a0f;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-subtle);
}

.terminal-dots { display: flex; gap: 8px; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27c93f; }

.terminal-title { 
  font-size: 0.8rem; 
  color: #64748b; 
  font-weight: 700; 
  letter-spacing: 1px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.75rem;
  color: var(--green-pass);
  font-weight: 700;
}

.pulse {
  width: 8px;
  height: 8px;
  background: var(--red-accent);
  border-radius: 50%;
  animation: pulse-red 1s infinite;
}

@keyframes pulse-red {
  0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(220, 38, 38, 0); }
  100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
}

.terminal-body {
  padding: 20px;
  height: 450px; /* Consola más grande y espectacular */
  overflow-y: auto;
  font-size: 0.85rem;
  line-height: 1.6;
}

/* Scrollbar de la terminal */
.terminal-body::-webkit-scrollbar { width: 6px; }
.terminal-body::-webkit-scrollbar-track { background: #000; }
.terminal-body::-webkit-scrollbar-thumb { background: #334155; }

/* Estilos de Live Logs */
.log-line {
  margin-bottom: 4px;
}
.log-time { color: #475569; margin-right: 10px; }
.log-module { font-weight: 700; margin-right: 10px; }
.log-message { color: #e2e8f0; }

.text-blue { color: #3b82f6; }
.text-gray { color: #94a3b8; }
.text-yellow { color: #eab308; }
.text-red { color: #ef4444; }
.text-green { color: #10b981; }

.cursor-blink {
  display: inline-block;
  width: 8px;
  height: 15px;
  background-color: #10b981;
  animation: blink 1s step-end infinite;
  margin-top: 5px;
}

@keyframes blink { 50% { opacity: 0; } }

/* Estilos de Real Logs (Backend) */
.scan-complete-banner {
  color: #10b981;
  font-weight: 800;
  font-size: 1.2rem;
  margin-bottom: 20px;
  border-bottom: 1px dashed #10b981;
  padding-bottom: 10px;
}

.hint-text { 
  color: #94a3b8; 
  font-size: 0.8rem; 
  margin-bottom: 15px; 
  font-style: italic; 
}

.interactive-log { 
  cursor: pointer; 
  transition: background 0.2s; 
}

.interactive-log:hover { 
  background: rgba(255,255,255,0.08); 
}

.log-row {
  display: flex;
  gap: 12px;
  padding: 8px 10px;
  margin-bottom: 6px;
  background: rgba(255,255,255,0.02);
  border-left: 2px solid transparent;
}

.badge-tag {
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
}

.log-row.pass { border-left-color: var(--green-pass); }
.log-row.pass .badge-tag { background: rgba(16, 185, 129, 0.2); color: var(--green-pass); }

.log-row.fail { border-left-color: var(--red-accent); }
.log-row.fail .badge-tag { background: rgba(220, 38, 38, 0.2); color: var(--red-accent); }

.log-row.warn { border-left-color: #f59e0b; }
.log-row.warn .badge-tag { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }

.log-row.info { border-left-color: #475569; }
.log-row.info .badge-tag { background: rgba(148, 163, 184, 0.2); color: var(--text-muted); }

.action-row {
  margin-top: 30px;
  text-align: center;
}

.btn-report {
  background: var(--red-accent);
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 1.05rem;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 4px 20px var(--red-glow);
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.btn-report:hover { background: #ef4444; transform: translateY(-2px); }

/* Estilos del Modal Técnico (Tarjeta interactiva) */
.modal-backdrop { 
  position: fixed; 
  top: 0; 
  left: 0; 
  width: 100vw; 
  height: 100vh; 
  background: rgba(0,0,0,0.85); 
  z-index: 999; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  backdrop-filter: blur(5px); 
}

.modal-card { 
  background: #0a0a0f; 
  border: 1px solid #334155; 
  border-radius: 8px; 
  width: 90%; 
  max-width: 500px; 
  box-shadow: 0 20px 40px rgba(0,0,0,0.9);
}

.modal-header { 
  display: flex; 
  justify-content: space-between; 
  padding: 15px 20px; 
  border-bottom: 1px solid #1e293b; 
  color: white; 
}

.modal-header h3 { 
  font-size: 1.1rem; 
  margin: 0; 
}

.btn-close { 
  background: none; 
  border: none; 
  color: #94a3b8; 
  cursor: pointer; 
  font-size: 1.2rem; 
}

.btn-close:hover { 
  color: white; 
}

.modal-body { 
  padding: 20px; 
  color: #e2e8f0; 
}

.event-tag { 
  display: inline-block; 
  padding: 4px 8px; 
  border-radius: 4px; 
  font-weight: bold; 
  font-size: 0.8rem; 
  margin-bottom: 10px; 
}

.event-tag.fail { background: rgba(220, 38, 38, 0.2); color: #ef4444; }
.event-tag.warn { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.event-tag.pass { background: rgba(16, 185, 129, 0.2); color: #10b981; }

.event-msg { 
  font-family: 'JetBrains Mono', monospace; 
  font-size: 0.95rem; 
  margin-bottom: 20px; 
  line-height: 1.5; 
}

.modal-recommendation { 
  background: rgba(59, 130, 246, 0.1); 
  border: 1px solid rgba(59, 130, 246, 0.3); 
  padding: 15px; 
  border-radius: 6px; 
}

.modal-recommendation strong { 
  color: #60a5fa; 
  display: block; 
  margin-bottom: 5px; 
  font-size: 0.9rem;
}

.modal-recommendation p { 
  font-size: 0.85rem; 
  color: #cbd5e1; 
  line-height: 1.5; 
  margin: 0;
}
</style>