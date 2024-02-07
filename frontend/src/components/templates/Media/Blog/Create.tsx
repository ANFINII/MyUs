import React, { useState } from 'react'
import dynamic from 'next/dynamic'
import { MentionUser } from 'types/internal/timeline'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

const QuillEditor = dynamic(() => import('components/widgets/QuillEditor'), { ssr: false })

interface Props {
  isAuth: boolean
}

export default function BlogCreate(props: Props) {
  const { isAuth } = props

  const [content, setContent] = useState('')

  const users: MentionUser[] = [
    { id: 1, value: 'an' },
    { id: 2, value: 'souhi' },
    { id: 3, value: 'keima' },
  ]

  const handleChange = (value: string) => {
    const trimmedValue = value.trim()
    trimmedValue !== '<p><br></p>' && setContent(value)
  }

  return (
    <Main title="Blog">
      <LoginRequired isAuth={isAuth}>
        <p className="mv_16">タイトル</p>
        <Input name="title" id="title" required />

        <p className="mv_16">内容</p>
        <Textarea name="content" id="content" required></Textarea>

        <p className="mv_16">サムネイル</p>
        <InputFile id="file_1" accept="image/*" required />

        <p className="mv_16">本文</p>
        <div className="blog">
          <QuillEditor value={content} users={users} onChange={handleChange} />
        </div>

        <Button green type="submit" name="作成する" className="mt_32" />
      </LoginRequired>
    </Main>
  )
}
