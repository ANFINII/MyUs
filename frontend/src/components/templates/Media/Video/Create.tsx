import { useState } from 'react'
import { useRouter } from 'next/router'
import { postVideoCreate } from 'api/internal/media/create'
import { VideoIn } from 'types/internal/media'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

export default function VideoCreate() {
  const router = useRouter()
  const { user } = useUser()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<VideoIn>({ title: '', content: '' })

  const handleTitle = (title: string) => setValues({ ...values, title })
  const handleContent = (content: string) => setValues({ ...values, content })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleMovie = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, video: files })

  const handleForm = async () => {
    const { title, content, image, video } = values
    if (!(title && content && image && video)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postVideoCreate(values)
      router.push(`/media/video/${data.id}`)
    } catch (e) {
      console.log(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Video" type="table" buttonArea={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginRequired isAuth={user.isActive} margin="mt_20">
        <form method="POST" action="" encType="multipart/form-data" className="create_grid">
          <Input label="タイトル" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" required={isRequired} onChange={handleContent} />

          <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />

          <InputFile label="動画" accept="video/*" required={isRequired} onChange={handleMovie} />
        </form>
      </LoginRequired>
    </Main>
  )
}
