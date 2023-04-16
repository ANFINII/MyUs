// WebSocketオブジェクト
let ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws'
const chatId = JSON.parse(document.getElementById('obj_id').textContent)
const chatSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + '/ws/chat/detail/' + chatId)
const isPeriod = JSON.parse(document.getElementById('is_period').textContent)
const isAuthenticated = JSON.parse(document.getElementById('is_authenticated').textContent)

// Pjax処理
let threadDict = {}
history.replaceState(null, null, location.href)

function pjaxThread(href) {
  const threadObj = document.querySelector('.chat_section_thread_area').innerHTML
  threadDict[href] = threadObj
  history.pushState(null, null, href)
}

window.addEventListener('popstate', e => {
  const backUrl = location.pathname
  const backObj = threadDict[backUrl]
  if (backUrl.indexOf('thread') !== -1) {
    $('.chat_section_thread_area').html(backObj)
    if (document.querySelector('.message_aria_check') != null) {
      document.querySelector('.message_aria_check').checked = true
    }
  } else {
    $('.chat_section_thread_area').html(backObj)
    if (document.querySelector('.message_aria_check') != null) {
      document.querySelector('.message_aria_check').checked = false
    }
  }
})

function sleep(waitMsec) {
  return new Promise((resolve) => setTimeout(resolve, waitMsec));
}

// chatSocket の websocket 処理
chatSocket.onmessage = function (event) {
  let data = JSON.parse(event.data)
  if (data['command'] === 'create_message') {
    document.getElementById('message_form_button').setAttribute('disabled', true)
    const response = data['message']
    $('#chat_section_main_area').append(response.message_lists)
    $('#joined').html(response.joined)
    $('#thread').html(response.thread)
    const loginUserId = document.getElementById('user_id').textContent
    if (loginUserId != response.user_id && !response.is_period) {
      $('#edit_button_' + response.message_id).remove()
      $('#edit_update_main_' + response.message_id).remove()
    }
    const obj = document.getElementById('chat_section_main_area')
    obj.scrollTop = obj.scrollHeight
  } else if (data['command'] === 'create_reply_message') {
    const response = data['message']
    if ('/chat/detail/' + chatId + '/thread/' + response.parent_id === location.pathname) {
      document.getElementById('reply_form_button').setAttribute('disabled', true)
      $('#joined').html(response.joined)
      $('#reply_count_' + response.parent_id).html('返信 ' + response.reply_count + ' 件')
      $('#chat_section_thread_area_' + response.parent_id).append(response.reply_lists)
      const loginUserId = document.getElementById('user_id').textContent
      if (loginUserId != response.user_id && !response.is_period) {
        $('#edit_button_' + response.message_id).remove()
        $('#edit_update_main_' + response.message_id).remove()
      }
      const obj = document.querySelector('.chat_section_thread_area')
      obj.scrollTop = obj.scrollHeight
      pjaxThread(location.pathname)
    } else {
      $('#joined').html(response.joined)
      $('#reply_count_' + response.parent_id).html('返信 ' + response.reply_count + ' 件')
    }
  } else if (data['command'] === 'update_message') {
    const response = data['message']
    // 成功した時、背景色を戻す
    sleep(300)
    const highlight = document.querySelector('#message_aria_list_' + response.message_id)
    highlight.style.removeProperty('background-color')
    $('#message_aria_list_2_' + response.message_id).html(response.text)
    $('#message_aria_list_thread_' + response.message_id).html(response.text)
    pjaxThread(location.pathname)
  } else if (data['command'] === 'delete_message') {
    const response = data['message']
    // 成功した時、背景色を戻す
    const highlight = document.querySelector('#message_aria_list_cross_' + response.message_id)
    if (highlight !== null) {
      highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important')
    }
    sleep(200)
    $('#message_aria_list_' + response.message_id).remove()
    $('#edit_update_main_' + response.message_id).remove()
    $('#message_aria_list_thread_' + response.message_id).html('スレッドが削除されました!')
    $('#joined').html(response.joined)
    $('#thread').html(response.thread)
  } else if (data['command'] === 'delete_reply_message') {
    const response = data['message']
    const url = location.pathname
    if ('/chat/detail/' + chatId + '/thread/' + response.parent_id === url) {
      $('#message_aria_list_' + response.message_id).remove()
      $('#joined').html(response.joined)
      $('#reply_count_' + response.parent_id).html('返信 ' + response.reply_count + ' 件')
      pjaxThread(location.pathname)
    } else {
      $('#joined').html(response.joined)
      $('#reply_count_' + response.parent_id).html('返信 ' + response.reply_count + ' 件')
    }
  }
}

chatSocket.onopen = function (event) {
  console.log('open', event)
}

chatSocket.onerror = function (event) {
  console.log('error', event)
}

chatSocket.onclose = function (event) {
  console.log('close', event)
}


// スレッドボタンを押した時の処理
$(document).on('click', '.message_aria_thread', function (event) {
  event.preventDefault()
  const href = $(this).attr('href')
  const url = $(this).attr('thread')
  const messageId = $(this).attr('message-id')
  $.ajax({
    url: url,
    type: 'GET',
    data: { 'chat_id': chatId, 'message_id': messageId },
    dataType: 'json',
  })
    .done(function (response) {
      $('.chat_section_thread_area').html(response.thread)
      document.querySelector('.message_aria_check').checked = true
      pjaxThread(href)
    })
    .fail(function (response) {
      console.log(response)
    })
})


// バツボタンを押した時の処理
$(document).on('click', '.bi-x', function () {
  document.querySelector('.message_aria_check').checked = false
  const href = $(this).attr('href')
  pjaxThread(href)
})


// メッセージ作成
let placeholder = ''
if (isPeriod) {
  placeholder = 'チャット期間が過ぎています!'
} else if (!isAuthenticated) {
  placeholder = 'チャットするにはログインが必要です!'
} else {
  editor = document.getElementById('quill_chat')
}

const quillChat = new Quill('#quill_chat', {
  modules: {
    toolbar: [
      ['bold', 'underline', 'strike'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      ['code-block', 'blockquote', 'link', 'image'],
    ]
  },
  placeholder: placeholder,
  theme: 'snow'
})

if (isPeriod || !isAuthenticated) {
  quillChat.enable(false)
}

quillChat.on('text-change', function() {
  // focus時にそれ以外のQuillを無効化する
  const hasFocus = quillChat.hasFocus()
  if (hasFocus) {
    const targetElem = document.querySelectorAll('.form_button')
    const targetCount = targetElem.length
    if (targetElem) {
      for (let i = 0; i < targetCount; i++) {
        targetElem[i].setAttribute('disabled', true)
      }
    }
  }

  const quillText = quillChat.getText()
  if (quillText.match(/\S/g)) {
    document.getElementById('message_form_button').removeAttribute('disabled')
  } else {
    document.getElementById('message_form_button').setAttribute('disabled', true)
  }

  // ショートカット
  shortcut.add('Ctrl+Enter', function () {
    $('#message_form_button').click()
  })
  shortcut.add('meta+Enter', function () {
    $('#message_form_button').click()
  })
})

$('#message_form').submit(function (event) {
  event.preventDefault()
  const chatId = JSON.parse(document.getElementById('obj_id').textContent)
  const message = quillChat.root.innerHTML
  const delta = JSON.stringify(quillChat.getContents())
  const length = quillChat.getLength()
  quillChat.deleteText(0, length)
  document.getElementById('message_form_button').setAttribute('disabled', true)
  chatSocket.send(JSON.stringify({
    'command': 'create_message',
    'chat_id': chatId,
    'message': message,
    'delta': delta,
  }))
})


// リプライ作成
const quillReply = new Quill('#quill_reply', {
  modules: {
    toolbar: [
      ['bold', 'underline', 'strike'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      ['code-block', 'blockquote', 'link', 'image'],
    ]
  },
  placeholder: placeholder,
  theme: 'snow'
})

if (isPeriod || !isAuthenticated) {
  quillReply.enable(false)
}

quillReply.on('text-change', function() {
  // focus時にそれ以外のQuillを無効化する
  const hasFocus = quillReply.hasFocus()
  if (hasFocus) {
    const targetElem = document.querySelectorAll('.form_button')
    const targetCount = targetElem.length
    if (targetElem) {
      for (let i = 0; i < targetCount; i++) {
        targetElem[i].setAttribute('disabled', true)
      }
    }
  }

  const quillText = quillReply.getText()
  if (quillText.match(/\S/g)) {
    document.getElementById('reply_form_button').removeAttribute('disabled')
  } else {
    document.getElementById('reply_form_button').setAttribute('disabled', true)
  }

  // ショートカット
  shortcut.add('Ctrl+Enter', function () {
    $('#reply_form_button').click()
  })
  shortcut.add('meta+Enter', function () {
    $('#reply_form_button').click()
  })
})

$('#reply_form').submit(function (event) {
  event.preventDefault()
  const chatId = JSON.parse(document.getElementById('obj_id').textContent)
  const parentId = document.getElementById('parent_id').getAttribute('value')
  const message = quillReply.root.innerHTML
  const delta = JSON.stringify(quillReply.getContents())
  const length = quillReply.getLength()
  quillReply.deleteText(0, length)
  document.getElementById('reply_form_button').setAttribute('disabled', true)
  chatSocket.send(JSON.stringify({
    'command': 'create_reply_message',
    'chat_id': chatId,
    'message': message,
    'delta': delta,
    'parent_id': parentId,
  }))
})


// メッセージ編集
$(document).on('click', '.edit_button_update', function (event) {
  const messageId = $(this).parent().attr('message-id')
  document.getElementById('edit_update_main_' + messageId).classList.add('active')
  document.getElementById('message_aria_list_' + messageId).classList.add('active')

  let quillUpdate = new Object()
  child = document.getElementById('edit_textarea_caht_' + messageId).firstElementChild

  if (!child.classList.contains('ql-toolbar')) {
    quillUpdate = new Quill(`#quill_update_${messageId}`, {
      modules: {
        toolbar: [
          ['bold', 'underline', 'strike'],
          [{'list': 'ordered'}, {'list': 'bullet'}],
          ['code-block', 'blockquote', 'link', 'image'],
        ]
      },
      placeholder: '',
      theme: 'snow'
    })

    if (isPeriod || !isAuthenticated) {
      quillUpdate.enable(false)
    }

    quillUpdate.on('text-change', function() {
      // focus時にそれ以外のQuillを無効化する
      const hasFocus = quillUpdate.hasFocus()
      if (hasFocus) {
        const targetElem = document.querySelectorAll('.form_button')
        const targetCount = targetElem.length
        if (targetElem) {
          for (let i = 0; i < targetCount; i++) {
            targetElem[i].setAttribute('disabled', true)
          }
        }
      }

      const quillText = quillUpdate.getText()
      if (quillText.match(/\S/g)) {
        document.getElementById('update_form_button_' + messageId).removeAttribute('disabled')
      } else {
        document.getElementById('update_form_button_' + messageId).setAttribute('disabled', true)
      }

      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#update_form_button_' + messageId).click()
      })
      shortcut.add('meta+Enter', function () {
        $('#update_form_button_' + messageId).click()
      })
    })

    $(document).on('click', '.edit_update_cancel', function () {
      const messageId = $(this).closest('form').attr('message-id')
      document.getElementById('edit_update_main_' + messageId).classList.remove('active')
      document.getElementById('message_aria_list_' + messageId).classList.remove('active')
    })

    $(document).on('click', '#update_form_button_' + messageId, function (event) {
      event.preventDefault()
      const messageId = $(this).closest('form').attr('message-id')
      const message = quillUpdate.root.innerHTML
      const delta = JSON.stringify(quillUpdate.getContents())

      document.getElementById('edit_update_main_' + messageId).classList.remove('active')
      document.getElementById('message_aria_list_' + messageId).classList.remove('active')
      document.getElementById('update_form_button_' + messageId).setAttribute('disabled', true)

      // 更新時のアニメーション
      const highlight = document.querySelector('#message_aria_list_' + messageId)
      highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important')
      chatSocket.send(JSON.stringify({
        'command': 'update_message',
        'message_id': messageId,
        'message': message,
        'delta': delta,
      }))
    })
  }
})


// 削除モーダル
$(document).on('click', '.edit_button_delete', function () {
  const messageId = $(this).parent().attr('message-id')
  document.getElementById('modal_content_' + messageId).classList.add('active')
  document.getElementById('mask_' + messageId).classList.add('active')
})

$(document).on('click', '.modal_cancel', function () {
  const messageId = $(this).closest('.edit_button').attr('message-id')
  document.getElementById('modal_content_' + messageId).classList.remove('active')
  document.getElementById('mask_' + messageId).classList.remove('active')
})

// メッセージ削除
$(document).on('click', '.edit_delete_message', function (event) {
  event.preventDefault()
  const messageId = $(this).closest('.edit_button').attr('message-id')
  document.getElementById('modal_content_' + messageId).classList.remove('active')
  document.getElementById('mask_' + messageId).classList.remove('active')
  // 削除時のアニメーション
  const highlight = document.querySelector('#message_aria_list_' + messageId)
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important')
  chatSocket.send(JSON.stringify({
    'command': 'delete_message',
    'message_id': messageId,
  }))
})

// リプライ削除
$(document).on('click', '.edit_delete_reply', function (event) {
  event.preventDefault()
  const messageId = $(this).closest('.edit_button').attr('message-id')
  document.getElementById('modal_content_' + messageId).classList.remove('active')
  document.getElementById('mask_' + messageId).classList.remove('active')
  // 削除時のアニメーション
  const highlight = document.querySelector('#message_aria_list_' + messageId)
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important')
  chatSocket.send(JSON.stringify({
    'command': 'delete_reply_message',
    'message_id': messageId,
  }))
})
