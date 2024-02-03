import ContentTitle from '../Common/ContentTitle'

interface Props {
  imageUrl?: string
  nickname?: string
}

export default function MediaDetailInfo(props: Props) {
  const { imageUrl, nickname } = props

  return (
    <section className="section_detail">
      <div className="main_decolation">
        <a href="{% url 'myus:blog_detail' item.pk item.title %}" className="content_side">
          <figure className="content_size">
            <img src="" className="radius_8" />
          </figure>
          <div className="author_space_side">
            <ContentTitle title="" nickname="" read={1} totalLike={1} created="" />
          </div>
        </a>
      </div>
    </section>
  )
}
