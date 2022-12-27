import config from 'pages/api/config'

interface Params {
  path: string
  method: string
  headers?: any
  body?: any
}

export const apiBase = async (params: Params): Promise<any> => {
  const {path, method, headers, body} = params
  const response = await fetch(config.baseUrl + path, {
    method: method,
    credentials: 'include',
    headers: headers,
    body: JSON.stringify(body)
  }).then((response) => {
    return response.json()
  }).catch((err) => {
    console.log(err)
  })
  return response
}
