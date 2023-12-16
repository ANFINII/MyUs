import Image from 'next/image'
import Link from 'next/link'
import Router from 'next/router'
import config from 'api/config'
import { Mypage } from 'types/internal/auth'
import { Search, Follow } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'

interface Props {
  isAuth: boolean
  search?: Search
  mypage?: Mypage
  datas: Follow[]
}

export default function Followers(props: Props) {
  const { isAuth, search, mypage, datas } = props

  return (
    <Main title="Follower" search={search}>
      {isAuth ? (
        <>
          <div className="follow_button">
            <Button blue size="xs" name="フォロー" onClick={() => Router.push('/menu/follow')} />
            <span>フォロワー数：{mypage ? mypage.followerCount : 0}</span>
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
                        <Link href="/userpage/[nickname]" data-name={nickname} className="pjax_button_userpage">
                          <Image src={imageUrl} title={nickname} className="follow_image" alt="" />
                        </Link>
                      </object>
                      <span title={nickname} className="follow_content_1">
                        {nickname}
                      </span>
                      <span className="follow_content_2">フォロワー数{data.mypage.followerCount}</span>
                      <span className="follow_content_3">フォロー数{data.mypage.followingCount}</span>
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
      ) : (
        <h2 className="login_required">ログインしてください</h2>
      )}
    </Main>
  )
}
