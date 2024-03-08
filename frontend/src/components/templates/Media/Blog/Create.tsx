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
  const [data, setData] = useState<CreateBlog>({ title: '', content: '', richtext: '' })

  const handleTitle = (title: string) => setData({ ...data, title })
  const handleContent = (content: string) => setData({ ...data, content })
  const handleFile = (image: File) => setData({ ...data, image })

  const handleChange = (richtext: string) => {
    const value = richtext.trim()
    value !== '<p><br></p>' && setData({ ...data, richtext })
  }

  const handleForm = async () => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 3000))
    const formData = new FormData()
    formData.append('title', data.title)
    formData.append('content', data.content)
    formData.append('richtext', data.richtext)
    if (data.image) {
      formData.append('image', data.image)
      console.log('data.ima', data.image)
    }
    console.log('data', data)

    try {
      const blog = await postBlogCreate(formData)
      // const blogk = await postBlogCreate(data)
      router.push(`/media/blog/${blog.id}`)
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  // const handleForm = async (e: React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault()
  //   setIsLoading(true)
  //   const formData = new FormData()
  //   formData.append('title', data.title)
  //   formData.append('content', data.content)
  //   if (data?.image) {
  //     formData.append('image', data?.image)
  //   }

  //   try {
  //     console.log('data', formData)
  //     const blog = await postBlogCreate(formData)
  //     router.push(`media/blog/${blog.id}`)
  //   } catch (error) {
  //     console.log(error)
  //   } finally {
  //     setIsLoading(false)
  //   }
  // }

  return (
    <Main title="Blog">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="">
          <p className="mv_16">タイトル</p>
          <Input name="title" value={data.title} onChange={handleTitle} required />

          <p className="mv_16">内容</p>
          <Textarea name="content" value={data.content} onChange={handleContent} required></Textarea>

          <p className="mv_16">サムネイル</p>
          <InputFile id="file_1" accept="image/*" onChange={handleFile} required />

          <p className="mv_16">本文</p>
          <div className="blog">
            <QuillEditor users={users} value={data.richtext} onChange={handleChange} />
          </div>

          <Button color="green" name="作成する" className="mt_32" loading={isLoading} onClick={handleForm} />
        </form>
      </LoginRequired>
    </Main>
  )
}
