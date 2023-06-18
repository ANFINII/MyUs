// コメント 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#comment_form').submit(function (event) {
  event.preventDefault()
  const id = $(this).attr('obj-id')
  const path = $(this).attr('path')
  const csrf = $(this).attr('csrf')
  const text = $('form [name=text]').val().replace(/\n+$/g, '')
  $('#comment_form')[0].reset()
  document.getElementById('comment_area').style.height = '39px'
  document.getElementById('comment_button').setAttribute('disabled', true)
  $.ajax({
    url: '/comment/form',
    type: 'POST',
    data: { 'id': id, 'path': path, 'text': text, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_count').html(response.comment_count)
      $('#comment_aria').prepend(response.comment_lists)
    })
    .fail(function (response) {
      console.log(response)
    })
})

// 返信コメント表示, 非表示
$(document).on('click', '.reply_button_open', function () {
  const commentId = $(this).parent().attr('comment-id')
  document.getElementById('comment_aria_list_reply_' + commentId).classList.add('active')
  document.getElementById('reply_button_open_' + commentId).classList.add('vanish')
  document.getElementById('reply_button_close_' + commentId).classList.remove('vanish')
  $('#reply_' + commentId).textareaAutoHeight()
})

$(document).on('click', '.reply_button_close', function () {
  const commentId = $(this).parent().attr('comment-id')
  document.getElementById('comment_aria_list_reply_' + commentId).classList.remove('active')
  document.getElementById('reply_button_open_' + commentId).classList.remove('vanish')
  document.getElementById('reply_button_close_' + commentId).classList.add('vanish')
})

$(document).on('click', '.reply_list_button_open', function () {
  const commentId = $(this).parent().attr('comment-id')
  document.getElementById('reply_aria_list_' + commentId).classList.add('active')
  document.getElementById('reply_list_button_open_' + commentId).classList.add('vanish')
  document.getElementById('reply_list_button_close_' + commentId).classList.remove('vanish')
})

$(document).on('click', '.reply_list_button_close', function () {
  const commentId = $(this).parent().attr('comment-id')
  document.getElementById('reply_aria_list_' + commentId).classList.remove('active')
  document.getElementById('reply_list_button_open_' + commentId).classList.remove('vanish')
  document.getElementById('reply_list_button_close_' + commentId).classList.add('vanish')
})

$(document).on('click', '.reply_cancel_button', function () {
  const commentId = $(this).closest('form').attr('comment-id')
  document.getElementById('comment_aria_list_reply_' + commentId).classList.remove('active')
  document.getElementById('reply_button_open_' + commentId).classList.remove('vanish')
  document.getElementById('reply_button_close_' + commentId).classList.add('vanish')
})

// コメントリプライ
$(document).on('click', '.reply_form', function (event) {
  event.preventDefault()
  const id = $(this).closest('form').attr('obj-id')
  const path = $(this).closest('form').attr('path')
  const csrf = $(this).closest('form').attr('csrf')
  const commentId = $(this).closest('form').attr('comment-id')
  const text = $('#reply_' + commentId).val().replace(/\n+$/g, '')
  $('#comment_aria_list_reply_' + commentId)[0].reset()
  document.getElementById('reply_' + commentId).style.height = '39px'
  document.getElementById('reply_button_' + commentId).setAttribute('disabled', true)
  $.ajax({
    url: '/reply/form',
    type: 'POST',
    data: { 'id': id, 'path': path, 'comment_id': commentId, 'text': text, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_count').html(response.comment_count)
      $('#reply_count_open_' + commentId).html('▼ スレッド ' + response.reply_count + ' 件')
      $('#reply_count_close_' + commentId).html('▲ スレッド ' + response.reply_count + ' 件')
      $('#reply_aria_list_' + commentId).prepend(response.reply_lists)
    })
    .fail(function (response) {
      console.log(response)
    })
})

// メッセージ編集
$(document).on('click', '.edit_button_update', function () {
  const commentId = $(this).parent().attr('comment-id')
  document.getElementById('edit_update_main_' + commentId).classList.add('active')
  document.getElementById('comment_aria_list_' + commentId).classList.add('active')
  document.getElementById('comment_update_' + commentId).style.height = '31px'
  $('#comment_update_' + commentId).textareaAutoHeight()
})

$(document).on('click', '.edit_update_cancel', function () {
  const commentId = $(this).closest('form').attr('comment-id')
  document.getElementById('edit_update_main_' + commentId).classList.remove('active')
  document.getElementById('comment_aria_list_' + commentId).classList.remove('active')
})

$(document).on('click', '.edit_update_button', function (event) {
  event.preventDefault()
  const csrf = $(this).closest('form').attr('csrf')
  const commentId = $(this).closest('form').attr('comment-id')
  const text = $('#comment_update_' + commentId).val().replace(/\n+$/g, '')
  document.getElementById('edit_update_main_' + commentId).classList.remove('active')
  document.getElementById('comment_aria_list_' + commentId).classList.remove('active')
  document.getElementById('update_button_' + commentId).setAttribute('disabled', true)
  // 更新時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + commentId)
  highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important')
  $.ajax({
    url: `/comment/update/${commentId}`,
    type: 'POST',
    data: { 'comment_id': commentId, 'text': text, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      // 成功した時、背景色を戻す
      highlight.style.removeProperty('background-color')
      $('#comment_aria_list_2_' + commentId).html(response.text)
      $('#modal_comment_' + commentId).html(response.text)
    })
    .fail(function (response) {
      // 失敗した時、背景色を戻す
      highlight.style.removeProperty('background-color')
      console.log(response)
    })
})

// メッセージ削除
$(document).on('click', '.edit_button_delete', function () {
  const commentId = $(this).parent().attr('comment-id')
  document.getElementById('modal_content_' + commentId).classList.add('active')
  document.getElementById('mask_' + commentId).classList.add('active')
})

$(document).on('click', '.modal_cancel', function () {
  const commentId = $(this).parent().attr('comment-id')
  document.getElementById('modal_content_' + commentId).classList.remove('active')
  document.getElementById('mask_' + commentId).classList.remove('active')
})

$(document).on('click', '.edit_delete', function (event) {
  event.preventDefault()
  const id = $(this).parent().attr('obj-id')
  const path = $(this).parent().attr('path')
  const csrf = $(this).parent().attr('csrf')
  const commentId = $(this).parent().attr('comment-id')
  const parentId = $(this).parent().attr('parent-id')
  let url = `/comment/delete/${commentId}`
  if (parentId !== '') {
    url = `/reply/delete/${commentId}`
  }
  document.getElementById('modal_content_' + commentId).classList.remove('active')
  document.getElementById('mask_' + commentId).classList.remove('active')
  // 削除時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + commentId)
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important')
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'path': path, 'comment_id': commentId, 'parent_id': parentId, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_aria_list_' + commentId).remove()
      $('#comment_count').html(response.comment_count)
      $('#reply_count_open_' + response.parentId).html('▼ スレッド ' + response.reply_count + ' 件')
      $('#reply_count_close_' + response.parentId).html('▲ スレッド ' + response.reply_count + ' 件')
    })
    .fail(function (response) {
      // 失敗した時、背景色を戻す
      highlight.style.removeProperty('background-color')
      console.log(response)
    })
})

// replyショートカット
$(document).on('focus', '.reply_area', function (event) {
  event.preventDefault()
  const commentId = $(this).closest('form').attr('comment-id')

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
    document.getElementById('reply_button_' + commentId).removeAttribute('disabled')
  }

  $(document).on('input', '#reply_' + commentId, function (event) {
    event.preventDefault()
    const text = $(this).val()
    if (!text || !text.match(/\S/g)) {
      // disabled属性を設定
      document.getElementById('reply_button_' + commentId).setAttribute('disabled', true)
    } else {
      // disabled属性を削除
      document.getElementById('reply_button_' + commentId).removeAttribute('disabled')

      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#reply_button_' + commentId).click()
      })
      shortcut.add('meta+Enter', function () {
        $('#reply_button_' + commentId).click()
      })
    }
  })
})
