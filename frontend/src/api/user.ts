import config from 'api/config'

const parameter = {
  method: 'GET',
  headers: {
    'Authorization': 'JWT ' + config.token,
    'Content-Type': 'application/json'
  },
}

export async function getProfile() {
  return fetch(config.baseUrl + '/api/profile', parameter)
  .then((res) => {
    console.log(res)
    return res.json()
  })
}
