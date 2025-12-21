<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">사용자명</label>
        <input
          id="username"
          v-model="username"
          type="text"
          required
          placeholder="사용자명을 입력하세요"
          autocomplete="username"
        />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          placeholder="비밀번호를 입력하세요"
          autocomplete="current-password"
        />
      </div>
      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? '로그인 중...' : '로그인' }}
      </button>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const auth = btoa(`${username.value}:${password.value}`)
    const authHeader = `Basic ${auth}`
    api.defaults.headers.common['Authorization'] = authHeader
    
    // localStorage에 인증 정보 저장
    localStorage.setItem('auth_token', authHeader)
    
    try {
      await api.options('/api/cards/')
      emit('login-success')
    } catch (testErr) {
      emit('login-success')
    }
  } catch (err) {
    error.value = '로그인에 실패했습니다. 사용자명과 비밀번호를 확인해주세요.'
    console.error('Login error:', err)
    delete api.defaults.headers.common['Authorization']
    localStorage.removeItem('auth_token')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  padding: var(--spacing-lg);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-group label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.form-group input {
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  transition: all 0.3s ease;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input::placeholder {
  color: var(--text-secondary);
}

.btn-primary {
  padding: 14px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  background: var(--primary-color);
  color: white;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
  letter-spacing: 0.3px;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-primary:disabled {
  background: var(--text-secondary);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.error-message {
  color: var(--danger-color);
  font-size: 14px;
  text-align: center;
  margin-top: var(--spacing-xs);
  padding: var(--spacing-xs);
  background: #f8d7da;
  border-radius: var(--radius-sm);
  border: 1px solid #f5c6cb;
}
</style>
