<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8050'

// Estado del formulario
const form = ref({
  url: 'https://effectivaspa.cl',
  nombre_empresa: 'Effectiva SpA',
  rut_empresa: '76.123.456-7',
  correo_contacto: 'contacto@effectiva.cl',
  telefono_contacto: '+56 9 1234 5678'
})

// Estados de ejecución y datos
const loading = ref(false)
const activeTab = ref('audit') // 'audit', 'dashboard', 'report'
const result = ref(null)
const knowledgeBase = ref({})
const selectedEduInfo = ref(null)

// Cargar Base de Conocimiento OWASP al iniciar
onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/knowledge`)
    knowledgeBase.value = res.data
  } catch (err) {
    console.error('Error al conectar con el backend:', err)
  }
})

// Ejecutar Auditoría
const runAudit = async () => {
  if (!form.value.url) return alert('Por favor ingrese una URL')
  loading.value = true
  result.value = null
  selectedEduInfo.value = null

  try {
    const res = await axios.post(`${API_BASE}/api/scan`, form.value)
    result.value = res.data
  } catch (err) {
    alert('Fallo al conectar con el motor de escaneo backend.')
  } finally {
    loading.value = false
  }
}

// Abrir Modal Educativo al hacer clic en un log o hallazgo
const openKnowledgeModal = (id) => {
  if (knowledgeBase.value[id]) {
    selectedEduInfo.value = knowledgeBase.value[id]
  } else {
    selectedEduInfo.value = {
      titulo: 'Evento de Auditoría',
      owasp: 'General Security',
      riesgo: 'Detalle técnico registrado durante el análisis perimetral.',
      solucion: 'Siga las recomendaciones de buenas prácticas de TI.'
    }
  }
}

// Cálculo de Valor de Cotización Sugerido ($ CLP)
const cotizacionEstimada = computed(() => {
  if (!result.value) return 0
  let base = 150000 // Base fija de informe
  base += (result.value.nivel_riesgo.critico || 0) * 85000
  base += (result.value.nivel_riesgo.medio || 0) * 45000
  return base
})

const printReport = () => {
  window.print()
}
</script>

<template>
  <div class="app-container">
    <!-- Header Principal -->
    <header class="app-header">
      <div class="logo-box">
        <span class="shield-icon">🛡️</span>
        <div>
          <h1>WG PENTESTING</h1>
          <p class="subtitle">Cybersecurity Audit & Commercial Engine v5.0</p>
        </div>
      </div>
    </header>

    <!-- Formulario de Entrada y Datos Comerciales -->
    <section class="form-section">
      <h3>📋 Datos de la Auditoría y Cliente</h3>
      <div class="form-grid">
        <div class="field">
          <label>URL Objetivo *</label>
          <input v-model="form.url" type="text" placeholder="https://ejemplo.cl" />
        </div>
        <div class="field">
          <label>Nombre Empresa</label>
          <input v-model="form.nombre_empresa" type="text" placeholder="Ej. Empresa SpA" />
        </div>
        <div class="field">
          <label>RUT Empresa</label>
          <input v-model="form.rut_empresa" type="text" placeholder="Ej. 76.xxx.xxx-k" />
        </div>
        <div class="field">
          <label>Correo Contacto</label>
          <input v-model="form.correo_contacto" type="email" placeholder="gerencia@empresa.cl" />
        </div>
        <div class="field">
          <label>Teléfono</label>
          <input v-model="form.telefono_contacto" type="text" placeholder="+56 9 ..." />
        </div>
      </div>

      <div class="action-bar">
        <button class="btn-scan" :disabled="loading" @click="runAudit">
          <span v-if="loading">⚡ Escaneando Objetivo...</span>
          <span v-else>🚀 Ejecutar Pentest Automatizado</span>
        </button>
      </div>
    </section>

    <!-- Navegación por Pestañas -->
    <nav class="tab-nav">
      <button :class="{ active: activeTab === 'audit' }" @click="activeTab = 'audit'">
        🔍 Consola Interactiva
      </button>
      <button :class="{ active: activeTab === 'dashboard' }" :disabled="!result" @click="activeTab = 'dashboard'">
        📊 Dashboard de Riesgos
      </button>
      <button :class="{ active: activeTab === 'report' }" :disabled="!result" @click="activeTab = 'report'">
        📄 Cotización & Reporte PDF
      </button>
    </nav>

    <!-- Pestaña 1: Consola de Salida -->
    <main v-if="activeTab === 'audit'" class="tab-content">
      <div class="console-box">
        <div class="console-header">
          <span>TERMINAL LOGS</span>
          <span class="tip-text">💡 Haz clic en los eventos para ver la ficha OWASP</span>
        </div>
        <div class="console-body">
          <div v-if="loading" class="scanning-loader">
            <p>Ejecutando pruebas de puertos, cabeceras, DNS y rate limiting...</p>
          </div>
          <div v-else-if="result" class="logs-list">
            <div
              v-for="(log, idx) in result.logs"
              :key="idx"
              class="log-line"
              :class="log.tipo.toLowerCase()"
              @click="openKnowledgeModal(log.tipo)"
            >
              <span class="log-tag">[{{ log.tipo }}]</span>
              <span class="log-msg">{{ log.mensaje }}</span>
            </div>
          </div>
          <div v-else class="empty-state">
            <p>Ingrese los datos de la empresa y presione "Ejecutar Pentest Automatizado"</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Pestaña 2: Dashboard -->
    <main v-if="activeTab === 'dashboard' && result" class="tab-content">
      <div class="dashboard-grid">
        <div class="score-card" :class="result.puntaje >= 80 ? 'good' : result.puntaje >= 50 ? 'warn' : 'bad'">
          <h4>SCORE DE SEGURIDAD</h4>
          <div class="score-number">{{ result.puntaje }} / 100</div>
          <p>{{ result.puntaje >= 80 ? 'Infraestructura Sólida' : 'Requiere Remediación Inmediata' }}</p>
        </div>

        <div class="risk-summary">
          <h4>Resumen de Vulnerabilidades</h4>
          <div class="risk-bar-container">
            <div class="risk-badge critical">Críticos: {{ result.nivel_riesgo.critico }}</div>
            <div class="risk-badge medium">Medios: {{ result.nivel_riesgo.medio }}</div>
            <div class="risk-badge low">Bajos: {{ result.nivel_riesgo.bajo }}</div>
          </div>
        </div>
      </div>
    </main>

    <!-- Pestaña 3: Reporte Comercial Imprimible -->
    <main v-if="activeTab === 'report' && result" class="tab-content printable-report">
      <button class="btn-print" @click="printReport">🖨️ Imprimir / Guardar como PDF</button>

      <div class="pdf-page">
        <div class="pdf-header">
          <div class="company-brand">
            <h2>WG PENTESTING</h2>
            <p>Servicios Profesionales de Ciberseguridad & Auditoría</p>
          </div>
          <div class="client-info">
            <p><strong>Cliente:</strong> {{ result.nombre_empresa }}</p>
            <p><strong>RUT:</strong> {{ result.rut_empresa }}</p>
            <p><strong>Objetivo:</strong> {{ result.dominio }}</p>
            <p><strong>Fecha:</strong> {{ result.fecha }}</p>
          </div>
        </div>

        <hr />

        <div class="report-score-box">
          NIVEL DE RIESGO PERIMETRAL: {{ result.puntaje }} / 100
        </div>

        <h3>Hallazgos Detectados y Plan de Remediación</h3>
        <div v-for="(item, i) in result.hallazgos" :key="i" class="report-finding">
          <h4>🚨 {{ item.msg }}</h4>
          <p><strong>OWASP:</strong> {{ knowledgeBase[item.id]?.owasp || 'A05:2021 Security Misconfiguration' }}</p>
          <p class="text-risk"><strong>Riesgo Comercial:</strong> {{ knowledgeBase[item.id]?.riesgo }}</p>
          <p class="text-sol"><strong>Solución para TI:</strong> {{ knowledgeBase[item.id]?.solucion }}</p>
        </div>

        <!-- Cuadro de Cotización Comercial -->
        <div class="quote-box">
          <h3>Propuesta Económica de Remediación</h3>
          <p>Implementación de parches de seguridad, cierre de puertos y configuración de cabeceras:</p>
          <div class="price-tag">
            Total Estimado: ${{ cotizacionEstimada.toLocaleString('es-CL') }} CLP + IVA
          </div>
          <p class="quote-note">* Incluye re-escaneo de certificación tras la remediación.</p>
        </div>
      </div>
    </main>

    <!-- Modal Educativo OWASP -->
    <div v-if="selectedEduInfo" class="modal-overlay" @click.self="selectedEduInfo = null">
      <div class="modal-card">
        <h3>🔍 {{ selectedEduInfo.titulo }}</h3>
        <span class="owasp-badge">{{ selectedEduInfo.owasp }}</span>
        
        <div class="modal-body">
          <p class="risk-p"><strong>⚠️ Riesgo Real:</strong> {{ selectedEduInfo.riesgo }}</p>
          <p class="sol-p"><strong>✅ Solución Recomendada:</strong> {{ selectedEduInfo.solucion }}</p>
        </div>

        <button class="btn-close" @click="selectedEduInfo = null">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  border-bottom: 2px solid var(--accent-teal);
  padding-bottom: 15px;
  margin-bottom: 25px;
}

.logo-box {
  display: flex;
  align-items: center;
  gap: 15px;
}

.shield-icon {
  font-size: 2.5rem;
}

.logo-box h1 {
  margin: 0;
  color: var(--accent-cyan);
  font-size: 1.8rem;
}

.subtitle {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.form-section {
  background: var(--bg-secondary);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field label {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.field input {
  background: var(--bg-primary);
  border: 1px solid var(--accent-teal);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
}

.action-bar {
  margin-top: 20px;
}

.btn-scan {
  background: var(--danger-red);
  color: white;
  border: none;
  padding: 12px 24px;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  font-size: 1rem;
}

.btn-scan:disabled {
  opacity: 0.5;
}

.tab-nav {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-nav button {
  background: var(--bg-secondary);
  border: none;
  color: var(--text-muted);
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.tab-nav button.active {
  background: var(--accent-teal);
  color: white;
}

.console-box {
  background: black;
  border: 1px solid #333;
  border-radius: 6px;
  overflow: hidden;
}

.console-header {
  background: #111;
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  font-family: monospace;
  font-size: 0.85rem;
  color: var(--accent-cyan);
}

.console-body {
  padding: 15px;
  min-height: 300px;
  font-family: monospace;
}

.log-line {
  padding: 6px 8px;
  cursor: pointer;
  border-bottom: 1px solid #111;
  display: flex;
  gap: 10px;
}

.log-line:hover {
  background: #1a1a1a;
}

.log-line.pass { color: var(--success-green); }
.log-line.warn { color: var(--warning-orange); }
.log-line.fail { color: var(--danger-red); }
.log-line.info { color: var(--accent-cyan); }

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-card {
  background: var(--bg-secondary);
  padding: 25px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.owasp-badge {
  background: var(--accent-teal);
  color: white;
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 0.8rem;
}

.risk-p { color: #ff6b6b; }
.sol-p { color: #1dd1a1; }

.btn-close {
  background: var(--danger-red);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
}

.pdf-page {
  background: white;
  color: #222;
  padding: 30px;
  border-radius: 6px;
}

.report-score-box {
  background: var(--danger-red);
  color: white;
  padding: 15px;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 4px;
  margin: 20px 0;
}

.quote-box {
  background: #f8f9fa;
  border: 2px dashed var(--accent-teal);
  padding: 20px;
  border-radius: 6px;
  margin-top: 30px;
}

.price-tag {
  font-size: 1.4rem;
  font-weight: bold;
  color: #27ae60;
}

.btn-print {
  background: var(--accent-teal);
  color: white;
  border: none;
  padding: 10px 20px;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 15px;
}

@media print {
  .btn-print, .app-header, .form-section, .tab-nav {
    display: none !important;
  }
  .app-container {
    padding: 0;
  }
  .pdf-page {
    box-shadow: none;
  }
}
</style>