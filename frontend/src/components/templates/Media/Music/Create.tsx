import { useState } from 'react'
import { useRouter } from 'next/router'
import { postMusicCreate } from 'api/media/post'
import { MusicIn } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  isAuth: boolean
}

export default function MusicCreate(props: Props) {
  const { isAuth } = props

  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<MusicIn>({ title: '', content: '', lyric: '', download: true })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handleLyric = (lyric: string) => setData({ ...data, lyric })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setData({ ...data, music: files })
  const handleDownload = (checked: boolean) => setData({ ...data, download: checked })

  const handleForm = async () => {
    const title = data.title
    const content = data.content
    const lyric = data.lyric
    const music = data.music
    const download = data.download
    if (!(title && content && lyric && music)) {
      setIsRequired(true)
      return
    }

    setIsLoading(true)
    const request = { title, content, lyric, music, download }
    try {
      const data = await postMusicCreate(request)
      router.push(`/media/music/${data.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Music">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="" encType="multipart/form-data">
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <Textarea label="歌詞" className="mt_16" required={isRequired} onChange={handleLyric} />

          <InputFile label="音楽" accept="audio/*" className="mt_16" required={isRequired} onChange={handleFile} />
          <CheckBox label="ダウンロード許可" className="mt_4" checked onChange={handleDownload} />

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
