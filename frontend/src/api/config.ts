const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxNTE3NzM0LCJpYXQiOjE2NzEwODU3MzQsImp0aSI6IjVlMDM1MjE4OGJiODQzN2Q5YmI2YjcyMzc2NWMxNDI2IiwidXNlcl9pZCI6NX0.CCZuy0GARxK68Tr5u2dY9mbzhItm4vsFU-DcdZkfJTc'

const config = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL,
  token: 'JWT ' + token
}
export default config
