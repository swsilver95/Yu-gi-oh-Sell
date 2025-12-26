<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <h1 class="site-title">Yu-gi-oh Sell</h1>
        <div class="header-actions">
          <button v-if="!isAuthenticated" @click="showLoginModal = true" class="btn-login">
            관리자 로그인
          </button>
          <div v-else class="auth-info-header">
            <span class="auth-status">관리자로 로그인됨</span>
            <button @click="handleLogout" class="btn-logout">로그아웃</button>
          </div>
        </div>
      </div>
    </header>
    
    <main class="app-main">
      <div class="container">
        <div v-if="isAuthenticated" class="upload-section">
          <CardUpload @card-created="loadCards" />
        </div>
        
        <div class="cards-section">
          <h2 class="section-title">카드 목록</h2>
          <CardGrid :cards="cards" :is-admin="isAuthenticated" @card-updated="loadCards" />
        </div>
      </div>
    </main>
    
    <LoginModal :show="showLoginModal" @close="showLoginModal = false" @login-success="handleLoginSuccess" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { cardService } from './services/api'
import CardGrid from './components/CardGrid.vue'
import CardUpload from './components/CardUpload.vue'
import LoginModal from './components/LoginModal.vue'
import api from './services/api'

const cards = ref([])
const loading = ref(false)
const isAuthenticated = ref(false)
const showLoginModal = ref(false)

const checkAuth = async () => {
  // 초기 상태는 인증되지 않음
  isAuthenticated.value = false
  
  // localStorage에서 저장된 인증 정보 복원
  const savedAuth = localStorage.getItem('auth_token')
  if (savedAuth) {
    api.defaults.headers.common['Authorization'] = savedAuth
  }
  
  // Authorization 헤더가 있는지 확인
  if (!api.defaults.headers.common['Authorization']) {
    return
  }
  
  // 관리자 인증 확인 전용 엔드포인트로 확인
  try {
    const response = await api.get('/api/cards/check_auth/')
    // 인증 성공 및 관리자 권한 확인
    if (response.data && response.data.authenticated && response.data.is_admin) {
      isAuthenticated.value = true
    } else {
      // 인증은 되었지만 관리자가 아닌 경우
      isAuthenticated.value = false
      delete api.defaults.headers.common['Authorization']
      localStorage.removeItem('auth_token')
    }
  } catch (error) {
    // 인증 실패 (401, 403 등)
    isAuthenticated.value = false
    // Authorization 헤더 제거
    delete api.defaults.headers.common['Authorization']
    // localStorage에서도 제거
    localStorage.removeItem('auth_token')
  }
}

const handleLoginSuccess = () => {
  isAuthenticated.value = true
  loadCards()
}

const handleLogout = () => {
  delete api.defaults.headers.common['Authorization']
  localStorage.removeItem('auth_token')
  isAuthenticated.value = false
}

const loadCards = async () => {
  loading.value = true
  try {
    const response = await cardService.getCards()
    cards.value = response.data.results || response.data
  } catch (error) {
    console.error('카드 목록 로드 실패:', error)
    alert('카드 목록을 불러오는데 실패했습니다.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCards()
  checkAuth()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #667eea;
  --primary-dark: #5568d3;
  --secondary-color: #764ba2;
  --accent-color: #e74c3c;
  --success-color: #28a745;
  --info-color: #17a2b8;
  --danger-color: #dc3545;
  --text-primary: #2c3e50;
  --text-secondary: #6c757d;
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --bg-tertiary: #f5f5f5;
  --border-color: #e0e0e0;
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.16);
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --spacing-xs: 8px;
  --spacing-sm: 12px;
  --spacing-md: 20px;
  --spacing-lg: 30px;
  --spacing-xl: 40px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header Styles */
.app-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  color: white;
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  gap: var(--spacing-md);
}

.site-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.5px;
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-shrink: 0;
}

.btn-login {
  padding: 10px 20px;
  border: 2px solid white;
  border-radius: var(--radius-sm);
  background: transparent;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-login:hover {
  background: white;
  color: var(--primary-color);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.auth-info-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-wrap: nowrap;
}

.auth-status {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  white-space: nowrap;
}

.btn-logout {
  padding: 8px 16px;
  border: 2px solid white;
  border-radius: var(--radius-sm);
  background: transparent;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-logout:hover {
  background: white;
  color: var(--danger-color);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

/* Main Content */
.app-main {
  flex: 1;
  width: 100%;
  padding: var(--spacing-xl) 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  width: 100%;
}

.upload-section {
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.cards-section {
  width: 100%;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  letter-spacing: -0.5px;
}
</style>
