import Head from 'next/head'
import Link from 'next/link'
import Router from 'next/router'
import config from 'api/config'
import {FollowResponse} from 'utils/type'
import Button from 'components/parts/Button'

interface Props {datas: Array<FollowResponse>}

export default function Follow(props: Props) {
  const {datas} = props
  const is_authenticated = true

  return (
    <>
      <Head>
        <title>MyUsフォロー</title>
      </Head>

      <h1>フォロー
        {/* {% if query %}
        <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section>
        {% endif %} */}
      </h1>

      {is_authenticated ?
        <>
          <div className="follow_button">
            <Button blue size="xs" onClick={() => Router.push('/follower')}>フォロー</Button>
            {/* <span>フォロー数：{data.mypage.following_num}</span> */}
          </div>
          <article className="article_list">
            {datas.map((data) => {
              const imageUrl = config.baseUrl + data.author.image
              const nickname = data.author.nickname
              return (
                <section className="section_follow">
                  <div className="main_decolation">
                    <Link href="/userpage/[nickname]" data-name={nickname} className="follow_box pjax_button_userpage">
                      <object className="author_follow">
                        <Link href="" data-name={nickname} className="pjax_button_userpage">
                          <img src={imageUrl} title={nickname} className="follow_image">
                        </Link>
                      </object>
                      <span title="{{nickname}}" className="follow_content_1">{nickname}</span>
                      <span className="follow_content_2">フォロワー数：{data.mypage.follower_num}</span>
                      <span className="follow_content_3">フォロー数　：{data.mypage.following_num}</span>
                      {/* <object title={data.introduction} className="follow_content_4">
                        {data.introduction}
                      </object> */}
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
    </>
  )
}
