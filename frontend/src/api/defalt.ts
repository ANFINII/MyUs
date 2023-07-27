// import axios from 'lib/api/axios'

// // ヘッダーがセットされた状態で送信される！！
// // axios.get('localhost:8000/api/user')
// // .then(res => {...})

// export const apiURL = 'http://localhost:8000/api/v1/'

// const Default = () => {
//   const history = useHistory()
//   //ログインしているか否かのstate
//   const isLoggedIn= useSelector(state => state.user.isLoggedIn)
//   const [cookies, setCookie, removeCookie] = useCookies()
//   const dispatch = useDispatch()

//   // AccessToken 更新用
//   async function refreshToken(){
//     axios.post(apiURL+'auth/jwt/refresh',{
//       refresh:cookies.refreshtoken,
//     })
//     .then(res => {
//       console.log("refresh")
//       setCookie('accesstoken', res.data.access, { path: '/' }, { httpOnly: true })
//       setCookie('refreshtoken', res.data.refresh, { path: '/' }, { httpOnly: true })
//     })
//     .catch(err => {
//       alert("ログインしてください")
//       dispatch(isLoggedInOff())
//       history.push('/login')
//     })
//   }

//   // AccessToken 検証用
//   async function verifyAccessToken(){
//     axios.post(apiURL+'auth/jwt/verify',{
//       token:cookies.accesstoken,
//     }).then(res => {
//       console.log("JWT ok")
//     })
//     .catch(err => {
//       if(err.response.status === 401){
//         console.log("verify failed")
//         // 検証結果が401の場合リフレッシュを試す
//         refreshToken()
//       }
//     })
//   }

//   useLayoutEffect(() => {
//     if(isLoggedIn){
//       // isLoggedInがTrueで JWTがある
//       if(cookies.accesstoken !== undefined){
//         console.log("go verify")
//         verifyAccessToken()
//       }
//       // isLoggedInはTrueだが JWTがない
//       else{
//         // ログインページへ遷移 isLoggedInをfalseに
//         console.log("トークンなし")
//         alert("ログインしてください")
//         dispatch(isLoggedInOff())
//         history.push('/login')
//       }
//     }
//   },[])
// }
