// import axios from 'lib/api/axios'
// import { useEffect, useState } from 'react'
// import Profile from 'pages/account/profile'

// type User = {
//   image: string
//   email: string
//   username: string
//   nickname: string
//   fullname: string
//   year: number
//   month: number
//   day: number
//   age: number
//   gender: string
//   phone: string
//   postal_code: string
//   prefecture: string
//   city: string
//   address: string
//   building: string
//   introduction: string
// }

// const [user, setUser] = useState<User>({
//   image: '',
//   email: '',
//   username: '',
//   nickname: '',
//   fullname: '',
//   year: 0,
//   month: 0,
//   day: 0,
//   age: 0,
//   gender: '',
//   phone: '',
//   postal_code: '',
//   prefecture: '',
//   city: '',
//   address: '',
//   building: '',
//   introduction: '',
// })

// export default function profileAPI() {
//   const url = process.env.NEXT_PUBLIC_API_URL
//   const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MDQ2NjA1LCJqdGkiOiIwNzI5ZjIwZjkwMGM0MzU3YmEwOWYxNzA5Y2QwZDMwNSIsInVzZXJfaWQiOjF9.QKL4zB8Grig3M8_gC1Sgh9NseZOYICy3q0jOBcpJCwU'
//   axios.get(url + '/api/profile', {headers: {'Authorization': 'JWT ' + token}})
//   .then(res => {
//     setUser(res.data)
//     console.log(res)

//     return {user.map(data => <Profile {...data}/>)}
//   })
//   .catch(e => {
//     console.log(e)
//   })
// }

// useEffect(() => {
// },[])
