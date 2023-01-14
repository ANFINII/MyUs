import config from 'api/config'

export const fetchCurrentUser = async () => {
  try {
    const user = await tokenToUser()
    return user
  } catch (e) {
    // tokenの有効期限が切れていたら refreshを試みる
    if (e['error'] === 'Activations link expired') {
      const refresh = await refreshToken()
      const newRefresh = await newToken(refresh)

      if (newRefresh['access']) {
        // refresh に成功したら再度 access tokenでのユーザー取得を試みる
        const user = await tokenToUser()
        return user
      }
    }
  }
}

// tokenからuser情報を取得
const tokenToUser = async () => {
  const res = await fetch(`${config.baseUrl}/api/user/`, {
    credentials: 'include',
  })
  const ret = await res.json()
  if (res.status === 400) {
    throw ret
  }
  return ret
}

// refresh tokenをもらう
export const getRefreshToken = async () => {
  const res = await fetch(`${config.baseUrl}/api/user/refresh/`, {
    credentials: 'include',
  })
  const ret = await res.json()
  return ret
}

// refresh tokenから 新しい access tokenを生成
const newToken = async (refresh: any) => {
  const res = await fetch(`${config.baseUrl}/api/user/refresh/token/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json charset=utf-8',
      'X-CSRFToken': csrf['token'],
    },
    body: JSON.stringify(refresh),
  })
  const ret = await res.json()
  destroyCookie(null, 'csrftoken')
  return ret
}
