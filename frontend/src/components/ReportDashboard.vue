<template>
  <div class="report-wrapper">
    <div class="no-print header-actions">
      <h2>Reporte Oficial de Auditoría</h2>
      <div class="action-buttons">
        <button class="btn-secondary" @click="$emit('close-report')">Cerrar Reporte ✖</button>
        <button class="btn-print" @click="printPDF">🖨️ Exportar a PDF</button>
      </div>
    </div>

    <div class="executive-paper">
      <div class="paper-header">
        <div class="brand-zone">
          <h1>WG PENTESTING</h1>
          <p>Cybersecurity & Commercial Diagnostics</p>
        </div>
        <div class="meta-zone">
          <p><strong>Fecha:</strong> {{ result.fecha }}</p>
          <p><strong>Ref:</strong> AUDIT-{{ Math.floor(Math.random() * 9000) + 1000 }}</p>
        </div>
      </div>

      <div class="client-box">
        <div><small>Cliente:</small> <br><strong>{{ result.nombre_empresa }}</strong></div>
        <div><small>RUT:</small> <br><strong>{{ result.rut_empresa }}</strong></div>
        <div><small>Objetivo Analizado:</small> <br><strong>{{ result.dominio }}</strong></div>
        <div><small>Contacto:</small> <br><strong>{{ result.correo_contacto }}</strong></div>
      </div>

      <div class="score-banner" :class="scoreClass">
        <h3>ÍNDICE DE RIESGO PERIMETRAL</h3>
        <div class="score-number">{{ result.puntaje }} / 100</div>
        <p v-if="result.puntaje < 50" class="score-alert">Estado Crítico: Intervención Inmediata Requerida</p>
      </div>

      <div class="findings-area">
        <h3>Detalle Técnico y Riesgos Comerciales (Estándar OWASP)</h3>
        
        <div v-if="result.hallazgos.length === 0" class="finding-card success">
          ✅ Infraestructura sólida. No se detectaron vulnerabilidades críticas en la superficie expuesta.
        </div>
        
        <div v-for="(h, i) in result.hallazgos" :key="i" class="finding-card">
          <div class="finding-header">
            <h4>🚨 {{ h.msg }}</h4>
            <span class="owasp-tag">{{ knowledgeBase[h.id]?.owasp || 'A05:2021 Security Misconfiguration' }}</span>
          </div>
          
          <div class="finding-details">
            <p class="risk">
              <strong>Impacto Comercial:</strong> {{ knowledgeBase[h.id]?.riesgo }}
            </p>
            <div class="example-box">
              <strong>Ejemplo Real:</strong> {{ getEjemploReal(h.id) }}
            </div>
            <p class="solution">
              <strong>Solución para el área TI:</strong> {{ knowledgeBase[h.id]?.solucion }}
            </p>
          </div>
        </div>
      </div>

      <div class="quote-area">
        <h3>Cotización Oficial de Remediación</h3>
        <p>Servicio integral de fortificación de servidores (Hardening) e implementación perimetral.</p>
        <div class="price-val">
          Subtotal Estimado: ${{ cotizacion.toLocaleString('es-CL') }} CLP
        </div>
        <p class="disclaimer">* Valores expresados sin IVA. Incluye un escaneo de validación posterior a las correcciones tecnológicas.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: Object,
  knowledgeBase: Object
})

const emit = defineEmits(['close-report'])

const printPDF = () => window.print()

const scoreClass = computed(() => {
  if (props.result.puntaje >= 80) return 'good'
  if (props.result.puntaje >= 50) return 'warn'
  return 'bad'
})

const cotizacion = computed(() => {
  let base = 150000
  base += (props.result.nivel_riesgo.critico || 0) * 85000
  base += (props.result.nivel_riesgo.medio || 0) * 45000
  return base
})

// Función para agregar ejemplos dramáticos basados en el ID de la vulnerabilidad
const getEjemploReal = (id) => {
  if (id === 'HEADER_MISSING') return 'Un atacante inyecta un script malicioso en su web. Los clientes entran, el script roba sus tarjetas de crédito y culpan a su empresa por la brecha de seguridad.'
  if (id === 'PORT_OPEN') return 'Un bot ruso detecta su puerto MySQL abierto. Lanza millones de contraseñas por segundo hasta entrar, roba su base de datos y pide un rescate en Bitcoin (Ransomware).'
  if (id === 'DNS_VULN') return 'Ciberdelincuentes envían correos falsos haciéndose pasar por el Gerente General, pidiendo transferencias urgentes a sus proveedores. Como no tiene DMARC, el correo no es detectado como spam.'
  return 'Un actor malicioso explota esta configuración para comprometer la integridad del servidor.'
}
</script>

<style scoped>
.report-wrapper { 
  max-width: 900px; 
  margin: 0 auto; 
  margin-top: 20px; /* Separación del Header */
}

.header-actions { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 25px; 
}

.header-actions h2 { font-size: 1.5rem; }

.action-buttons {
  display: flex;
  gap: 15px;
}

.btn-secondary {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-secondary:hover { background: rgba(255,255,255,0.1); color: white; }

.btn-print { 
  background: var(--red-accent); 
  color: white; 
  border: none; 
  padding: 10px 20px; 
  border-radius: 6px; 
  cursor: pointer; 
  font-weight: 600; 
  box-shadow: 0 4px 15px var(--red-glow);
}
.btn-print:hover { background: #ef4444; }

.executive-paper { 
  background: white; 
  color: #0f172a; 
  padding: 50px; 
  border-radius: 10px; 
  box-shadow: 0 10px 50px rgba(0,0,0,0.5); 
}

.paper-header { display: flex; justify-content: space-between; border-bottom: 4px solid var(--red-accent); padding-bottom: 20px; margin-bottom: 25px; }
.brand-zone h1 { font-size: 2rem; font-weight: 900; color: #000; margin: 0; letter-spacing: -1px; }
.brand-zone p { color: #64748b; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px; }
.meta-zone { text-align: right; font-size: 0.95rem; color: #475569; }

.client-box { 
  display: grid; 
  grid-template-columns: repeat(4, 1fr); 
  background: #f8fafc; 
  padding: 20px; 
  border-radius: 8px; 
  margin-bottom: 35px; 
  font-size: 0.95rem; 
  border: 1px solid #e2e8f0; 
}
.client-box small { color: #64748b; text-transform: uppercase; font-size: 0.75rem; font-weight: 700; }
.client-box strong { color: #0f172a; display: block; margin-top: 5px; }

.score-banner { text-align: center; padding: 25px; border-radius: 8px; color: white; margin-bottom: 35px; box-shadow: inset 0 0 0 2px rgba(255,255,255,0.2); }
.score-banner.bad { background: linear-gradient(135deg, #dc2626, #991b1b); }
.score-banner.warn { background: linear-gradient(135deg, #f59e0b, #b45309); }
.score-banner.good { background: linear-gradient(135deg, #10b981, #047857); }
.score-number { font-size: 3rem; font-weight: 900; letter-spacing: -2px; margin: 10px 0; }
.score-alert { font-weight: 700; background: rgba(0,0,0,0.2); display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.85rem; }

.findings-area h3 { font-size: 1.3rem; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; color: #0f172a;}
.finding-card { background: #f8fafc; border-left: 5px solid #dc2626; padding: 20px; margin-bottom: 20px; border-radius: 0 8px 8px 0; border-top: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;}
.finding-card.success { border-left-color: #10b981; }

.finding-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px; }
.finding-header h4 { margin: 0; color: #0f172a; font-size: 1.1rem; max-width: 75%; }
.owasp-tag { background: #334155; color: white; font-size: 0.75rem; padding: 4px 10px; border-radius: 4px; font-weight: 600; }

.finding-details { display: flex; flex-direction: column; gap: 12px; }
.risk { color: #b91c1c; font-size: 0.95rem; }
.example-box { background: rgba(220, 38, 38, 0.05); border: 1px dashed #fca5a5; padding: 12px; border-radius: 6px; font-size: 0.9rem; color: #7f1d1d; }
.solution { color: #047857; font-size: 0.95rem; }

.quote-area { margin-top: 40px; background: #fff5f5; border: 2px dashed #dc2626; padding: 30px; border-radius: 10px; text-align: center; }
.quote-area h3 { color: #991b1b; font-size: 1.4rem; margin-bottom: 10px; }
.price-val { font-size: 2rem; font-weight: 900; color: #dc2626; margin: 20px 0; }
.disclaimer { font-size: 0.85rem; color: #64748b; }

@media print {
  .no-print { display: none !important; }
  .executive-paper { box-shadow: none; padding: 0; border: none; }
  body { background: white; }
  .report-wrapper { margin-top: 0; }
}
</style>