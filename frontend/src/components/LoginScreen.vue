<template>
  <div class="login-wrapper">
    <div class="glass-card login-card">
      <div class="brand-header">
        <span class="logo-box">WG</span>
        <h2>ACCESO RESTRINGIDO</h2>
        <p>WG Pentesting Suite v5.0</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label>Usuario Autorizado</label>
          <input type="text" v-model="username" placeholder="Ingrese su usuario" required autofocus />
        </div>

        <div class="input-group">
          <label>Contraseña</label>
          <input type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <div v-if="errorMessage" class="error-msg">
          ⚠️ {{ errorMessage }}
        </div>

        <button type="submit" class="btn-login">Desbloquear Sistema</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = () => {
  // Credenciales maestras
  if (username.value === 'walteralexis' && password.value === 'Python1650/') {
    errorMessage.value = ''
    emit('login-success')
  } else {
    errorMessage.value = 'Acceso Denegado. Credenciales incorrectas.'
    password.value = '' // Limpia la contraseña para intentar de nuevo
  }
}
</script>

<style scoped>
.login-wrapper {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 500;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: rgba(10, 10, 15, 0.85);
  padding: 40px;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0,0,0,0.8);
}

.brand-header {
  margin-bottom: 30px;
}

.logo-box {
  display: inline-block;
  background: var(--red-accent);
  color: white;
  font-weight: 800;
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 1.5rem;
  box-shadow: 0 0 20px var(--red-glow);
  margin-bottom: 15px;
}

.brand-header h2 {
  font-size: 1.2rem;
  letter-spacing: 2px;
  margin-bottom: 5px;
}

.brand-header p {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 8px;
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
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.input-group input:focus {
  border-color: var(--red-accent);
}

.error-msg {
  color: #fca5a5;
  background: rgba(220, 38, 38, 0.1);
  padding: 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  text-align: center;
  border: 1px solid rgba(220, 38, 38, 0.3);
}

.btn-login {
  background: var(--red-accent);
  color: white;
  border: none;
  padding: 14px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
  transition: all 0.2s;
}

.btn-login:hover {
  background: #ef4444;
  box-shadow: 0 0 15px var(--red-glow);
}
</style>