import { ChangeEvent, useState, useEffect, useMemo } from 'react'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { FollowIn, LikeMediaIn } from 'types/internal/auth'
import { Comment, CommnetIn } from 'types/internal/comment'
import { Author, MediaUser } from 'types/internal/media'
import { postComment } from 'api/internal/media/comment'
import { postFollow, postLikeMedia } from 'api/internal/user'
import { CommentType, FetchError } from 'utils/constants/enum'
import { commentTypeNoMap, mediaTypeMap } from 'utils/constants/map'
import { capitalize, isActive } from 'utils/functions/common'
import { formatDatetime } from 'utils/functions/datetime'
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
import FollowDeleteModal from 'components/widgets/Modal/FollowDelete'
import View from 'components/widgets/View'
import style from './Common.module.scss'

export interface MediaDetailState {
  isLike: boolean
  isFollow: boolean
  likeCount: number
  followerCount: number
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
    author: Author
    mediaUser: MediaUser
    type: 'video' | 'music' | 'comic' | 'picture' | 'blog'
  }
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): JSX.Element {
  const { media, handleToast } = props
  const { title, content, read, created, author, mediaUser } = media

  const initFormState: MediaDetailState = useMemo(
    () => ({
      isLike: mediaUser.isLike,
      isFollow: mediaUser.isFollow,
      likeCount: media.like,
      followerCount: author.followerCount,
      text: '',
      comments: media.comments,
    }),
    [mediaUser, author, media.like, media.comments],
  )

  const router = useRouter()
  const { user } = useUser()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isContentView, setIsContentView] = useState<boolean>(false)
  const [isCommentView, setIsCommentView] = useState<boolean>(false)
  const [formState, setFormState] = useState<MediaDetailState>(initFormState)
  useEffect(() => setFormState(initFormState), [router.query.id, initFormState])

  const { isLike, isFollow, likeCount, followerCount, text, comments } = formState
  const isFallowDisable = !user || user.ulid === author.ulid
  const handleModal = () => setIsModal(!isModal)
  const handleContentView = () => setIsContentView(!isContentView)
  const handleCommentView = () => setIsCommentView(!isCommentView)
  const handleComment = (e: ChangeEvent<HTMLTextAreaElement>) => setFormState((prev) => ({ ...prev, text: e.target.value }))

  const handleLike = async () => {
    const id = Number(router.query.id)
    const pathname = capitalize(String(router.pathname.split('/')[2]))
    const mediaType = mediaTypeMap[pathname]
    if (!mediaType) return
    const request: LikeMediaIn = { id, mediaType, isLike: !isLike }
    const ret = await postLikeMedia(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, ...data }))
  }

  const fetchFollow = async (isFollow: boolean) => {
    const request: FollowIn = { ulid: author.ulid, isFollow }
    const ret = await postFollow(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, ...data }))
  }

  const handleFollow = async () => {
    await fetchFollow(true)
    handleToast('フォローしました', false)
  }

  const handleDeleteFollow = async () => {
    await fetchFollow(false)
    handleModal()
    handleToast('フォローを解除しました', false)
  }

  const handleMediaComment = async () => {
    setIsLoading(true)
    const typeName = capitalize(String(router.pathname.split('/')[2]))
    const typeNo = commentTypeNoMap[typeName as CommentType]
    const objectId = Number(router.query.id)
    const request: CommnetIn = { text, typeName, typeNo, objectId }
    const ret = await postComment(request)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast(FetchError.Post, true)
      return
    }
    const data = ret.value
    setFormState((prev) => ({ ...prev, text: '', comments: [data, ...prev.comments] }))
    setIsLoading(false)
  }

  return (
    <div>
      <div className="media_detail_aria">
        <h1 title={title}>{title}</h1>

        <time className="media_detail_aria_1">{formatDatetime(created)}</time>

        <div className="media_detail_aria_2">
          <CountRead read={read} />
          <CountLike isLike={isLike} disable={!user.isActive} likeCount={likeCount} onClick={handleLike} />
        </div>

        <div className="media_detail_aria_3">{/* {% include 'parts/common/hashtag.html' %} */}</div>
      </div>

      <Divide />

      <div className="content_detail">
        <HStack gap="4" justify="between">
          <HStack gap="4">
            <AvatarLink src={author.avatar} size="l" ulid={author.ulid} nickname={author.nickname} />
            <VStack gap="2">
              <p className="fs_14">{author.nickname}</p>
              <p className="fs_14 text_sub">
                登録者数<span className="ml_8">{followerCount}</span>
              </p>
            </VStack>
          </HStack>
          <div className="content_detail_p2">
            {!isFollow && <Button color="green" name="フォローする" disabled={isFallowDisable} onClick={handleFollow} />}
            {isFollow && <Button color="white" name="フォロー済み" onClick={handleModal} />}
          </div>
        </HStack>
        <div className="content_detail_p1">
          <VStack gap="2">
            <View isView={isContentView} onView={handleContentView} content={isContentView ? '縮小表示' : '拡大表示'} />
            <div className={clsx('content_detail_aria', isActive(isContentView))}>
              <p>{content}</p>
            </div>
          </VStack>
        </div>
      </div>

      <Divide />

      <CommentInput user={user} count={comments.length} loading={isLoading} value={text} onChange={handleComment} onClick={handleMediaComment} />
      <VStack gap="6">
        <View isView={isCommentView} onView={handleCommentView} content={isCommentView ? '縮小表示' : '拡大表示'} />
        <VStack gap="10" className={clsx(style.comment_aria, isCommentView && style.active)}>
          {comments.map((comment) => (
            <CommentContent key={comment.id} comment={comment} user={user} setFormState={setFormState} handleToast={handleToast} />
          ))}
        </VStack>
      </VStack>

      <Divide />

      <div className="advertise_aria">
        <h2>広告表示</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article_auto.html' %} */}</article>
        <Divide />

        <h2>個別広告</h2>
        <article className="article_list">{/* {% include 'parts/advertise_article.html' %} */}</article>
      </div>

      <FollowDeleteModal open={isModal} onClose={handleModal} loading={isLoading} onAction={handleDeleteFollow} author={author} />
    </div>
  )
}
