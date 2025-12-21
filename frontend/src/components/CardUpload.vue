<template>
  <div class="card-upload-container">
    <h2 class="form-title">카드 등록</h2>
    <form @submit.prevent="handleSubmit" class="upload-form">
      <div class="form-group">
        <label for="name">카드명</label>
        <div class="autocomplete-wrapper">
          <input
            id="name"
            v-model="formData.name"
            type="text"
            required
            maxlength="200"
            placeholder="카드 이름을 입력하세요"
            @input="handleCardNameInput"
            @focus="handleCardNameFocus"
            @blur="handleCardNameBlur"
            autocomplete="off"
          />
          <ul v-if="showAutocomplete && autocompleteResults.length > 0" class="autocomplete-list">
            <li
              v-for="(result, index) in autocompleteResults"
              :key="index"
              @mousedown="selectCardName(result.name)"
              :class="{ 'highlighted': index === highlightedIndex }"
              class="autocomplete-item"
            >
              {{ result.name }}
            </li>
          </ul>
        </div>
      </div>

      <div class="form-group">
        <label for="serial_number">카드 시리얼</label>
        <input
          id="serial_number"
          v-model="formData.serial_number"
          type="text"
          maxlength="50"
          placeholder="예: ICP-0001, DACP-0893"
        />
      </div>

      <div class="form-group">
        <label for="image">카드 이미지</label>
        <input
          id="image"
          type="file"
          accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
          @change="handleImageChange"
          required
        />
        <div v-if="imagePreview" class="image-preview">
          <img :src="imagePreview" alt="미리보기" />
        </div>
      </div>

      <div class="form-group">
        <label for="condition">상태</label>
        <select id="condition" v-model="formData.condition" required>
          <option value="S">S급</option>
          <option value="A">A급</option>
          <option value="B">B급</option>
          <option value="C">C급</option>
        </select>
      </div>

      <div class="form-group">
        <label for="rarity">레어리티</label>
        <select id="rarity" v-model="formData.rarity" required>
          <option value="N">노멀(N)</option>
          <option value="R">레어(R)</option>
          <option value="SR">슈퍼 레어(SR)</option>
          <option value="UR">울트라 레어(UR)</option>
          <option value="SE">시크릿 레어(SE)</option>
          <option value="UL">얼티미트 레어(UL)</option>
          <option value="HR">홀로그래픽 레어(HR)</option>
        </select>
      </div>

      <div class="form-group">
        <label for="price">판매 가격</label>
        <div class="price-input-container">
          <input
            id="price"
            v-model.number="formData.price"
            type="number"
            min="0"
            required
            placeholder="가격을 입력하세요"
            class="price-input"
          />
          <div class="price-buttons">
            <button type="button" @click="addPrice(10000)" class="price-btn">+10,000</button>
            <button type="button" @click="addPrice(5000)" class="price-btn">+5,000</button>
            <button type="button" @click="addPrice(1000)" class="price-btn">+1,000</button>
            <button type="button" @click="addPrice(100)" class="price-btn">+100</button>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? '등록 중...' : '카드 등록' }}
        </button>
        <button type="button" @click="resetForm" class="btn-secondary">
          초기화
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { cardService } from '../services/api'

const emit = defineEmits(['card-created'])

const formData = ref({
  name: '',
  serial_number: '',
  condition: 'A',
  rarity: 'N',
  price: 0,
})

const imageFile = ref(null)
const imagePreview = ref(null)
const loading = ref(false)
const autocompleteResults = ref([])
const showAutocomplete = ref(false)
const highlightedIndex = ref(-1)
const allCardNames = ref([]) // 모든 카드명 목록 (클라이언트 사이드 검색용)
let autocompleteTimeout = null

// 페이지 진입 시 모든 카드명 로드
onMounted(async () => {
  try {
    const response = await cardService.getAllCardNames()
    allCardNames.value = response.data.card_names || []
    console.log(`카드명 ${allCardNames.value.length}개 로드 완료`)
  } catch (error) {
    console.error('카드명 로드 실패:', error)
  }
})

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (!file) {
    return
  }
  
  // 파일 크기 검증 (20MB 제한)
  const maxSize = 20 * 1024 * 1024 // 20MB
  if (file.size > maxSize) {
    alert('이미지 파일 크기는 20MB 이하여야 합니다.')
    event.target.value = '' // 파일 선택 초기화
    return
  }
  
  // 파일 타입 검증
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    alert('허용된 이미지 형식: JPG, PNG, GIF, WEBP')
    event.target.value = '' // 파일 선택 초기화
    return
  }
  
  // 파일 확장자 검증
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
  const fileExt = '.' + file.name.split('.').pop().toLowerCase()
  if (!allowedExtensions.includes(fileExt)) {
    alert('허용된 이미지 형식: JPG, PNG, GIF, WEBP')
    event.target.value = '' // 파일 선택 초기화
    return
  }
  
  imageFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleSubmit = async () => {
  if (!imageFile.value) {
    alert('이미지를 선택해주세요.')
    return
  }
  
  // 입력 검증
  if (!formData.value.name || !formData.value.name.trim()) {
    alert('카드명을 입력해주세요.')
    return
  }
  
  if (formData.value.name.length > 200) {
    alert('카드명은 200자 이하여야 합니다.')
    return
  }
  
  if (!formData.value.condition) {
    alert('상태를 선택해주세요.')
    return
  }
  
  if (!formData.value.price || formData.value.price < 0) {
    alert('올바른 가격을 입력해주세요.')
    return
  }
  
  if (formData.value.price > 9999999999) {
    alert('가격이 너무 큽니다.')
    return
  }

  loading.value = true

  try {
    const formDataToSend = new FormData()
    formDataToSend.append('name', formData.value.name)
    if (formData.value.serial_number) {
      formDataToSend.append('serial_number', formData.value.serial_number)
    }
    formDataToSend.append('image', imageFile.value)
    formDataToSend.append('condition', formData.value.condition)
    formDataToSend.append('rarity', formData.value.rarity)
    formDataToSend.append('price', formData.value.price)
    formDataToSend.append('sale_status', 'available')

    await cardService.createCard(formDataToSend)
    resetForm()
    emit('card-created')
  } catch (error) {
    console.error('카드 등록 실패:', error)
    let errorMessage = '카드 등록에 실패했습니다.'
    
    if (error.response) {
      const status = error.response.status
      const data = error.response.data
      
      if (status === 403 || status === 401) {
        errorMessage = '권한이 없습니다. 관리자로 로그인해주세요.'
      } else if (status === 400) {
        const fieldErrors = []
        for (const [field, messages] of Object.entries(data)) {
          if (Array.isArray(messages)) {
            fieldErrors.push(`${field}: ${messages.join(', ')}`)
          } else {
            fieldErrors.push(`${field}: ${messages}`)
          }
        }
        errorMessage = `입력 오류:\n${fieldErrors.join('\n')}`
      } else if (data.detail) {
        errorMessage = data.detail
      } else if (data.message) {
        errorMessage = data.message
      }
    } else if (error.request) {
      errorMessage = '서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.'
    }
    
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

const handleCardNameInput = (event) => {
  const query = event.target.value.trim()
  
  // 기존 타이머 취소
  if (autocompleteTimeout) {
    clearTimeout(autocompleteTimeout)
  }
  
  if (query.length < 1) {
    autocompleteResults.value = []
    showAutocomplete.value = false
    return
  }
  
  // 클라이언트 사이드에서 즉시 검색 (디바운싱 제거 또는 최소화)
  autocompleteTimeout = setTimeout(() => {
    if (allCardNames.value.length === 0) {
      // 카드명이 아직 로드되지 않은 경우 서버 검색으로 폴백
      searchCardNamesFromServer(query)
      return
    }
    
    // 클라이언트 사이드 검색 (대소문자 구분 없음, 부분 일치)
    const queryLower = query.toLowerCase()
    const filtered = allCardNames.value
      .filter(name => name.toLowerCase().includes(queryLower))
      .slice(0, 20) // 최대 20개만 표시
    
    autocompleteResults.value = filtered.map(name => ({ name }))
    showAutocomplete.value = filtered.length > 0
    highlightedIndex.value = -1
  }, 50) // 매우 짧은 딜레이 (입력 반응성 향상)
}

// 서버 검색 (폴백용)
const searchCardNamesFromServer = async (query) => {
  try {
    const response = await cardService.searchCardNames(query)
    autocompleteResults.value = response.data.results || []
    showAutocomplete.value = autocompleteResults.value.length > 0
    highlightedIndex.value = -1
  } catch (error) {
    console.error('카드명 검색 실패:', error)
    autocompleteResults.value = []
    showAutocomplete.value = false
  }
}

const handleCardNameFocus = () => {
  if (autocompleteResults.value.length > 0) {
    showAutocomplete.value = true
  }
}

const handleCardNameBlur = () => {
  // 클릭 이벤트가 발생할 수 있도록 약간의 지연
  setTimeout(() => {
    showAutocomplete.value = false
  }, 200)
}

const selectCardName = (cardName) => {
  formData.value.name = cardName
  showAutocomplete.value = false
  autocompleteResults.value = []
}

const addPrice = (amount) => {
  formData.value.price = (formData.value.price || 0) + amount
}

const resetForm = () => {
  formData.value = {
    name: '',
    serial_number: '',
    condition: 'A',
    rarity: 'N',
    price: 0,
  }
  imageFile.value = null
  imagePreview.value = null
}
</script>

<style scoped>
.card-upload-container {
  width: 100%;
}

.form-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  letter-spacing: -0.5px;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  width: 100%;
}

.form-group label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.form-group input,
.form-group select {
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  transition: all 0.3s ease;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input::placeholder {
  color: var(--text-secondary);
}

.autocomplete-wrapper {
  position: relative;
  width: 100%;
  max-width: 100%;
}

.autocomplete-wrapper input {
  width: 100%;
  min-width: 100%;
  box-sizing: border-box;
}

.autocomplete-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-top: none;
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  margin: 0;
  padding: 0;
  list-style: none;
  box-shadow: var(--shadow-md);
}

.autocomplete-item {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 14px;
}

.autocomplete-item:last-child {
  border-bottom: none;
}

.autocomplete-item:hover,
.autocomplete-item.highlighted {
  background: var(--primary-color);
  color: white;
}

.price-input-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.price-input {
  width: 100%;
}

.price-buttons {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

.price-btn {
  padding: 8px 16px;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  min-width: 80px;
}

.price-btn:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.image-preview {
  margin-top: var(--spacing-xs);
  max-width: 300px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 2px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.image-preview img {
  width: 100%;
  height: auto;
  display: block;
}

.form-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-xs);
}

.btn-primary,
.btn-secondary {
  padding: 14px 28px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.3px;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
  flex: 1;
  box-shadow: var(--shadow-sm);
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

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--border-color);
  border-color: var(--text-secondary);
}
</style>
