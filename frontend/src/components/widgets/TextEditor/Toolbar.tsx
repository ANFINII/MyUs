import { useCallback, useRef, useState } from 'react'
import { Editor } from '@tiptap/react'
import clsx from 'clsx'
import style from './TextEditor.module.scss'

interface Props {
  editor: Editor
}

export default function Toolbar(props: Props): React.JSX.Element {
  const { editor } = props

  const [isLinkInput, setIsLinkInput] = useState(false)
  const [colorValue, setColorValue] = useState('rgb(0, 0, 0)')
  const inputRef = useRef<HTMLInputElement>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  const handleToggleLink = useCallback(() => {
    if (editor.isActive('link')) {
      editor.chain().focus().unsetLink().run()
      return
    }
    setIsLinkInput((prev) => !prev)
    setTimeout(() => inputRef.current?.focus(), 0)
  }, [editor])

  const handleLinkSubmit = useCallback(() => {
    const url = inputRef.current?.value.trim()
    if (!url) return
    editor.chain().focus().setLink({ href: url }).run()
    setIsLinkInput(false)
  }, [editor])

  const handleLinkKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        e.preventDefault()
        handleLinkSubmit()
      }
      if (e.key === 'Escape') {
        setIsLinkInput(false)
        editor.commands.focus()
      }
    },
    [editor, handleLinkSubmit],
  )

  const handleLinkCancel = useCallback(() => {
    setIsLinkInput(false)
    editor.commands.focus()
  }, [editor])

  const handleImageClick = useCallback(() => {
    fileRef.current?.click()
  }, [])

  const handleFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = () => {
        const src = reader.result
        if (typeof src === 'string') {
          editor.chain().focus().setImage({ src }).run()
        }
      }
      reader.readAsDataURL(file)
      e.target.value = ''
    },
    [editor],
  )

  const handleColor = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setColorValue(e.target.value)
      editor.chain().focus().setColor(e.target.value).run()
    },
    [editor],
  )

  const handleHeading = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      const value = e.target.value
      if (value === '0') {
        editor.chain().focus().setParagraph().run()
      } else {
        const level = Number(value) as 1 | 2 | 3 | 4 | 5 | 6
        editor.chain().focus().toggleHeading({ level }).run()
      }
    },
    [editor],
  )

  const handleAlign = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      editor.chain().focus().setTextAlign(e.target.value).run()
    },
    [editor],
  )

  const activeHeading = (): string => {
    for (const level of [1, 2, 3, 4, 5, 6] as const) {
      if (editor.isActive('heading', { level })) return String(level)
    }
    return '0'
  }

  const activeAlign = (): string => {
    for (const align of ['left', 'center', 'right', 'justify'] as const) {
      if (editor.isActive({ textAlign: align })) return align
    }
    return 'left'
  }

  const btnClass = (isActive: boolean) => clsx(style.toolbar_button, isActive && style.toolbar_button_active)

  return (
    <div>
      <div className={style.toolbar}>
        {/* 見出し */}
        <div className={style.toolbar_group}>
          <select className={style.toolbar_select} value={activeHeading()} onChange={handleHeading}>
            <option value="0">Normal</option>
            <option value="1">Heading 1</option>
            <option value="2">Heading 2</option>
            <option value="3">Heading 3</option>
            <option value="4">Heading 4</option>
            <option value="5">Heading 5</option>
          </select>
        </div>

        {/* 配置 */}
        <div className={style.toolbar_group}>
          <select className={style.toolbar_select} value={activeAlign()} onChange={handleAlign}>
            <option value="left">Left</option>
            <option value="center">Center</option>
            <option value="right">Right</option>
            <option value="justify">Justify</option>
          </select>
        </div>

        {/* 文字装飾 */}
        <div className={style.toolbar_group}>
          {/* 太字 */}
          <button type="button" className={btnClass(editor.isActive('bold'))} title="太字" onClick={() => editor.chain().focus().toggleBold().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <path d="M5,4H9.5A2.5,2.5,0,0,1,12,6.5v0A2.5,2.5,0,0,1,9.5,9H5A0,0,0,0,1,5,9V4A0,0,0,0,1,5,4Z" />
              <path d="M5,9h5.5A2.5,2.5,0,0,1,13,11.5v0A2.5,2.5,0,0,1,10.5,14H5a0,0,0,0,1,0,0V9A0,0,0,0,1,5,9Z" />
            </svg>
          </button>
          {/* 斜体 */}
          <button type="button" className={btnClass(editor.isActive('italic'))} title="斜体" onClick={() => editor.chain().focus().toggleItalic().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <line x1="7" x2="13" y1="4" y2="4" />
              <line x1="5" x2="11" y1="14" y2="14" />
              <line x1="8" x2="10" y1="14" y2="4" />
            </svg>
          </button>
          {/* 下線 */}
          <button type="button" className={btnClass(editor.isActive('underline'))} title="下線" onClick={() => editor.chain().focus().toggleUnderline().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <path d="M5,3V9a4.012,4.012,0,0,0,4,4H9a4.012,4.012,0,0,0,4-4V3" />
              <rect height="1" rx="0.5" ry="0.5" width="12" x="3" y="15" className={style.icon_fill} />
            </svg>
          </button>
          {/* 取り消し線 */}
          <button type="button" className={btnClass(editor.isActive('strike'))} title="取り消し線" onClick={() => editor.chain().focus().toggleStrike().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <line x1="15.5" x2="2.5" y1="8.5" y2="9.5" className={style.icon_thin} />
              <path
                d="M9.007,8C6.542,7.791,6,7.519,6,6.5,6,5.792,7.283,5,9,5c1.571,0,2.765.679,2.969,1.309a1,1,0,0,0,1.9-.617C13.356,4.106,11.354,3,9,3,6.2,3,4,4.538,4,6.5a3.2,3.2,0,0,0,.5,1.843Z"
                className={style.icon_fill}
              />
              <path
                d="M8.984,10C11.457,10.208,12,10.479,12,11.5c0,0.708-1.283,1.5-3,1.5-1.571,0-2.765-.679-2.969-1.309a1,1,0,1,0-1.9.617C4.644,13.894,6.646,15,9,15c2.8,0,5-1.538,5-3.5a3.2,3.2,0,0,0-.5-1.843Z"
                className={style.icon_fill}
              />
            </svg>
          </button>
          {/* 文字色 */}
          <label className={style.toolbar_color_label} title="文字色">
            <svg viewBox="0 0 18 18" className={style.icon}>
              <line x1="3" x2="15" y1="15" y2="15" style={{ stroke: colorValue, strokeWidth: 3 }} />
              <polyline points="5.5 11 9 3 12.5 11" />
              <line x1="11.63" x2="6.38" y1="9" y2="9" />
            </svg>
            <input type="color" className={style.toolbar_color_input} onChange={handleColor} />
          </label>
          {/* 上付き */}
          <button type="button" className={btnClass(editor.isActive('superscript'))} title="上付き" onClick={() => editor.chain().focus().toggleSuperscript().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <path
                d="M15.5,7H13.861a4.015,4.015,0,0,0,1.914-2.975,1.8,1.8,0,0,0-1.6-1.751A1.922,1.922,0,0,0,12.021,3.7a0.5,0.5,0,1,0,.957.291,0.917,0.917,0,0,1,1.053-.725,0.81,0.81,0,0,1,.744.762c0,1.077-1.164,1.925-1.934,2.486A1.423,1.423,0,0,0,12,7.5a0.5,0.5,0,0,0,.5.5h3A0.5,0.5,0,0,0,15.5,7Z"
                className={style.icon_fill}
              />
              <path
                d="M9.651,5.241a1,1,0,0,0-1.41.108L6,7.964,3.759,5.349a1,1,0,1,0-1.519,1.3L4.683,9.5,2.241,12.35a1,1,0,1,0,1.519,1.3L6,11.036,8.241,13.65a1,1,0,0,0,1.519-1.3L7.317,9.5,9.759,6.651A1,1,0,0,0,9.651,5.241Z"
                className={style.icon_fill}
              />
            </svg>
          </button>
          {/* 下付き */}
          <button type="button" className={btnClass(editor.isActive('subscript'))} title="下付き" onClick={() => editor.chain().focus().toggleSubscript().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <path
                d="M15.5,15H13.861a3.858,3.858,0,0,0,1.914-2.975,1.8,1.8,0,0,0-1.6-1.751A1.921,1.921,0,0,0,12.021,11.7a0.50013,0.50013,0,1,0,.957.291h0a0.914,0.914,0,0,1,1.053-.725,0.81,0.81,0,0,1,.744.762c0,1.076-1.16971,1.86982-1.93971,2.43082A1.45639,1.45639,0,0,0,12,15.5a0.5,0.5,0,0,0,.5.5h3A0.5,0.5,0,0,0,15.5,15Z"
                className={style.icon_fill}
              />
              <path
                d="M9.65,5.241a1,1,0,0,0-1.409.108L6,7.964,3.759,5.349A1,1,0,0,0,2.192,6.59178Q2.21541,6.6213,2.241,6.649L4.684,9.5,2.241,12.35A1,1,0,0,0,3.71,13.70722q0.02557-.02768.049-0.05722L6,11.036,8.241,13.65a1,1,0,1,0,1.567-1.24277Q9.78459,12.3777,9.759,12.35L7.316,9.5,9.759,6.651A1,1,0,0,0,9.65,5.241Z"
                className={style.icon_fill}
              />
            </svg>
          </button>
        </div>

        {/* リスト */}
        <div className={style.toolbar_group}>
          {/* 番号付きリスト */}
          <button type="button" className={btnClass(editor.isActive('orderedList'))} title="番号付きリスト" onClick={() => editor.chain().focus().toggleOrderedList().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <line x1="7" x2="15" y1="4" y2="4" />
              <line x1="7" x2="15" y1="9" y2="9" />
              <line x1="7" x2="15" y1="14" y2="14" />
              <line x1="2.5" x2="4.5" y1="5.5" y2="5.5" className={style.icon_thin} />
              <path
                d="M3.5,6A0.5,0.5,0,0,1,3,5.5V3.085l-0.276.138A0.5,0.5,0,0,1,2.053,3c-0.124-.247-0.023-0.324.224-0.447l1-.5A0.5,0.5,0,0,1,4,2.5v3A0.5,0.5,0,0,1,3.5,6Z"
                className={style.icon_fill}
              />
              <path d="M4.5,10.5h-2c0-.234,1.85-1.076,1.85-2.234A0.959,0.959,0,0,0,2.5,8.156" className={style.icon_thin} />
              <path d="M2.5,14.846a0.959,0.959,0,0,0,1.85-.109A0.7,0.7,0,0,0,3.75,14a0.688,0.688,0,0,0,.6-0.736,0.959,0.959,0,0,0-1.85-.109" className={style.icon_thin} />
            </svg>
          </button>
          {/* 箇条書き */}
          <button type="button" className={btnClass(editor.isActive('bulletList'))} title="箇条書き" onClick={() => editor.chain().focus().toggleBulletList().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <line x1="6" x2="15" y1="4" y2="4" />
              <line x1="6" x2="15" y1="9" y2="9" />
              <line x1="6" x2="15" y1="14" y2="14" />
              <line x1="3" x2="3" y1="4" y2="4" />
              <line x1="3" x2="3" y1="9" y2="9" />
              <line x1="3" x2="3" y1="14" y2="14" />
            </svg>
          </button>
        </div>

        {/* ブロック・リンク・画像 */}
        <div className={style.toolbar_group}>
          {/* コードブロック */}
          <button type="button" className={btnClass(editor.isActive('codeBlock'))} title="コードブロック" onClick={() => editor.chain().focus().toggleCodeBlock().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <polyline points="5 7 3 9 5 11" />
              <polyline points="13 7 15 9 13 11" />
              <line x1="10" x2="8" y1="5" y2="13" />
            </svg>
          </button>
          {/* 引用 */}
          <button type="button" className={btnClass(editor.isActive('blockquote'))} title="引用" onClick={() => editor.chain().focus().toggleBlockquote().run()}>
            <svg viewBox="0 0 18 18" className={style.icon}>
              <rect x="3" y="3" width="2" height="12" rx="1" className={style.icon_fill} />
              <line x1="8" x2="15" y1="5" y2="5" />
              <line x1="8" x2="14" y1="9" y2="9" />
              <line x1="8" x2="13" y1="13" y2="13" />
            </svg>
          </button>
          {/* リンク */}
          <button type="button" className={btnClass(editor.isActive('link') || isLinkInput)} title="リンク" onClick={handleToggleLink}>
            <svg viewBox="0 0 24 24" className={style.icon_link}>
              <path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z" />
            </svg>
          </button>
          {/* 画像 */}
          <button type="button" className={style.toolbar_button} title="画像" onClick={handleImageClick}>
            <svg viewBox="0 0 28 20" className={style.icon_wide}>
              <rect x="2" y="2" width="24" height="16" rx="2" ry="2" />
              <circle cx="8" cy="7.5" r="1.5" />
              <polyline points="26 14 20 8 8 18" />
            </svg>
          </button>
          <input ref={fileRef} type="file" accept="image/*" className={style.file_hidden} onChange={handleFileChange} />
        </div>
      </div>

      {/* リンク入力パネル */}
      {isLinkInput && (
        <div className={style.input_panel}>
          <input ref={inputRef} type="url" className={style.input_field} placeholder="URLを入力" onKeyDown={handleLinkKeyDown} />
          <button type="button" className={style.input_submit} onClick={handleLinkSubmit}>
            挿入
          </button>
          <button type="button" className={style.input_cancel} onClick={handleLinkCancel}>
            ✕
          </button>
        </div>
      )}
    </div>
  )
}
