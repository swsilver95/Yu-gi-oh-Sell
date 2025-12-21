<template>
  <div class="card-grid-container">
    <div class="card-grid">
      <div
        v-for="card in cards"
        :key="card.id"
        class="card-item"
        :class="{ 
          'sold': card.sale_status === 'sold',
          'reserved': card.sale_status === 'reserved'
        }"
      >
        <div class="card-image-wrapper">
          <img
            :src="card.image_optimized_url || card.image_url"
            :alt="card.name"
            class="card-image"
          />
          <div v-if="card.sale_status === 'sold'" class="sold-overlay">
            <span class="sold-text">판매완료</span>
          </div>
          <div v-if="card.sale_status === 'reserved'" class="reserved-overlay">
            <span class="reserved-text">예약중</span>
          </div>
          <div v-if="isAdmin" class="admin-actions">
            <button
              v-if="card.sale_status === 'available'"
              @click="markAsSold(card.id)"
              class="action-btn btn-sold"
              title="판매완료 처리"
            >
              판매완료
            </button>
            <button
              v-else-if="card.sale_status === 'sold'"
              @click="markAsAvailable(card.id)"
              class="action-btn btn-available"
              title="판매중으로 변경"
            >
              판매중
            </button>
            <button
              v-else-if="card.sale_status === 'reserved'"
              @click="markAsAvailable(card.id)"
              class="action-btn btn-available"
              title="판매중으로 변경"
            >
              판매중
            </button>
            <button
              v-if="card.sale_status === 'available'"
              @click="markAsReserved(card.id)"
              class="action-btn btn-reserved"
              title="예약중 처리"
            >
              예약중
            </button>
            <button
              @click="deleteCard(card.id)"
              class="action-btn btn-delete"
              title="카드 삭제"
            >
              삭제
            </button>
          </div>
        </div>
                <div class="card-info">
                  <h3 class="card-name">{{ card.name }}</h3>
                  <div v-if="card.serial_number" class="card-serial">
                    {{ card.serial_number }}
                  </div>
                  <div class="card-details">
            <div class="card-badges">
              <span class="card-condition" :class="`condition-${card.condition.toLowerCase()}`">
                {{ card.condition_display }}
              </span>
              <span class="card-rarity" :class="`rarity-${card.rarity.toLowerCase()}`">
                {{ card.rarity }}
              </span>
            </div>
            <span class="card-price">{{ formatPrice(card.price) }}원</span>
          </div>
          <div class="card-status">
            <span class="status-badge" :class="card.sale_status">
              {{ card.sale_status_display }}
            </span>
          </div>
        </div>
      </div>
    </div>
    <div v-if="cards.length === 0" class="empty-state">
      등록된 카드가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { cardService } from '../services/api'

const props = defineProps({
  cards: {
    type: Array,
    required: true,
    default: () => [],
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['card-updated'])

const formatPrice = (price) => {
  return new Intl.NumberFormat('ko-KR').format(price)
}

const markAsSold = async (cardId) => {
  try {
    await cardService.markAsSold(cardId)
    emit('card-updated')
  } catch (error) {
    console.error('판매완료 처리 실패:', error)
    alert('판매완료 처리에 실패했습니다.')
  }
}

const markAsAvailable = async (cardId) => {
  try {
    await cardService.markAsAvailable(cardId)
    emit('card-updated')
  } catch (error) {
    console.error('판매중 변경 실패:', error)
    alert('판매중 변경에 실패했습니다.')
  }
}

const markAsReserved = async (cardId) => {
  try {
    await cardService.markAsReserved(cardId)
    emit('card-updated')
  } catch (error) {
    console.error('예약중 처리 실패:', error)
    alert('예약중 처리에 실패했습니다.')
  }
}

const deleteCard = async (cardId) => {
  if (!confirm('이 카드를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
    return
  }
  
  try {
    await cardService.deleteCard(cardId)
    emit('card-updated')
  } catch (error) {
    console.error('카드 삭제 실패:', error)
    alert('카드 삭제에 실패했습니다.')
  }
}
</script>

<style scoped>
.card-grid-container {
  width: 100%;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  width: 100%;
}

/* 반응형 디자인 */
@media (min-width: 1400px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1024px) and (max-width: 1399px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-sm);
  }
}

@media (min-width: 480px) and (max-width: 767px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-sm);
  }
}

@media (max-width: 479px) {
  .card-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }
}

.card-item {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
}

.card-item:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-color);
}

.card-item.sold {
  opacity: 0.75;
}

.card-item.reserved {
  opacity: 0.85;
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  padding-top: 140%;
  background: var(--bg-tertiary);
  overflow: hidden;
}

.card-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.card-item:hover .card-image {
  transform: scale(1.05);
}

.sold-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.sold-text {
  color: white;
  font-size: 28px;
  font-weight: 700;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
  letter-spacing: 2px;
}

.reserved-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 193, 7, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.reserved-text {
  color: white;
  font-size: 28px;
  font-weight: 700;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
  letter-spacing: 2px;
}

.admin-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 3;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card-item:hover .admin-actions {
  opacity: 1;
}

.action-btn {
  padding: 8px 14px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: var(--shadow-sm);
  letter-spacing: 0.3px;
}

.action-btn:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

.btn-sold {
  background: var(--success-color);
  color: white;
}

.btn-sold:hover {
  background: #218838;
}

.btn-available {
  background: var(--info-color);
  color: white;
}

.btn-available:hover {
  background: #138496;
}

.btn-reserved {
  background: #ffc107;
  color: #000;
}

.btn-reserved:hover {
  background: #e0a800;
}

.btn-delete {
  background: var(--danger-color);
  color: white;
}

.btn-delete:hover {
  background: #c82333;
}

.card-info {
  padding: var(--spacing-sm);
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.card-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.card-serial {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
  margin-bottom: 4px;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.card-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-xs);
}

.card-badges {
  display: flex;
  gap: 6px;
  align-items: center;
}

.card-condition {
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.condition-s {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.condition-a {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.condition-b {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.condition-c {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.card-rarity {
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
}

.rarity-n { background: #6c757d; }
.rarity-r { background: #17a2b8; }
.rarity-sr { background: #ffc107; color: #343a40; }
.rarity-ur { background: #fd7e14; }
.rarity-se { background: #e83e8c; }
.rarity-ul { background: #6f42c1; }
.rarity-hr { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }

.card-price {
  font-size: 18px;
  font-weight: 700;
  color: var(--accent-color);
  letter-spacing: -0.3px;
}

.card-status {
  margin-top: auto;
  padding-top: var(--spacing-xs);
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.status-badge.available {
  background: #d4edda;
  color: #155724;
}

.status-badge.reserved {
  background: #fff3cd;
  color: #856404;
}

.status-badge.sold {
  background: #f8d7da;
  color: #721c24;
}

.empty-state {
  text-align: center;
  padding: 80px var(--spacing-md);
  color: var(--text-secondary);
  font-size: 18px;
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
</style>
