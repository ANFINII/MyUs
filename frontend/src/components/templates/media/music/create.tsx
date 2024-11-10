import { useState } from 'react'
import { useRouter } from 'next/router'
import { MusicIn } from 'types/internal/media'
import { postMusicCreate } from 'api/internal/media/create'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import Vertical from 'components/parts/Stack/Vertical'

export default function MusicCreate() {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<MusicIn>({ title: '', content: '', lyric: '', download: true })

  const handleTitle = (title: string) => setValues({ ...values, title })
  const handleContent = (content: string) => setValues({ ...values, content })
  const handleLyric = (lyric: string) => setValues({ ...values, lyric })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, music: files })
  const handleDownload = (checked: boolean) => setValues({ ...values, download: checked })

  const handleForm = async () => {
    const { title, content, lyric, music } = values
    if (!(title && content && lyric && music)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postMusicCreate(values)
      router.push(`/media/music/${data.id}`)
    } catch {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="Music" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="" encType="multipart/form-data">
          <Vertical gap="8">
            <Input label="タイトル" required={isRequired} onChange={handleTitle} />
            <Textarea label="内容" required={isRequired} onChange={handleContent} />
            <Textarea label="歌詞" required={isRequired} onChange={handleLyric} />
            <div>
              <InputFile label="音楽" accept="audio/*" required={isRequired} onChange={handleFile} />
              <CheckBox label="ダウンロード許可" className="mt_4" checked onChange={handleDownload} />
            </div>
          </Vertical>
        </form>
      </LoginError>
    </Main>
  )
}
