import axios from 'axios'
// import Cookies from 'js-cookie'

axios.defaults.withCredentials = true
// const token = Cookies.get('user_token')
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxNTIzMjM5LCJpYXQiOjE2NzEwOTEyMzksImp0aSI6ImYyMDliY2RhOGM1NjQzMjdiMzk5NDhkNTdjYjkyNDIzIiwidXNlcl9pZCI6MX0.hdIKDXLocFhnp_6StHiDLGCYam5f-TqHfcKnttCG1H8'
// console.log(token)
const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Authorization': 'JWT ' + token,
    'Content-Type': 'application/json'
  },
  timeout: 10000,
})

export default instance
