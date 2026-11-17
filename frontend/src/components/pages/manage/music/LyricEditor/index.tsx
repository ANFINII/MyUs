import { KeyboardEvent, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { buildLyric, formatLyricTime, LyricLine, toLyricRows } from 'utils/functions/lyric'
import Button from 'components/parts/Button'
import IconClock from 'components/parts/Icon/Clock'
import IconCross from 'components/parts/Icon/Cross'
import IconPlus from 'components/parts/Icon/Plus'
import Modal from 'components/parts/Modal'
import AudioPlayer from 'components/widgets/AudioPlayer'
import Lyric from 'components/widgets/Lyric'
import style from './LyricEditor.module.scss'

const NUDGE_SECONDS = 0.1

interface Props {
  src: string
  lyric: string
  onClose: () => void
  onApply: (lyric: string) => void
}

export default function LyricEditor(props: Props): React.JSX.Element {
  const { src, lyric: initLyric, onClose, onApply } = props

  const { t } = useTranslation()
  const audioRef = useRef<HTMLAudioElement>(null)
  const [rows, setRows] = useState<LyricLine[]>(toLyricRows(initLyric))
  const [selected, setSelected] = useState<number>(0)
  const [currentTime, setCurrentTime] = useState<number>(0)

  const lyric = buildLyric(rows)

  const updateTime = (index: number, time: number) => setRows(rows.map((row, i) => (i === index ? { ...row, time } : row)))
  const handleApply = () => onApply(lyric)

  const handleSelect = (index: number) => {
    setSelected(index)
    const row = rows[index]
    const audio = audioRef.current
    if (row && row.time >= 0 && audio) audio.currentTime = row.time
  }

  const handleRecord = () => {
    const audio = audioRef.current
    if (!audio || !rows[selected]) return
    updateTime(selected, Math.round(audio.currentTime * 100) / 100)
    setSelected(Math.min(selected + 1, rows.length - 1))
  }

  const handleNudge = (index: number, delta: number) => {
    const row = rows[index]
    if (!row || row.time < 0) return
    updateTime(index, Math.max(0, Math.round((row.time + delta) * 100) / 100))
  }

  const handleClear = (index: number) => updateTime(index, -1)
  const handleText = (index: number, text: string) => setRows(rows.map((row, i) => (i === index ? { ...row, text } : row)))

  const handleAddRow = (index: number) => {
    setRows([...rows.slice(0, index + 1), { time: -1, text: '' }, ...rows.slice(index + 1)])
    setSelected(index + 1)
  }

  const handleDeleteRow = (index: number) => {
    if (rows.length === 1) return setRows([{ time: -1, text: '' }])
    setRows(rows.filter((_, i) => i !== index))
    setSelected(Math.min(selected, rows.length - 2))
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>, index: number) => {
    if (e.key !== 'Enter' || e.nativeEvent.isComposing) return
    e.preventDefault()
    handleAddRow(index)
  }

  const handleSeek = (time: number) => {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = time
    audio.play()?.catch(() => {})
  }

  return (
    <Modal
      open
      onClose={onClose}
      title={t('manage.lyric.open')}
      size="l"
      actions={[
        { name: t('action.cancel'), color: 'white', onClick: onClose },
        { name: t('manage.lyric.apply'), color: 'blue', onClick: handleApply },
      ]}
    >
      <div className={style.editor}>
        <p className={style.hint}>{t('manage.lyric.hint')}</p>
        <AudioPlayer src={src} isVolumeInline audioRef={audioRef} className={style.player} onTimeUpdate={setCurrentTime} />
      <div className={style.body}>
        <div className={style.rows}>
          <Button color="purple" name={t('manage.lyric.record')} className={style.record} onClick={handleRecord} />
          <ol className={style.list}>
            {rows.map((row, index) => (
              <li key={index} className={cx(style.row, index === selected && style.selected)} onClick={() => handleSelect(index)}>
                <span className={cx(style.time, row.time < 0 && style.unset)}>{row.time >= 0 ? formatLyricTime(row.time) : '--:--.--'}</span>
                <input
                  value={row.text}
                  placeholder={t('manage.lyric.placeholder')}
                  className={style.text}
                  onChange={(e) => handleText(index, e.target.value)}
                  onFocus={() => setSelected(index)}
                  onKeyDown={(e) => handleKeyDown(e, index)}
                />
                <span className={style.actions} onClick={(e) => e.stopPropagation()}>
                  {row.time >= 0 && (
                    <>
                      <button type="button" className={style.nudge} onClick={() => handleNudge(index, -NUDGE_SECONDS)}>
                        -0.1
                      </button>
                      <button type="button" className={style.nudge} onClick={() => handleNudge(index, NUDGE_SECONDS)}>
                        +0.1
                      </button>
                      <button type="button" title={t('manage.lyric.clear')} className={style.nudge} onClick={() => handleClear(index)}>
                        <IconClock size="12" />
                      </button>
                    </>
                  )}
                  <button type="button" title={t('manage.lyric.addRow')} className={style.icon} onClick={() => handleAddRow(index)}>
                    <IconPlus size="14" />
                  </button>
                  <button type="button" title={t('manage.lyric.deleteRow')} className={cx(style.icon, style.delete)} onClick={() => handleDeleteRow(index)}>
                    <IconCross size="16" />
                  </button>
                </span>
              </li>
            ))}
          </ol>
        </div>
        <div className={style.preview}>
          <Lyric lyric={lyric} currentTime={currentTime} isExpand={false} onSeek={handleSeek} />
        </div>
      </div>
      </div>
    </Modal>
  )
}
