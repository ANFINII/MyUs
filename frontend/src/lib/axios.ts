import axios from 'axios'

const headers = {
  'Content-Type': 'application/json',
}

// axiosの初期設定
export const api = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_API_URL}/api`,
  headers,
})

// レスポンスのエラー判定処理
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.log(error)
    switch (error?.response?.status) {
      case 401:
        break
      case 404:
        break
      default:
        console.log('== internal server error')
    }

    const errorMessage = (error.response?.data?.message || '').split(',')
    throw new Error(errorMessage)
  },
)
