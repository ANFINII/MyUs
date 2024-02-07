import React, { useCallback } from 'react'
import ReactQuill from 'react-quill'
import 'react-quill/dist/quill.snow.css'
import 'quill-mention'
import 'quill-mention/dist/quill.mention.css'
import { MentionUser } from 'types/internal/timeline'

interface Props {
  reference?: React.LegacyRef<ReactQuill>
  users?: MentionUser[]
  value?: string
  onChange?: (value: string) => void
}

export default function QuillEditor(props: Props) {
  const { reference, users, value, onChange } = props

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

  return <ReactQuill theme="snow" ref={reference} modules={modules} formats={formats} value={value} onChange={onChange} />
}
