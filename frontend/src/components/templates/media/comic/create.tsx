import { useState } from 'react'
import { useRouter } from 'next/router'
import { ComicIn } from 'types/internal/media'
import { postComicCreate } from 'api/internal/media/create'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import Vertical from 'components/parts/Stack/Vertical'

export default function ComicCreate() {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<ComicIn>({ title: '', content: '' })

  const handleTitle = (title: string) => setValues({ ...values, title })
  const handleContent = (content: string) => setValues({ ...values, content })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleMultiFile = (files: File | File[]) => Array.isArray(files) && setValues({ ...values, images: files })

  const handleForm = async () => {
    const { title, content, image, images } = values
    if (!(title && content && image && images)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postComicCreate(values)
      router.push(`/media/comic/${data.id}`)
    } catch {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Comic" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="" encType="multipart/form-data">
          <Vertical gap="8">
            <Input label="タイトル" required={isRequired} onChange={handleTitle} />
            <Textarea label="内容" required={isRequired} onChange={handleContent} />
            <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />
            <InputFile label="ページ画像" accept="image/*" required={isRequired} multiple onChange={handleMultiFile} />
          </Vertical>
        </form>
      </LoginError>
    </Main>
  )
}
