// コメント 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#comment_form').submit(function (event) {
  event.preventDefault()
  const id = $(this).attr('obj-id')
  const path = $(this).attr('path')
  const csrf = $(this).attr('csrf')
  const text = $('form [name=text]').val().replace(/\n+$/g, '')
  $('#comment_form')[0].reset()
  document.getElementById('comment_form_area').style.height = '39px'
  document.getElementById('comment_form_button').setAttribute('disabled', true)
  $.ajax({
    url: '/comment/form',
    type: 'POST',
    data: { 'id': id, 'path': path, 'text': text, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_num').html(response.comment_num)
      $('#comment_aria').prepend(response.comment_lists)
    })
    .fail(function (response) {
      console.log(response)
    })
})

// 返信コメント表示, 非表示
$(document).on('click', '.reply_button', function () {
  const comment_id = $(this).parent().attr('comment-id')
  document.getElementById('comment_aria_list_reply_' + comment_id).classList.add('active')
  document.getElementById('reply_button_' + comment_id).classList.add('vanish')
  document.getElementById('reply_button_cancel_' + comment_id).classList.remove('vanish')
  $('#reply_' + comment_id).textareaAutoHeight()
})

$(document).on('click', '.reply_button_cancel', function () {
  const comment_id = $(this).parent().attr('comment-id')
  document.getElementById('comment_aria_list_reply_' + comment_id).classList.remove('active')
  document.getElementById('reply_button_' + comment_id).classList.remove('vanish')
  document.getElementById('reply_button_cancel_' + comment_id).classList.add('vanish')
})

$(document).on('click', '.reply_list_button', function () {
  const comment_id = $(this).parent().attr('comment-id')
  document.getElementById('reply_aria_list_' + comment_id).classList.add('active')
  document.getElementById('reply_list_button_' + comment_id).classList.add('vanish')
  document.getElementById('reply_list_button_cancel_' + comment_id).classList.remove('vanish')
})

$(document).on('click', '.reply_list_button_cancel', function () {
  const comment_id = $(this).parent().attr('comment-id')
  document.getElementById('reply_aria_list_' + comment_id).classList.remove('active')
  document.getElementById('reply_list_button_' + comment_id).classList.remove('vanish')
  document.getElementById('reply_list_button_cancel_' + comment_id).classList.add('vanish')
})

$(document).on('click', '.reply_cancel_button', function () {
  const comment_id = $(this).closest('form').attr('comment-id')
  document.getElementById('comment_aria_list_reply_' + comment_id).classList.remove('active')
  document.getElementById('reply_button_' + comment_id).classList.remove('vanish')
  document.getElementById('reply_button_cancel_' + comment_id).classList.add('vanish')
})

// コメントリプライ
$(document).on('click', '.reply_form', function (event) {
  event.preventDefault()
  const id = $(this).closest('form').attr('obj-id')
  const path = $(this).closest('form').attr('path')
  const csrf = $(this).closest('form').attr('csrf')
  const comment_id = $(this).closest('form').attr('comment-id')
  const text = $('#reply_' + comment_id).val().replace(/\n+$/g, '')
  $('#comment_aria_list_reply_' + comment_id)[0].reset()
  document.getElementById('reply_' + comment_id).style.height = '39px'
  document.getElementById('reply_form_button_' + comment_id).setAttribute('disabled', true)
  $.ajax({
    url: '/reply/form',
    type: 'POST',
    data: { 'id': id, 'path': path, 'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_num').html(response.comment_num)
      $('#reply_num_open_' + comment_id).html('▼ スレッド ' + response.reply_num + ' 件')
      $('#reply_num_close_' + comment_id).html('▲ スレッド ' + response.reply_num + ' 件')
      $('#reply_aria_list_' + comment_id).prepend(response.reply_lists)
    })
    .fail(function (response) {
      console.log(response)
    })
})

// メッセージ編集
$(document).on('click', '.edit_button_update', function () {
  const comment_id = $(this).parent().attr('comment-id')
  document.getElementById('edit_update_main_' + comment_id).classList.add('active')
  document.getElementById('comment_aria_list_' + comment_id).classList.add('active')
  document.getElementById('comment_form_update_' + comment_id).style.height = '31px'
  $('#comment_form_update_' + comment_id).textareaAutoHeight()
})

$(document).on('click', '.edit_update_cancel', function () {
  const comment_id = $(this).closest('form').attr('comment-id')
  document.getElementById('edit_update_main_' + comment_id).classList.remove('active')
  document.getElementById('comment_aria_list_' + comment_id).classList.remove('active')
})

$(document).on('click', '.edit_update_button', function (event) {
  event.preventDefault()
  const csrf = $(this).closest('form').attr('csrf')
  const comment_id = $(this).closest('form').attr('comment-id')
  const text = $('#comment_form_update_' + comment_id).val().replace(/\n+$/g, '')
  document.getElementById('edit_update_main_' + comment_id).classList.remove('active')
  document.getElementById('comment_aria_list_' + comment_id).classList.remove('active')
  document.getElementById('update_form_button_' + comment_id).setAttribute('disabled', true)
  // 更新時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + comment_id)
  highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important')
  $.ajax({
    url: `/comment/update/${comment_id}`,
    type: 'POST',
    data: { 'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      // 成功した時、背景色を戻す
      highlight.style.removeProperty('background-color')
      $('#comment_aria_list_2_' + comment_id).html(response.text)
    })
    .fail(function (response) {
      // 失敗した時、背景色を戻す
      highlight.style.removeProperty('background-color')
      console.log(response)
    })
})

// メッセージ削除
$(document).on('click', '.edit_button_delete', function () {
  const comment_id = $(this).parent().attr('comment-id')
  document.getElementById('modal_content_' + comment_id).classList.add('active')
  document.getElementById('mask_' + comment_id).classList.add('active')
})

$(document).on('click', '.modal_cancel', function () {
  const comment_id = $(this).parent().attr('comment-id')
  document.getElementById('modal_content_' + comment_id).classList.remove('active')
  document.getElementById('mask_' + comment_id).classList.remove('active')
})

$(document).on('click', '.edit_delete', function (event) {
  event.preventDefault()
  const id = $(this).parent().attr('obj-id')
  const path = $(this).parent().attr('path')
  const csrf = $(this).parent().attr('csrf')
  const comment_id = $(this).parent().attr('comment-id')
  const parent_id = $(this).parent().attr('parent-id')
  let url = `/comment/delete/${comment_id}`
  if (parent_id !== '') {
    url = `/reply/delete/${comment_id}`
  }
  document.getElementById('modal_content_' + comment_id).classList.remove('active')
  document.getElementById('mask_' + comment_id).classList.remove('active')
  // 削除時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + comment_id)
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important')
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'path': path, 'comment_id': comment_id, 'parent_id': parent_id, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_aria_list_' + comment_id).remove()
      $('#comment_num').html(response.comment_num)
      $('#reply_num_open_' + response.parent_id).html('▼ スレッド ' + response.reply_num + ' 件')
      $('#reply_num_close_' + response.parent_id).html('▲ スレッド ' + response.reply_num + ' 件')
    })
    .fail(function (response) {
      // 失敗した時、背景色を戻す
      highlight.style.removeProperty('background-color')
      console.log(response)
    })
})

// replyショートカット
$(document).on('focus', '.reply_form_area', function (event) {
  event.preventDefault()
  const comment_id = $(this).closest('form').attr('comment-id')

  // focus時にそれ以外のtextareaを無効化する
  const targetElem = document.querySelectorAll('.form_button')
  const targetCount = targetElem.length
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].setAttribute('disabled', true)
  }

  const text = $(this).val()
  if (text || text.match(/\S/g)) {
    // disabled属性を削除
    document.getElementById('reply_form_button_' + comment_id).removeAttribute('disabled')
  }

  $(document).on('input', '#reply_' + comment_id, function (event) {
    event.preventDefault()
    const text = $(this).val()
    if (!text || !text.match(/\S/g)) {
      // disabled属性を設定
      document.getElementById('reply_form_button_' + comment_id).setAttribute('disabled', true)
    } else {
      // disabled属性を削除
      document.getElementById('reply_form_button_' + comment_id).removeAttribute('disabled')

      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#reply_form_button_' + comment_id).click()
      })
      shortcut.add('meta+Enter', function () {
        $('#reply_form_button_' + comment_id).click()
      })
    }
  })
})
