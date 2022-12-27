const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxNTE3NzM0LCJpYXQiOjE2NzEwODU3MzQsImp0aSI6IjVlMDM1MjE4OGJiODQzN2Q5YmI2YjcyMzc2NWMxNDI2IiwidXNlcl9pZCI6NX0.CCZuy0GARxK68Tr5u2dY9mbzhItm4vsFU-DcdZkfJTc'
const BASEURL = process.env.NEXT_PUBLIC_API_URL

const parameter = {
  method: 'GET',
  headers: {
    'Authorization': 'JWT ' + token,
    'Content-Type': 'application/json'
  },
}

export async function getProfile() {
  return fetch(BASEURL + '/api/profile', parameter)
  .then((res) => {
    console.log(res)
    return res.json()
  })
}

// export async function getVideoList() {
//   const res = await fetch(BASEURL + '/api/video')
//   const videos = await res.json()
//   console.log(videos)
//   return {
//     props: {
//       videos: videos,
//     },
//   }
// }
