import { useState, ChangeEvent } from 'react'
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

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleMovie = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, video: files })

  const handleForm = async () => {
    const { title, content, image, video } = values
    if (!(title && content && image && video)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    const ret = await postVideoCreate(values)
    if (ret.isErr()) return handleToast('エラーが発生しました！', true)
    router.push(`/media/video/${ret.value.id}`)
    setIsLoading(false)
  }

  return (
    <Main title="Video" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="" encType="multipart/form-data">
          <Vertical gap="8">
            <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
            <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
            <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />
            <InputFile label="動画" accept="video/*" required={isRequired} onChange={handleMovie} />
          </Vertical>
        </form>
      </LoginError>
    </Main>
  )
}
