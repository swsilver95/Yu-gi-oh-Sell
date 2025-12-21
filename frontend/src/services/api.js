import axios from 'axios'

// API base URL - 프로덕션에서는 현재 도메인 사용
const getBaseURL = () => {
  if (typeof window !== 'undefined') {
    // 브라우저 환경에서는 현재 호스트 사용
    return window.location.origin
  }
  // 서버 사이드 렌더링 등
  return 'http://localhost:8000'
}

const api = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // 세션 쿠키를 포함하기 위해
})

export const cardService = {
  // 모든 카드 조회
  getCards() {
    return api.get('/api/cards/')
  },
  
  // 카드 상세 조회
  getCard(id) {
    return api.get(`/api/cards/${id}/`)
  },
  
  // 카드 생성 (이미지 업로드 포함)
  createCard(formData) {
    // multipart/form-data는 Content-Type 헤더를 제거해야 브라우저가 boundary를 자동 설정함
    return api.post('/api/cards/', formData, {
      headers: {
        // Content-Type을 명시하지 않으면 axios가 자동으로 multipart/form-data로 설정하고 boundary를 추가함
        // Authorization 헤더는 api 인스턴스에 이미 설정되어 있음
      },
      transformRequest: [
        (data, headers) => {
          // FormData를 사용할 때는 Content-Type을 제거하여 브라우저가 boundary를 자동 설정하도록 함
          if (data instanceof FormData) {
            delete headers['Content-Type']
          }
          return data
        }
      ],
    })
  },
  
  // 카드 수정
  updateCard(id, formData) {
    return api.patch(`/api/cards/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  
  // 카드 삭제
  deleteCard(id) {
    return api.delete(`/api/cards/${id}/`)
  },
  
  // 판매 완료로 표시
  markAsSold(id) {
    return api.patch(`/api/cards/${id}/mark_as_sold/`)
  },
  
  // 판매중으로 표시
  markAsAvailable(id) {
    return api.patch(`/api/cards/${id}/mark_as_available/`)
  },
  
  // 예약중으로 표시
  markAsReserved(id) {
    return api.patch(`/api/cards/${id}/mark_as_reserved/`)
  },
  
  // 카드명 자동완성 검색 (레거시 - 사용하지 않음)
  searchCardNames(query) {
    return api.get('/api/cards/search_card_names/', {
      params: { q: query }
    })
  },
  
  // 모든 카드명 목록 가져오기 (클라이언트 사이드 검색용)
  getAllCardNames() {
    return api.get('/api/cards/get_all_card_names/')
  },
}

export default api
