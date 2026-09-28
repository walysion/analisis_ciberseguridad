<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h3>Configuración del Escáner</h3>
        <p>Los datos comerciales son opcionales. Úselos solo si desea generar el reporte PDF al finalizar.</p>
      </div>

      <div class="modal-body">
        <div class="input-group">
          <label>URL Objetivo (Bloqueado)</label>
          <input type="text" :value="initialUrl" disabled class="disabled-input" />
        </div>

        <div class="input-group">
          <label>Nombre de la Empresa (Opcional)</label>
          <input type="text" v-model="formData.nombre_empresa" placeholder="Ej: Empresa SpA" autofocus />
        </div>

        <div class="row-group">
          <div class="input-group">
            <label>RUT Empresa (Opcional)</label>
            <input type="text" v-model="formData.rut_empresa" placeholder="76.xxx.xxx-k" />
          </div>
          <div class="input-group">
            <label>Teléfono (Opcional)</label>
            <input type="text" v-model="formData.telefono_contacto" placeholder="+56 9 ..." />
          </div>
        </div>

        <div class="input-group">
          <label>Correo Electrónico (Opcional)</label>
          <input type="email" v-model="formData.correo_contacto" placeholder="contacto@empresa.cl" />
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn-cancel" @click="$emit('close')">Cancelar</button>
        <button class="btn-launch" @click="submitForm">Lanzar Auditoría 🚀</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  initialUrl: String
})

const emit = defineEmits(['close', 'start-scan'])

const formData = ref({
  nombre_empresa: '',
  rut_empresa: '',
  correo_contacto: '',
  telefono_contacto: ''
})

const submitForm = () => {
  // Eliminamos la restricción de campos obligatorios. 
  // Ahora envía lo que sea que haya escrito el usuario (o strings vacíos).
  const payload = {
    url: props.initialUrl, 
    nombre_empresa: formData.value.nombre_empresa || 'Cliente No Especificado',
    rut_empresa: formData.value.rut_empresa || 'N/A',
    correo_contacto: formData.value.correo_contacto || 'N/A',
    telefono_contacto: formData.value.telefono_contacto || 'N/A'
  }
  
  emit('start-scan', payload)
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-card {
  background: rgba(15, 15, 20, 0.95);
  border: 1px solid var(--glass-border);
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
  overflow: hidden;
}

.modal-header {
  padding: 25px 30px 15px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.modal-header h3 {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.modal-header p {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.modal-body {
  padding: 25px 30px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.row-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.input-group label {
  display: block;
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.input-group input {
  width: 100%;
  background: rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.1);
  color: white;
  padding: 12px 15px;
  border-radius: 6px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.input-group input:focus {
  border-color: var(--red-accent);
}

.disabled-input {
  color: #64748b !important;
  cursor: not-allowed;
  opacity: 0.7;
}

.modal-footer {
  padding: 20px 30px;
  background: rgba(0,0,0,0.3);
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  border-top: 1px solid rgba(255,255,255,0.05);
}

.btn-cancel {
  background: transparent;
  color: var(--text-muted);
  border: none;
  font-weight: 500;
  cursor: pointer;
  padding: 10px 15px;
}

.btn-cancel:hover { color: white; }

.btn-launch {
  background: var(--red-accent);
  color: white;
  border: none;
  padding: 10px 24px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 4px 15px var(--red-glow);
  transition: all 0.2s;
}

.btn-launch:hover { background: #ef4444; }
</style>