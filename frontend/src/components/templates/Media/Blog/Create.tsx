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

const QuillEditor = dynamic(() => import('components/widgets/QuillEditor'), { ssr: false })

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
  const [create, setCreate] = useState<CreateBlog>({ title: '', content: '', richtext: '' })

  const handleTitle = (title: string) => setCreate({ ...create, title })
  const handleContent = (content: string) => setCreate({ ...create, content })
  const handleFile = (image: File) => setCreate({ ...create, image })

  const handleChange = (richtext: string) => {
    const value = richtext.trim()
    value !== '<p><br></p>' && setCreate({ ...create, richtext })
  }

  const handleForm = async () => {
    setIsLoading(true)
    try {
      const blog = await postBlogCreate(create)
      router.push(`media/blog/${blog.id}`)
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
          <p className="mv_16">タイトル</p>
          <Input name="title" value={create.title} onChange={handleTitle} required />

          <p className="mv_16">内容</p>
          <Textarea name="content" value={create.content} onChange={handleContent} required></Textarea>

          <p className="mv_16">サムネイル</p>
          <InputFile id="file_1" accept="image/*" onChange={handleFile} required />

          <p className="mv_16">本文</p>
          <div className="blog">
            <QuillEditor users={users} value={create.richtext} onChange={handleChange} />
          </div>

          <Button green type="button" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
