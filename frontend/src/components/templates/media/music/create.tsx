import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { MusicIn } from 'types/internal/media'
import { postMusicCreate } from 'api/internal/media/create'
import { FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import VStack from 'components/parts/Stack/Vertical'

export default function MusicCreate(): React.JSX.Element {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const [values, setValues] = useState<MusicIn>({ title: '', content: '', lyric: '', download: true })

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleCheck = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.checked })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, music: files })

  const handleForm = async () => {
    const { title, content, lyric, music } = values
    if (!isRequiredCheck({ title, content, lyric, music })) return
    handleLoading(true)
    const ret = await postMusicCreate(values)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      handleLoading(false)
      return
    }
    router.push(`/media/music/${ret.value.id}`)
    handleLoading(false)
  }

  return (
    <Main title="Music" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <LoginError margin="mt_20">
        <form method="POST" action="" encType="multipart/form-data">
          <VStack gap="8">
            <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
            <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
            <Textarea label="歌詞" name="lyric" required={isRequired} onChange={handleText} />
            <VStack gap="2">
              <InputFile label="音楽" accept="audio/*" required={isRequired} onChange={handleFile} />
              <CheckBox label="ダウンロード許可" name="download" defaultChecked onChange={handleCheck} />
            </VStack>
          </VStack>
        </form>
      </LoginError>
    </Main>
  )
}
