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


import {apiBase} from 'pages/api/api'
import {config} from '@/api/config'
import {userLoginState, userCreateState} from '@/utils/types/state'
import {userCreateReponse, userResponse, usersResponse} from '@/utils/types/response'



export const authMe = async (): Promise<userResponse | undefined> => {
  const params = {
    path: '/api/user/v1/me/admin',
    method: 'GET',
    headers: {
      'x-recustomer-api-key': config().authKey,
      Authorization: 'Bearer ' + config().authToken
    }
  }
  const response = await apiBase(params)
  return response.json()
}


export const loginForm = async (state: userLoginState): Promise<Response> => {
  const url = `${config().baseUrl}/api/auth/v1/login/admin`
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'x-recustomer-api-key': config().authKey
    },
    body: JSON.stringify({
      email: state.mailAddress,
      password: state.password
    })
  })
  return response
}

export const logoutForm = async (): Promise<Response> => {
  const url = `${config().baseUrl}/api/auth/v1/logout`
  const response = await fetch(url, {
    method: 'GET',
    credentials: 'include'
  })
  return response
}

export const userCreate = async (
  state: userCreateState
): Promise<userCreateReponse> => {
  const url = `${config().baseUrl}/api/user/v1/add`
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'x-recustomer-api-key': config().authKey
    },
    body: JSON.stringify({
      first_name: state.firstName,
      last_name: state.lastName,
      email: state.primaryUserEmail,
      password: ''
    })
  })
  return response.json()
}

export const merchantUserCreate = async (
  userId: number,
  merchantId: number
): Promise<Response> => {
  const url = `${config().baseUrl}/api/user/v1/merchant`
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'x-recustomer-api-key': config().authKey
    },
    body: JSON.stringify({
      user_id: userId,
      merchant_id: merchantId,
      is_primary: true
    })
  })
  return response
}

export const merchantUserGet = async (
  merchantId: string
): Promise<usersResponse> => {
  const url = `${config().baseUrl}/api/user/v1/merchant/${merchantId}`
  const response = await fetch(url, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'x-recustomer-api-key': config().authKey,
      Authorization: 'Bearer ' + config().authToken
    }
  })
  return response.json()
}

export const merchantUserUpdate = async (
  merchantUserId: number,
  isPrimary: boolean
): Promise<Response> => {
  const url = `${config().baseUrl}/api/user/v1/merchant/${merchantUserId}`
  const response = await fetch(url, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'x-recustomer-api-key': config().authKey,
      Authorization: 'Bearer ' + config().authToken
    },
    body: JSON.stringify({
      is_primary: isPrimary
    })
  })
  return response
}
