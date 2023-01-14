import Head from 'next/head'
import MusicArticle from 'components/elements/Article/Music'

export default function Music() {
  const datas = [
    {
        "id": 1,
        "title": "音楽テスト1",
        "content": "音楽テスト1",
        "lyric": "音楽テスト1",
        "music": "/media/musics/user_1/object_1/02-%E6%8C%87%E8%B7%A1%E3%83%8F%E3%83%BC%E3%83%88_Instrumetal.mp3",
        "like": 0,
        "read": 102,
        "comment_num": 0,
        "download": true,
        "publish": true,
        "created": "2022-01-01T00:00:00Z",
        "updated": "2022-01-01T00:00:00Z",
        "author": {
            "id": 1,
            "nickname": "アンさん",
            "image": "/media/users/images_user/user_1/An_Okina.jpg"
        }
    },
    {
        "id": 2,
        "title": "音楽テスト2",
        "content": "音楽テスト2",
        "lyric": "音楽テスト2",
        "music": "/media/musics/user_2/object_2/02-%E6%8C%87%E8%B7%A1%E3%83%8F%E3%83%BC%E3%83%88_Instrumetal.mp3",
        "like": 1,
        "read": 102,
        "comment_num": 0,
        "download": true,
        "publish": true,
        "created": "2022-01-01T00:00:00Z",
        "updated": "2022-01-01T00:00:00Z",
        "author": {
            "id": 2,
            "nickname": "ショウエン",
            "image": "/media/users/images_user/user_2/MyUs_Profile_02.jpg"
        }
    },
    {
        "id": 3,
        "title": "音楽テスト3",
        "content": "音楽テスト3",
        "lyric": "音楽テスト3",
        "music": "/media/musics/user_3/object_3/02-%E6%8C%87%E8%B7%A1%E3%83%8F%E3%83%BC%E3%83%88_Instrumetal.mp3",
        "like": 0,
        "read": 101,
        "comment_num": 0,
        "download": true,
        "publish": true,
        "created": "2022-01-01T00:00:00Z",
        "updated": "2022-01-01T00:00:00Z",
        "author": {
            "id": 3,
            "nickname": "ソウヒ",
            "image": "/media/users/images_user/user_3/MyUs_Profile_03.jpg"
        }
    },
    {
        "id": 4,
        "title": "音楽テスト4",
        "content": "音楽テスト4",
        "lyric": "音楽テスト4",
        "music": "/media/musics/user_4/object_4/02-%E6%8C%87%E8%B7%A1%E3%83%8F%E3%83%BC%E3%83%88_Instrumetal.mp3",
        "like": 0,
        "read": 101,
        "comment_num": 0,
        "download": true,
        "publish": true,
        "created": "2022-01-01T00:00:00Z",
        "updated": "2022-01-01T00:00:00Z",
        "author": {
            "id": 4,
            "nickname": "ケイマ",
            "image": "/media/users/images_user/user_4/MyUs_Profile_04.jpg"
        }
    },
    {
        "id": 5,
        "title": "音楽テスト5",
        "content": "音楽テスト5",
        "lyric": "音楽テスト5",
        "music": "/media/musics/user_5/object_5/02-%E6%8C%87%E8%B7%A1%E3%83%8F%E3%83%BC%E3%83%88_Instrumetal.mp3",
        "like": 0,
        "read": 101,
        "comment_num": 0,
        "download": true,
        "publish": true,
        "created": "2022-01-01T00:00:00Z",
        "updated": "2022-01-01T00:00:00Z",
        "author": {
            "id": 5,
            "nickname": "アン",
            "image": "/media/users/images_user/user_5/MyUs_Profile_01.jpg"
        }
    }
]
  return (
    <>
      <Head>
        <title>MyUsミュージック</title>
      </Head>

      <h1>Music
        {/* {% if query %}
        <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section>
        {% endif %} */}
      </h1>

      <MusicArticle datas={datas} />
    </>
  )
}
