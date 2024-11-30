import { Todo } from 'types/internal/media'
import style from './Media.module.scss'

interface Props {
  data: Todo
}

export default function MediaTodo(props: Props) {
  const { data } = props
  // const { author, id, title } = data
  // const { nickname } = author
  console.log(data)

  return <section className={style.section_todo}></section>
}

// ;<section className="section_todo">
//   {/* {% if data.progress == '2' %} */}
//   {/* <div className="main_decolation_todo alert-dark" role="alert"> */}
//   {/* {% else %} */}
//   <div className="main_decolation_todo alert-{{ data.priority }}" role="alert">
//     {/* {% endif %} */}
//     <Link href="/todo/detail/[id][title]" className="author_space_todo">
//       {/* <div className="content_title">{{ data.title }}</div>
//     <p className="priority">優先度 {{ data.get_priority_display }}</p>
//     <p className="progress_myus">進捗度 {{ data.get_progress_display }}</p>
//     <time className="todo_time">期日 {{ data.duedate }}</time> */}
//       <object className="todo_link">
//         <Button color="green" size="s" name="編集" onClick={() => router.push(`/media/todo/update/${id}`)} />
//         <Button color="red" size="s" name="削除" onClick={() => router.push(`/media/todo/delete/${id}`)} />
//       </object>
//     </Link>
//   </div>
// </section>
