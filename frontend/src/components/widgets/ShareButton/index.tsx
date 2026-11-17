import { useTranslation } from 'react-i18next'
import { useRouter } from 'components/hooks/useRouter'
import Button from 'components/parts/Button'
import IconShare from 'components/parts/Icon/Share'

interface Props {
  path: string
  handleToast: (content: string, isError: boolean) => void
}

export default function ShareButton(props: Props): React.JSX.Element {
  const { path, handleToast } = props

  const router = useRouter()
  const { t } = useTranslation()

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(router.buildUrl(path))
      handleToast('share.copied', false)
    } catch {
      handleToast('share.failed', true)
    }
  }

  return <Button name={t('share.button')} size="s" icon={<IconShare size="1em" />} onClick={handleShare} />
}
