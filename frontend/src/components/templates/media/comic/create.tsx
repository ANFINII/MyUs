import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { ComicIn } from 'types/internal/media'
import { postComicCreate } from 'api/internal/media/create'
import { FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import VStack from 'components/parts/Stack/Vertical'

export default function ComicCreate(): React.JSX.Element {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const [values, setValues] = useState<ComicIn>({ title: '', content: '' })

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleMultiFile = (files: File | File[]) => Array.isArray(files) && setValues({ ...values, images: files })

  const handleForm = async () => {
    const { title, content, image, images } = values
    if (!isRequiredCheck({ title, content, image, images })) return
    handleLoading(true)
    const ret = await postComicCreate(values)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      handleLoading(false)
      return
    }
    router.push(`/media/comic/${ret.value.id}`)
    handleLoading(false)
  }

  return (
    <Main title="Comic" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="" encType="multipart/form-data">
          <VStack gap="8">
            <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
            <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
            <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />
            <InputFile label="ページ画像" accept="image/*" required={isRequired} multiple onChange={handleMultiFile} />
          </VStack>
        </form>
      </LoginError>
    </Main>
  )
}
