import Link from 'next/link'
import Image from 'next/image'
import Router from 'next/router'
import {Query, MypageResponse, FollowResponse} from 'utils/type'
import config from 'api/config'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'

interface Props {
  is_authenticated: boolean
  query?: Query
  mypage?: MypageResponse
  datas: FollowResponse[]
}

export default function FollowList(props: Props) {
  const {is_authenticated, query, mypage, datas} = props
  return (
    <Main title="MyUsフォロー" hero="Follow" query={query}>
      {is_authenticated ?
        <>
          <div className="follow_button">
            <Button blue size="xs" onClick={() => Router.push('/menu/follower')}>フォロー</Button>
            <span>フォロー数：{mypage? mypage.following_count : 0}</span>
          </div>
          <article className="article_list">
            {datas.map((data) => {
              const imageUrl = config.baseUrl + data.author.image
              const nickname = data.author.nickname
              return (
                <section className="section_follow" key={data.id}>
                  <div className="main_decolation">
                    <Link href="/userpage/[nickname]" data-name={nickname} className="follow_box pjax_button_userpage">
                      <object className="author_follow">
                        <Link href="" data-name={nickname} className="pjax_button_userpage">
                          <Image src={imageUrl} title={nickname} className="follow_image" alt="" />
                        </Link>
                      </object>
                      <span title={nickname} className="follow_content_1">{nickname}</span>
                      <span className="follow_content_2">フォロワー数：{data.mypage.follower_count}</span>
                      <span className="follow_content_3">フォロー数　：{data.mypage.following_count}</span>
                      <object title={data.introduction} className="follow_content_4">
                        {data.introduction}
                      </object>
                    </Link>
                  </div>
                </section>
              )
            })}
          </article>
        </>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </Main>
  )
}
