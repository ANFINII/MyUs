import { useState } from 'react'
import { useRouter } from 'next/router'
import { postPictureCreate } from 'api/media/post'
import { PictureIn } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  isAuth: boolean
}

export default function PictureCreate(props: Props) {
  const { isAuth } = props

  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<PictureIn>({ title: '', content: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setData({ ...data, image: files })

  const handleForm = async () => {
    const title = data.title
    const content = data.content
    const image = data.image
    if (!(title && content && image)) {
      setIsRequired(true)
      return
    }

    setIsLoading(true)
    const request = { title, content, image }
    try {
      const data = await postPictureCreate(request)
      router.push(`/media/picture/${data.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Picture">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="">
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <InputFile label="画像" accept="image/*" className="mt_16" required={isRequired} onChange={handleFile} />

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
