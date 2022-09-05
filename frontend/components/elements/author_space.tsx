export default function AuthorSpace() {
  return (
    <object className="author_image_space">
      <a href="{% url 'myus:userpage' item.author.nickname %}" data="{{ item.author.nickname }}" className="pjax_button_userpage">
        <img src="{{ item.author.image }}" title="{{ item.author.nickname }}" className="profile_image"/>
      </a>
    </object>
  )
}
