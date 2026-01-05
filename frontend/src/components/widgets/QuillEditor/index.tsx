import { useCallback, useEffect, useMemo, useRef } from 'react'
import clsx from 'clsx'
import QuillCore, { Sources } from 'quill'
import Delta from 'quill-delta'
import 'quill/dist/quill.snow.css'
import 'quill-mention'
import 'quill-mention/dist/quill.mention.css'
import { MentionUser } from 'types/internal/timeline'
import VStack from 'components/parts/Stack/Vertical'
import style from './QuillEditor.module.scss'

interface Props {
  label?: string
  value?: string
  required?: boolean
  className?: string
  users?: MentionUser[]
  onChange?: (value: string, delta: Delta, source: Sources, editor: QuillCore) => void
}

export default function QuillEditor(props: Props): React.JSX.Element {
  const { label, value, required = false, className, users, onChange } = props

  const hostRef = useRef<HTMLDivElement>(null)
  const quillRef = useRef<QuillCore | null>(null)
  const lastHtmlRef = useRef<string>('')
  const suppressChangeRef = useRef<boolean>(false)

  const isRequired = required && value === ''

  const mentionSource = useCallback(
    async (search: string, renderItem: (mentionUsers: MentionUser[] | undefined, search: string) => void, mentionChar: string) => {
      let mentionUsers: MentionUser[] | undefined
      if (mentionChar === '@') {
        mentionUsers = users
      }
      if (search.length === 0) {
        renderItem(mentionUsers, search)
      } else if (mentionUsers) {
        const matches = mentionUsers.filter((item) => item.value.toLowerCase().includes(search.toLowerCase()))
        renderItem(matches, search)
      }
    },
    [users],
  )

  const modules = useMemo(
    () => ({
      mention: {
        allowedChars: /^[A-Za-z\sÅÄÖåäö]*$/,
        mentionDenotationChars: ['@'],
        source: mentionSource,
      },
      toolbar: [
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        [{ color: [] }, { background: [] }, { align: [] }],
        [{ indent: '-1' }, { indent: '+1' }, { list: 'ordered' }, { list: 'bullet' }],
        ['bold', 'italic', 'underline', 'strike', 'formula', { script: 'super' }, { script: 'sub' }],
        ['code-block', 'blockquote', 'link', 'image'],
      ],
    }),
    [mentionSource],
  )

  const formats = [
    'header',
    'color',
    'background',
    'align',
    'indent',
    'list',
    'bold',
    'italic',
    'underline',
    'strike',
    'formula',
    'script',
    'code-block',
    'blockquote',
    'link',
    'image',
    'mention',
  ]

  const handleLabel = () => {
    quillRef.current?.focus()
  }

  useEffect(() => {
    const hostEl = hostRef.current
    if (!hostEl || quillRef.current) return

    const editor = document.createElement('div')
    hostEl.appendChild(editor)

    const quill = new QuillCore(editor, {
      theme: 'snow',
      modules,
      formats,
    })
    quillRef.current = quill

    const initialHtml = value ?? ''
    lastHtmlRef.current = initialHtml
    if (initialHtml) {
      quill.clipboard.dangerouslyPasteHTML(initialHtml)
    } else {
      quill.setText('')
    }

    const onTextChange = (delta: Delta, _oldDelta: Delta, source: Sources) => {
      if (suppressChangeRef.current) return
      const html = quill.root.innerHTML
      lastHtmlRef.current = html
      onChange?.(html, delta, source, quill)
    }

    quill.on('text-change', onTextChange)

    return () => {
      quill.off('text-change', onTextChange)
      quillRef.current = null
      hostEl.innerHTML = ''
    }
    // NOTE: modules/formats は useMemo で固定化され、初期化後に再生成しない（再初期化を避ける）
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const quill = quillRef.current
    if (!quill) return

    const nextHtml = value ?? ''
    if (nextHtml === lastHtmlRef.current) return

    suppressChangeRef.current = true
    try {
      if (nextHtml) {
        quill.clipboard.dangerouslyPasteHTML(nextHtml)
      } else {
        quill.setText('')
      }
      lastHtmlRef.current = nextHtml
    } finally {
      suppressChangeRef.current = false
    }
  }, [value])

  return (
    <VStack gap="2" className={className}>
      {label && (
        <label htmlFor={label} className={style.label} onClick={handleLabel}>
          {label}
        </label>
      )}
      <div ref={hostRef} className={clsx(style.editor, isRequired && style.error)} />
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
    </VStack>
  )
}
