import { useState, ChangeEvent } from 'react'
import { UnprivilegedEditor } from 'react-quill'
import dynamic from 'next/dynamic'
import { useRouter } from 'next/router'
import { DeltaStatic, Sources } from 'quill'
import { BlogIn } from 'types/internal/media'
import { postBlogCreate } from 'api/internal/media/create'
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

const Quill = dynamic(() => import('components/widgets/Quill'), { ssr: false })

export default function BlogCreate(): JSX.Element {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const [values, setValues] = useState<BlogIn>({ title: '', content: '', richtext: '', delta: '' })

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleQuill = (value: string, _delta: DeltaStatic, _source: Sources, editor: UnprivilegedEditor) => {
    const richtext = value.trim() === '<p><br></p>' ? '' : value.trim()
    setValues({ ...values, richtext, delta: JSON.stringify(editor.getContents()) })
  }

  const handleForm = async () => {
    const { title, content, richtext, image } = values
    if (!isRequiredCheck({ title, content, richtext, image })) return
    handleLoading(true)
    const ret = await postBlogCreate(values)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      handleLoading(false)
      return
    }
    router.push(`/media/blog/${ret.value.id}`)
    handleLoading(false)
  }

  return (
    <Main title="Blog" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="">
          <VStack gap="8">
            <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
            <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
            <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />
            <Quill label="本文" value={values.richtext} className="blog" required={isRequired} onChange={handleQuill} />
          </VStack>
        </form>
      </LoginError>
    </Main>
  )
}
