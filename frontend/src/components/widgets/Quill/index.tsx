import React, { useCallback, useRef } from 'react'
import ReactQuill, { UnprivilegedEditor } from 'react-quill'
import clsx from 'clsx'
import { DeltaStatic, Sources } from 'quill'
import 'react-quill/dist/quill.snow.css'
import 'quill-mention'
import 'quill-mention/dist/quill.mention.css'
import { MentionUser } from 'types/internal/timeline'
import style from './Quill.module.scss'

interface Props {
  label?: string
  value?: string
  required?: boolean
  className?: string
  users?: MentionUser[]
  onChange?: (value: string, delta: DeltaStatic, source: Sources, editor: UnprivilegedEditor) => void
}

export default function Quill(props: Props) {
  const { label, value, required = false, className, users } = props

  const ref = useRef<ReactQuill>(null)

  const isRequired = required && value === ''

  const modules = {
    mention: {
      allowedChars: /^[A-Za-z\sÅÄÖåäö]*$/,
      mentionDenotationChars: ['@'],
      source: useCallback(async (search: string, renderItem: (users: MentionUser[] | undefined, search: string) => void, mentionChar: string) => {
        let mentionUsers: MentionUser[] | undefined
        if (mentionChar === '@') {
          mentionUsers = users
        }
        if (search.length === 0) {
          renderItem(mentionUsers, search)
        } else if (mentionUsers) {
          const matches = mentionUsers?.filter((item) => item.value.toLowerCase().includes(search.toLowerCase()))
          renderItem(matches, search)
        }
      }, []),
    },
    toolbar: [
      [{ header: [1, 2, 3, 4, 5, 6, false] }],
      [{ color: [] }, { background: [] }, { align: [] }],
      [{ indent: '-1' }, { indent: '+1' }, { list: 'ordered' }, { list: 'bullet' }],
      ['bold', 'italic', 'underline', 'strike', 'formula', { script: 'super' }, { script: 'sub' }],
      ['code-block', 'blockquote', 'link', 'image'],
    ],
  }

  const formats = ['header', 'color', 'background', 'align', 'indent', 'list', 'bold', 'italic', 'underline', 'strike', 'formula', 'script', 'code-block', 'blockquote', 'link', 'image', 'mention']

  const handleLabel = () => {
    if (ref.current) {
      ref.current.focus()
    }
  }

  return (
    <div className={className}>
      {label && (
        <label htmlFor={label} className={style.label} onClick={handleLabel}>
          {label}
        </label>
      )}
      <ReactQuill {...props} theme="snow" ref={ref} modules={modules} formats={formats} className={clsx(isRequired && style.error)} />
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
    </div>
  )
}
