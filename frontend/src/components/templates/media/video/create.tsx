import { useState } from 'react'
import { useRouter } from 'next/router'
import { VideoIn } from 'types/internal/media'
import { postVideoCreate } from 'api/internal/media/create'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import Vertical from 'components/parts/Stack/Vertical'

export default function VideoCreate(): JSX.Element {
  const router = useRouter()
  const { toast, handleToast } = useToast()
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
    } catch {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Video" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="" encType="multipart/form-data">
          <Vertical gap="8">
            <Input label="タイトル" required={isRequired} onChange={handleTitle} />
            <Textarea label="内容" required={isRequired} onChange={handleContent} />
            <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />
            <InputFile label="動画" accept="video/*" required={isRequired} onChange={handleMovie} />
          </Vertical>
        </form>
      </LoginError>
    </Main>
  )
}
