import { TOKEN } from 'lib/config'

const parameter = {
  method: 'GET',
  headers: {
    Authorization: 'JWT ' + TOKEN,
    'Content-Type': 'application/json',
  },
}

export async function getProfile() {
  return fetch('/api/profile', parameter).then((res) => {
    console.log(res)
    return res.json()
  })
}
