<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import BackgroundCinematic from './components/BackgroundCinematic.vue'
import PublicLanding from './components/PublicLanding.vue'
import LoginScreen from './components/LoginScreen.vue'
import HeaderNav from './components/HeaderNav.vue'
import IntranetDashboard from './components/IntranetDashboard.vue'
import CorporateFooter from './components/CorporateFooter.vue'

// Componentes del Módulo Pentesting
import LandingHero from './components/LandingHero.vue'
import LeadModal from './components/LeadModal.vue'
import ScannerMinigame from './components/ScannerMinigame.vue'
import ReportDashboard from './components/ReportDashboard.vue'

const API_BASE = 'http://localhost:8050'

// ESTADOS PRINCIPALES DE LA APP: 'public', 'login', 'dashboard', 'pentesting'
const globalState = ref('public')

// Estados internos del módulo de pentesting
const pentestingView = ref('search') // 'search', 'scanning', 'report'
const showModal = ref(false)
const pendingUrl = ref('')
const knowledgeBase = ref({})
const scanResult = ref(null)
const scanFinished = ref(false)

onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/knowledge`)
    knowledgeBase.value = res.data
  } catch (err) {
    console.warn('Backend no disponible al cargar OWASP Data. Verifica Docker.')
  }
})

// --- FUNCIONES DE NAVEGACIÓN ---
const navigateToLogin = () => { globalState.value = 'login' }
const handleLoginSuccess = () => { globalState.value = 'dashboard' }
const openApp = (appName) => {
  if (appName === 'pentesting') {
    globalState.value = 'pentesting'
    pentestingView.value = 'search'
  }
}

// --- FUNCIONES DEL MÓDULO PENTESTING ---
const openCaptureModal = (url) => {
  let formattedUrl = url.trim()
  if (!/^https?:\/\//i.test(formattedUrl)) {
    formattedUrl = 'https://' + formattedUrl
  }
  pendingUrl.value = formattedUrl
  showModal.value = true
}

const startAuditProcess = async (formData) => {
  showModal.value = false
  pentestingView.value = 'scanning'
  scanFinished.value = false
  scanResult.value = null

  const startTime = Date.now()
  try {
    const res = await axios.post(`${API_BASE}/api/scan`, formData)
    scanResult.value = res.data
  } catch (err) {
    // Dummy en caso de error de conexión local
    scanResult.value = {
      dominio: formData.url,
      nombre_empresa: formData.nombre_empresa,
      rut_empresa: formData.rut_empresa,
      correo_contacto: formData.correo_contacto,
      fecha: new Date().toLocaleDateString(),
      puntaje: 0,
      nivel_riesgo: { critico: 0, medio: 0 },
      hallazgos: [],
      logs: [{ tipo: 'FAIL', mensaje: 'Error al conectar con el motor remoto.' }]
    }
  } finally {
    const elapsedTime = Date.now() - startTime
    const minWaitTime = 5500 
    const remainingTime = Math.max(0, minWaitTime - elapsedTime)
    setTimeout(() => {
      scanFinished.value = true
    }, remainingTime)
  }
}
</script>

<template>
  <div class="app-wrapper">
    <!-- El fondo de video siempre está visible en toda la plataforma -->
    <BackgroundCinematic />

    <!-- 1. VISTA PÚBLICA (Landing Comercial) -->
    <PublicLanding 
      v-if="globalState === 'public'" 
      @go-login="navigateToLogin" 
    />

    <!-- 2. VISTA LOGIN -->
    <LoginScreen 
      v-else-if="globalState === 'login'" 
      @login-success="handleLoginSuccess" 
    />

    <!-- 3. INTRANET (Requiere Login) -->
    <template v-else>
      <HeaderNav />

      <main class="main-content">
        <!-- Dashboard Principal de Iconos -->
        <IntranetDashboard 
          v-if="globalState === 'dashboard'" 
          @open-app="openApp" 
        />

        <!-- Módulo de Pentesting Activo -->
        <div v-if="globalState === 'pentesting'" class="module-container">
          <!-- Ocultamos el botón de volver si estamos viendo el reporte -->
          <button 
            v-if="pentestingView !== 'report'" 
            class="btn-back" 
            @click="globalState = 'dashboard'"
          >
            ← Volver al Dashboard
          </button>
          
          <LandingHero 
            v-if="pentestingView === 'search'" 
            @request-audit="openCaptureModal" 
          />
          
          <ScannerMinigame 
            v-if="pentestingView === 'scanning'" 
            :result="scanResult" 
            :isFinished="scanFinished" 
            @view-report="pentestingView = 'report'" 
          />
          
          <ReportDashboard 
            v-if="pentestingView === 'report'" 
            :result="scanResult" 
            :knowledgeBase="knowledgeBase"
            @close-report="pentestingView = 'search'"
          />
        </div>
      </main>

      <LeadModal 
        v-if="showModal" 
        :initial-url="pendingUrl" 
        @close="showModal = false" 
        @start-scan="startAuditProcess" 
      />
    </template>
    
    <!-- Footer Global -->
    <CorporateFooter />
  </div>
</template>

<style>
.app-wrapper {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  padding-top: 100px;
  padding-bottom: 40px;
}
.module-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}
.btn-back {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.2s;
}
.btn-back:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}
</style>