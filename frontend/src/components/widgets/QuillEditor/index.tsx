import { useState, useRef, useMemo } from 'react'
import { renderToString } from 'react-dom/server'
import ReactQuill from 'react-quill'
import Image from 'next/image'
import Editor, { RenderListFunction, mentionUser } from './modules/quill-setting'
import 'react-quill/dist/quill.snow.scss'

export async function showUsers(search: string, mentionUsers: mentionUser[]): Promise<mentionUser[]> {
  return mentionUsers.filter((user) => user.value.toLocaleLowerCase().includes(search.toLocaleLowerCase()))
}

interface Props {
  forwardedRef: React.LegacyRef<ReactQuill>
  placeholder: string
  value: string
  onChange: (value: string) => void
}

export default function QuillEditor(props: Props): JSX.Element {
  const { forwardedRef, placeholder, value, onChange } = props

  const getUsers = [
    {
      id: 1,
      username: 'an okina',
      avatar: '/',
    },
    {
      id: 2,
      username: 'an okina2',
      avatar: '/',
    },
  ]

  const rootDivRef = useRef<HTMLDivElement>(null)
  const [isFocused, setIsFocused] = useState(false)

  const renderMentionItem = (item: mentionUser): JSX.Element => {
    return (
      <div className="quill_avatar">
        <Image src={item.avatar} alt={item.value} width={32} height={32} />
        <span>{item.value}</span>
      </div>
    )
  }

  const modules = useMemo(
    () => ({
      magicUrl: true,
      blotFormatter: {},
      mention: {
        allowedChars: /^[A-Za-z\sÅÄÖåäö]*$/,
        mentionDenotationChars: ['@'],
        source: async function (search: string, renderList: RenderListFunction): Promise<void> {
          const mentionUsers = getUsers.map((user) => ({
            id: user.id,
            value: user.username,
            avatar: user.avatar,
          }))
          const matchUsers = await showUsers(search, mentionUsers as mentionUser[])
          renderList(matchUsers)
        },
        renderItem: function (item: mentionUser): string {
          return renderToString(renderMentionItem(item))
        },
      },
      toolbar: { container: [] },
    }),
    [getUsers],
  )

  const formats = ['mention', 'bold', 'blockquote', 'link', 'code-block']
  const handleFocus = (): void => setIsFocused(true)
  const handleBlur = (): void => setIsFocused(false)

  return (
    <div className={`${isFocused ? 'focused-border' : ''}`} ref={rootDivRef}>
      <Editor forwardedRef={forwardedRef} placeholder={placeholder} value={value} modules={modules} formats={formats} onChange={onChange} onFocus={handleFocus} onBlur={handleBlur} />
    </div>
  )
}
