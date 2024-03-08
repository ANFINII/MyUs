import { useState } from 'react'
import { useRouter } from 'next/router'
import { postPictureCreate } from 'api/media/post'
import { CreatePcture } from 'types/internal/media'
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
  const [create, setCreate] = useState<CreatePcture>({ title: '', content: '' })

  const handleTitle = (title: string) => setCreate({ ...create, title })
  const handleContent = (content: string) => setCreate({ ...create, content })
  const handleFile = (image: File) => setCreate({ ...create, image })

  const handleForm = async () => {
    setIsLoading(true)
    try {
      const picture = await postPictureCreate(create)
      router.push(`media/picture/${picture.id}`)
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
          <p className="mv_16">タイトル</p>
          <Input name="title" value={create.title} onChange={handleTitle} required />

          <p className="mv_16">内容</p>
          <Textarea name="content" value={create.content} onChange={handleContent} required></Textarea>

          <p className="mv_16">画像</p>
          <InputFile id="file_1" accept="image/*" onChange={handleFile} required />

          <Button color="green" name="作成する" loading={isLoading} onClick={handleForm} className="mt_32" />
        </form>
      </LoginRequired>
    </Main>
  )
}
