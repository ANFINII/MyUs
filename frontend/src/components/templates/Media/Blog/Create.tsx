import React, { useState } from 'react'
import dynamic from 'next/dynamic'
import { useRouter } from 'next/router'
import { postBlogCreate } from 'api/media/post'
import { CreateBlog } from 'types/internal/media'
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

interface Props {
  isAuth: boolean
}

export default function BlogCreate(props: Props) {
  const { isAuth } = props

  const router = useRouter()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<CreateBlog>({ title: '', content: '', richtext: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handleFile = (image: File) => setData({ ...data, image })

  const handleQuill = (value: string) => {
    const richtext = value.trim() === '<p><br></p>' ? '' : value.trim()
    setData({ ...data, richtext })
  }

  const handleForm = async () => {
    if (!(data.title && data.content && data.richtext && data.image)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    const formData = new FormData()
    formData.append('title', data.title)
    formData.append('content', data.content)
    formData.append('richtext', data.richtext)
    formData.append('image', data.image)

    try {
      const blog = await postBlogCreate(formData)
      router.push(`/media/blog/${blog.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Blog">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="">
          <Input label="タイトル" className="mt_16" required={isRequired} onChange={handleTitle} />

          <Textarea label="内容" className="mt_16" required={isRequired} onChange={handleContent} />

          <InputFile label="サムネイル" accept="image/*" className="mt_16" required={isRequired} onChange={handleFile} />

          <Quill label="本文" users={users} value={data.richtext} className="blog" required={isRequired} onChange={handleQuill} />

          <Button color="green" name="作成する" loading={isLoading} onClick={handleForm} className="mt_32" />
        </form>
      </LoginRequired>
    </Main>
  )
}
