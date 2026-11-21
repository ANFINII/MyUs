import { useTranslation } from 'react-i18next'
import { EncodeStatus } from 'utils/constants/enum'
import style from './EncodeStatus.module.scss'

interface Props {
  status: EncodeStatus
}

export default function ManageEncodeStatus(props: Props): React.JSX.Element {
  const { status } = props

  const { t } = useTranslation()

  return (
    <>
      {status === EncodeStatus.Failed && <span className={style.encode_failed}>{t('manage.encode.failed')}</span>}
      {status === EncodeStatus.LowBitRate && <span className={style.encode_failed}>{t('manage.encode.lowBitRate')}</span>}
      {status === EncodeStatus.Encoding && <span>{t('manage.encode.encoding')}</span>}
      {status === EncodeStatus.Done && <span>{t('manage.encode.done')}</span>}
    </>
  )
}
