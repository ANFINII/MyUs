import { VideoType } from 'utils/type'


const BASEURL = process.env.NEXT_PUBLIC_API_URL
const parameter = {
  method: 'GET',
  headers: {'Content-Type': 'application/json'},
}

export async function getVideo() {
  const res = await fetch(BASEURL + '/api/video', parameter);
  const items = await res.json();
  return items;
}

export async function getVideoId() {
  const res = await fetch(BASEURL + '/api/video', parameter);
  const items = await res.json();
  return items.map((video: VideoType) => {
    return {
      params: {
        id: String(video.id)
      }
    };
  })
}

export async function getVideoDetail(id: number) {
  const res = await fetch(BASEURL + '/api/video/' + id , parameter);
  const item = await res.json();
  return item
}
