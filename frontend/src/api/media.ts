import config from 'api/config'
import { Video } from 'types/media'

const parameter = {
  method: 'GET',
  headers: { 'Content-Type': 'application/json' },
}

export async function getVideo() {
  const res = await fetch(config.baseUrl + '/api/video', parameter)
  const items = await res.json()
  return items
}

export async function getVideoId() {
  const res = await fetch(config.baseUrl + '/api/video', parameter)
  const items = await res.json()
  return items.map((video: Video) => {
    return {
      params: {
        id: String(video.id),
      },
    }
  })
}

export async function getVideoDetail(id: number) {
  const res = await fetch(config.baseUrl + '/api/video/' + id, parameter)
  const item = await res.json()
  return item
}
