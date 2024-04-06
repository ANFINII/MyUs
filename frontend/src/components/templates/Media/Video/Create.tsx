import { useState } from 'react'
import { useRouter } from 'next/router'
import { postVideoCreate } from 'api/media/post'
import { VideoIn } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  isAuth: boolean
}

export default function VideoCreate(props: Props) {
  const { isAuth } = props

  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<VideoIn>({ title: '', content: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setData({ ...data, image: files })
  const handleMovie = (files: File | File[]) => Array.isArray(files) || setData({ ...data, video: files })

  const handleForm = async () => {
    const title = data.title
    const content = data.content
    const image = data.image
    const video = data.video
    if (!(title && content && image && video)) {
      setIsRequired(true)
      return
    }

    setIsLoading(true)
    const request = { title, content, image, video }
    try {
      const data = await postVideoCreate(request)
      router.push(`/media/video/${data.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Video">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="" encType="multipart/form-data">
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <InputFile label="サムネイル" accept="image/*" className="mt_16" required={isRequired} onChange={handleFile} />

          <InputFile label="動画" accept="video/*" className="mt_16" required={isRequired} onChange={handleMovie} />

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
