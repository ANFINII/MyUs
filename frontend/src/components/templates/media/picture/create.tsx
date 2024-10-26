import { useState } from 'react'
import { useRouter } from 'next/router'
import { postPictureCreate } from 'api/internal/media/create'
import { PictureIn } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'
import Vertical from 'components/parts/Vertical/inedex'

export default function PictureCreate() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<PictureIn>({ title: '', content: '' })

  const handleTitle = (title: string) => setValues({ ...values, title })
  const handleContent = (content: string) => setValues({ ...values, content })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleForm = async () => {
    const { title, content, image } = values
    if (!(title && content && image)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postPictureCreate(values)
      router.push(`/media/picture/${data.id}`)
    } catch (e) {
      console.log(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Picture" type="table" buttonArea={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginRequired margin="mt_20">
        <form method="POST" action="">
          <Vertical gap="8">
            <Input label="タイトル" required={isRequired} onChange={handleTitle} />
            <Textarea label="内容" required={isRequired} onChange={handleContent} />
            <InputFile label="画像" accept="image/*" required={isRequired} onChange={handleFile} />
          </Vertical>
        </form>
      </LoginRequired>
    </Main>
  )
}
