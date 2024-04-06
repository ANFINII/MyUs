import { useState } from 'react'
import { useRouter } from 'next/router'
import { postComicCreate } from 'api/media/post'
import { ComicIn } from 'types/internal/media'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  isAuth: boolean
}

export default function ComicCreate(props: Props) {
  const { isAuth } = props

  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<ComicIn>({ title: '', content: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setData({ ...data, image: files })
  const handleMultiFile = (files: File | File[]) => Array.isArray(files) && setData({ ...data, images: files })

  const handleForm = async () => {
    const title = data.title
    const content = data.content
    const image = data.image
    const images = data.images
    if (!(title && content && image && images)) {
      setIsRequired(true)
      return
    }

    setIsLoading(true)
    const request = { title, content, image, images }
    try {
      const data = await postComicCreate(request)
      router.push(`/media/comic/${data.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Comic">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="" encType="multipart/form-data">
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <InputFile label="サムネイル" accept="image/*" className="mt_16" required={isRequired} onChange={handleFile} />

          <InputFile label="ページ画像" accept="image/*" className="mt_16" required={isRequired} multiple onChange={handleMultiFile} />

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
