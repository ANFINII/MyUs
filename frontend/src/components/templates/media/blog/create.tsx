import React, { useState } from 'react'
import { UnprivilegedEditor } from 'react-quill'
import dynamic from 'next/dynamic'
import { useRouter } from 'next/router'
import { DeltaStatic, Sources } from 'quill'
import { postBlogCreate } from 'api/internal/media/create'
import { BlogIn } from 'types/internal/media'
import { MentionUser } from 'types/internal/timeline'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

const Quill = dynamic(() => import('components/widgets/Quill'), { ssr: false })

const users: MentionUser[] = [
  { id: 1, value: 'an' },
  { id: 2, value: 'souhi' },
  { id: 3, value: 'keima' },
]

export default function BlogCreate() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<BlogIn>({ title: '', content: '', richtext: '', delta: '' })

  const handleTitle = (title: string) => setValues({ ...values, title })
  const handleContent = (content: string) => setValues({ ...values, content })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleQuill = (value: string, delta: DeltaStatic, source: Sources, editor: UnprivilegedEditor) => {
    const richtext = value.trim() === '<p><br></p>' ? '' : value.trim()
    setValues({ ...values, richtext, delta: JSON.stringify(editor.getContents()) })
  }

  const handleForm = async () => {
    const { title, content, richtext, image } = values
    if (!(title && content && richtext && image)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postBlogCreate(values)
      router.push(`/media/blog/${data.id}`)
    } catch (e) {
      console.log(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Blog" type="table" buttonArea={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginRequired margin="mt_20">
        <form method="POST" action="" className="create_grid">
          <Input label="タイトル" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" required={isRequired} onChange={handleContent} />

          <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />

          <Quill label="本文" users={users} value={values.richtext} className="blog" required={isRequired} onChange={handleQuill} />
        </form>
      </LoginRequired>
    </Main>
  )
}
