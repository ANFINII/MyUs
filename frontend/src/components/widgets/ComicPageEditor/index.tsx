import { ChangeEvent, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { ComicPageItem } from 'types/internal/media/input'
import cx from 'utils/functions/cx'
import { previewUrl } from 'utils/functions/file'
import { useDragSort } from 'components/hooks/useDragSort'
import Button from 'components/parts/Button'
import ExImage from 'components/parts/ExImage'
import IconChevront from 'components/parts/Icon/Chevront'
import IconCross from 'components/parts/Icon/Cross'
import style from './ComicPageEditor.module.scss'

interface Props {
  label: string
  pages: ComicPageItem[]
  error?: string
  required?: boolean
  onChange: (pages: ComicPageItem[]) => void
}

export default function ComicPageEditor(props: Props): React.JSX.Element {
  const { label, pages, error, required = false, onChange } = props

  const { t } = useTranslation()
  const inputEl = useRef<HTMLInputElement>(null)
  const { dragIndex, dragOverIndex, dragItem } = useDragSort(pages, onChange)

  const isError = error === '' && required && pages.length === 0

  const handleAddClick = () => inputEl.current?.click()

  const handleAdd = (e: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? [])
    const added = files.map((file) => ({ key: crypto.randomUUID(), src: previewUrl(file), file }))
    onChange([...pages, ...added])
    e.target.value = ''
  }

  const handleMove = (index: number, offset: number) => () => {
    const next = index + offset
    if (next < 0 || next >= pages.length) return
    const moved = [...pages]
    const [page] = moved.splice(index, 1)
    if (page === undefined) return
    moved.splice(next, 0, page)
    onChange(moved)
  }

  const handleRemove = (index: number) => () => {
    const page = pages[index]
    if (page?.file) URL.revokeObjectURL(page.src)
    onChange(pages.filter((_, i) => i !== index))
  }

  return (
    <div className={style.editor}>
      <span className={style.label}>
        {label}
        {required && <span className={style.required}>*</span>}
      </span>
      <ul className={cx(style.pages, isError && style.error)}>
        {pages.map((page, index) => (
          <li key={page.key} className={cx(style.page, dragIndex === index && style.dragging, dragOverIndex === index && style.drag_over)} {...dragItem(index)}>
            <ExImage src={page.src} className={style.image} />
            <span className={style.number}>{index + 1}</span>
            <div className={style.actions}>
              <button type="button" className={style.action} title={t('manage.form.pagePrev')} disabled={index === 0} onClick={handleMove(index, -1)}>
                <IconChevront width="14" height="14" type="left" />
              </button>
              <button type="button" className={style.action} title={t('manage.form.pageNext')} disabled={index === pages.length - 1} onClick={handleMove(index, 1)}>
                <IconChevront width="14" height="14" type="right" />
              </button>
              <button type="button" className={style.action} title={t('manage.form.pageRemove')} onClick={handleRemove(index)}>
                <IconCross size="14" />
              </button>
            </div>
          </li>
        ))}
      </ul>
      <input ref={inputEl} type="file" accept="image/*" multiple hidden onChange={handleAdd} />
      <div>
        <Button color="white" size="s" name={t('manage.form.pageAdd')} onClick={handleAddClick} />
      </div>
      <p className={style.hint}>{t('manage.form.pageHint')}</p>
    </div>
  )
}
