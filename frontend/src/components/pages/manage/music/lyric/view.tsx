import { KeyboardEvent, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { errorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { Music } from 'types/internal/media/output'
import { putManageMusic } from 'api/internal/manage/update'
import { Fetch, FetchError } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { datetimeISO } from 'utils/functions/datetime'
import { buildLyric, formatLyricTime, LyricLine, toLyricRows } from 'utils/functions/lyric'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconClock from 'components/parts/Icon/Clock'
import IconCross from 'components/parts/Icon/Cross'
import IconPlus from 'components/parts/Icon/Plus'
import HStack from 'components/parts/Stack/Horizontal'
import AudioPlayer from 'components/widgets/AudioPlayer'
import Lyric from 'components/widgets/Lyric'
import style from './Lyric.module.scss'

const NUDGE_SECONDS = 0.1

interface Props {
  data: Music
}

export default function ManageMusicLyric(props: Props): React.JSX.Element {
  const { data } = props

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const audioRef = useRef<HTMLAudioElement>(null)
  const [rows, setRows] = useState<LyricLine[]>(toLyricRows(data.lyric))
  const [selected, setSelected] = useState<number>(0)
  const [currentTime, setCurrentTime] = useState<number>(0)

  const lyric = buildLyric(rows)

  const handleBack = () => router.push(`/manage/music/${data.ulid}`)
  const updateTime = (index: number, time: number) => setRows(rows.map((row, i) => (i === index ? { ...row, time } : row)))

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

  const handleSave = async () => {
    handleLoading(true)
    const ret = await putManageMusic(data.ulid, {
      categoryUlid: data.categoryUlid,
      title: data.title,
      content: data.content,
      lyric,
      download: data.download,
      publish: data.publish,
      publishAt: datetimeISO(data.publishAt),
    })
    handleLoading(false)
    if (ret.isErr()) return handleToast(errorMessage(ret.error, FetchError.Put), true)
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageMusic(data.ulid) })
    handleToast(Fetch.Save, false)
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('manage.button.save')} loading={loading} disabled={rows.length === 0} onClick={handleSave} />
      <Button color="blue" size="s" name={t('status.back')} onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title="Music" type="table" toast={toast} isFooter={false} button={button}>
      <div className={style.editor}>
        <div className={style.head}>
          <h2 className={style.title}>{data.title}</h2>
          <p className={style.hint}>{t('manage.lyric.hint')}</p>
        </div>
        <AudioPlayer src={data.music} isVolumeInline audioRef={audioRef} className={style.player} onTimeUpdate={setCurrentTime} />

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
            <Lyric lyric={lyric} currentTime={currentTime} isExpand onSeek={handleSeek} />
          </div>
        </div>
      </div>
    </Main>
  )
}
