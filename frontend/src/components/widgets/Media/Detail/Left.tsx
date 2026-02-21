import { ChangeEvent, useState, useEffect, useMemo } from 'react'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { Channel } from 'types/internal/channle'
import { Comment, CommnetIn } from 'types/internal/comment'
import { MediaUser } from 'types/internal/media'
import { LikeMediaIn, SubscribeIn } from 'types/internal/user'
import { postComment } from 'api/internal/media/comment'
import { postLikeMedia, postSubscribe } from 'api/internal/user'
import { FetchError } from 'utils/constants/enum'
import { commentTypeNoMap, mediaTypeMap } from 'utils/constants/map'
import { capitalize } from 'utils/functions/common'
import { commentTypeNameEnum } from 'utils/functions/convertEnum'
import { formatDatetime } from 'utils/functions/datetime'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useUser } from 'components/hooks/useUser'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import CountLike from 'components/parts/Count/Like'
import CountRead from 'components/parts/Count/Read'
import Divide from 'components/parts/Divide'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import CommentContent from 'components/widgets/Comment/Content'
import CommentInput from 'components/widgets/Comment/Input/Input'
import SubscribeDeleteModal from 'components/widgets/Modal/SubscribeDelete'
import View from 'components/widgets/View'
import style from './Common.module.scss'

export interface MediaDetailState {
  isLike: boolean
  isSubscribe: boolean
  likeCount: number
  subscribeCount: number
  text: string
  comments: Comment[]
}

interface Props {
  media: {
    title: string
    content: string
    read: number
    like: number
    created: Date
    comments: Comment[]
    channel: Channel
    mediaUser: MediaUser
    type: 'video' | 'music' | 'comic' | 'picture' | 'blog'
  }
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailLeft(props: Props): React.JSX.Element {
  const { media, handleToast } = props
  const { title, content, read, created, channel, mediaUser } = media

  const initFormState: MediaDetailState = useMemo(
    () => ({
      isLike: mediaUser.isLike,
      isSubscribe: mediaUser.isSubscribe,
      likeCount: media.like,
      subscribeCount: 0,
      text: '',
      comments: media.comments,
    }),
    [mediaUser, media.like, media.comments],
  )

  const router = useRouter()
  const { user } = useUser()
  const { isLoading, handleLoading } = useIsLoading()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isContentView, setIsContentView] = useState<boolean>(false)
  const [isCommentView, setIsCommentView] = useState<boolean>(false)
  const [formState, setFormState] = useState<MediaDetailState>(initFormState)
  useEffect(() => setFormState(initFormState), [router.query.ulid, initFormState])

  const { isLike, isSubscribe, likeCount, subscribeCount, text, comments } = formState
  const isFallowDisable = !user.isActive || user.ulid === channel.ulid
  const handleModal = () => setIsModal(!isModal)
  const handleContentView = () => setIsContentView(!isContentView)
  const handleCommentView = () => setIsCommentView(!isCommentView)
  const handleComment = (e: ChangeEvent<HTMLTextAreaElement>) => setFormState((prev) => ({ ...prev, text: e.target.value }))

  const handleLike = async () => {
    const ulid = String(router.query.ulid)
    const pathname = capitalize(String(router.pathname.split('/')[2]))
    const mediaType = mediaTypeMap[pathname]
    if (!mediaType) return
    const request: LikeMediaIn = { ulid, mediaType }
    const ret = await postLikeMedia(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, ...data }))
  }

  const fetchSubscribe = async (isSubscribe: boolean) => {
    const request: SubscribeIn = { channelUlid: channel.ulid, isSubscribe }
    const ret = await postSubscribe(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, isSubscribe: data.isSubscribe, subscribeCount: data.count }))
  }

  const handleSubscribe = async () => {
    await fetchSubscribe(true)
    handleToast('チャンネルを登録しました', false)
  }

  const handleDeleteSubscribe = async () => {
    await fetchSubscribe(false)
    handleModal()
    handleToast('チャンネル登録を解除しました', false)
  }

  const handleMediaComment = async () => {
    handleLoading(true)
    const typeName = commentTypeNameEnum(capitalize(String(router.pathname.split('/')[2])))
    const typeNo = commentTypeNoMap[typeName]
    const objectUlid = String(router.query.ulid)
    const request: CommnetIn = { text, typeName, typeNo, objectUlid }
    const ret = await postComment(request)
    if (ret.isErr()) {
      handleLoading(false)
      handleToast(FetchError.Post, true)
      return
    }
    const data = ret.value
    setFormState((prev) => ({ ...prev, text: '', comments: [data, ...prev.comments] }))
    handleLoading(false)
  }

  return (
    <div className={style.media_detail_left}>
      <VStack gap="4">
        <h1 title={title}>{title}</h1>

        <time className={style.media_detail_aria_1}>{formatDatetime(created)}</time>

        <div className={style.media_detail_aria_2}>
          <CountRead read={read} />
          <CountLike isLike={isLike} disable={!user.isActive} count={likeCount} onClick={handleLike} />
        </div>

        <div className={style.media_detail_aria_3}>{/* {% include 'parts/common/hashtag.html' %} */}</div>
      </VStack>

      <Divide />

      <div>
        <HStack gap="4" justify="between">
          <HStack gap="4">
            <AvatarLink src={channel.avatar} size="l" ulid={channel.ulid} nickname={channel.name} />
            <VStack gap="2">
              <p className="fs_14">{channel.name}</p>
              <p className="fs_14 text_sub">
                登録者数<span className="ml_8">{subscribeCount}</span>
              </p>
            </VStack>
          </HStack>
          <div className={style.content_detail_p2}>
            {!isSubscribe && <Button color="green" name="登録する" disabled={isFallowDisable} onClick={handleSubscribe} />}
            {isSubscribe && <Button color="white" name="登録済み" onClick={handleModal} />}
          </div>
        </HStack>
        <div className={style.content_detail_p1}>
          <VStack gap="2">
            <View isView={isContentView} onView={handleContentView} content={isContentView ? '縮小表示' : '拡大表示'} />
            <div className={clsx(style.content_detail_aria, isContentView && style.active)}>
              <p>{content}</p>
            </div>
          </VStack>
        </div>
      </div>
      <Divide />

      <div className="advertise_aria">
        <h2>広告表示</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article.html' %} */}</article>
      </div>
      <Divide />

      <CommentInput user={user} count={comments.length} loading={isLoading} value={text} onChange={handleComment} onClick={handleMediaComment} />
      <VStack gap="6">
        <View isView={isCommentView} onView={handleCommentView} content={isCommentView ? '縮小表示' : '拡大表示'} />
        <VStack gap="10" className={clsx(style.comment_aria, isCommentView && style.active)}>
          {comments.map((comment) => (
            <CommentContent key={comment.ulid} comment={comment} user={user} setFormState={setFormState} handleToast={handleToast} />
          ))}
        </VStack>
      </VStack>
      <SubscribeDeleteModal open={isModal} onClose={handleModal} loading={isLoading} onAction={handleDeleteSubscribe} channel={channel} followerCount={subscribeCount} />
    </div>
  )
}
