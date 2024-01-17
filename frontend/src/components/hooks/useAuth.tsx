// import { useRouter } from 'next/router'
// import { HttpStatusCode } from 'axios'
// import { useUserMeStore } from 'stores/userMe'
// import { apiAuthClient } from 'lib/axios'
// import { AUTH_NO_PATHS } from 'lib/config'
// import { UserMe } from 'types/internal/auth'
// import { apiUserMeV2 } from 'utils/constants/schemas/auth'

// interface UseUserMeHooks {
//   updateUserMe: () => Promise<void>
// }

// export const useUserMe = (): UseUserMeHooks => {
//   const { userMe, setUserMe } = useUserMeStore()
//   const router = useRouter()

//   const updateUserMe = async (): Promise<void> => {
//     if (AUTH_NO_PATHS.includes(router.pathname)) return

//     await apiAuthClient
//       .get(apiUserMeV2)
//       .then((res) => {
//         if (res.status !== HttpStatusCode.Ok) {
//           router.replace('/login')
//         }

//         const userMeResponse = res.data as UserMe
//         if (userMe?.id === userMeResponse.id) {
//           return
//         }
//         setUserMe(userMeResponse)
//       })
//       .catch(() => {
//         router.replace('/login')
//       })
//   }

//   return { updateUserMe }
// }
