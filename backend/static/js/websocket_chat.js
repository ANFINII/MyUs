// WebSocketオブジェクト
let ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
const chat_id = JSON.parse(document.getElementById('obj_id').textContent);
const chatSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + '/ws/chat/detail/' + chat_id);

// Pjax処理
let thread_dict = {};
history.replaceState(null, null, location.href);

function pjax_thread_dict(href) {
  const thread_obj = document.querySelector('.chat_section_thread_area').innerHTML;
  thread_dict[href] = thread_obj;
  history.pushState(null, null, href);
}

window.addEventListener('popstate', e => {
  const back_url = location.pathname;
  const back_obj = thread_dict[back_url];
  if (back_url.indexOf('thread') !== -1) {
    $('.chat_section_thread_area').html(back_obj);
    if (document.querySelector('.message_aria_check') != null) {
      document.querySelector('.message_aria_check').checked = true;
    }
  } else {
    $('.chat_section_thread_area').html(back_obj);
    if (document.querySelector('.message_aria_check') != null) {
      document.querySelector('.message_aria_check').checked = false;
    }
  }
});

// スレッドボタンを押した時の処理
$(document).on('click', '.message_aria_thread', function (event) {
  event.preventDefault();
  const href = $(this).attr('href');
  const url = $(this).attr('thread');
  const message_id = $(this).attr('message-id');
  $.ajax({
    url: url,
    type: 'GET',
    data: { 'chat_id': chat_id, 'message_id': message_id },
    dataType: 'json',
  })
    .done(function (response) {
      $('.chat_section_thread_area').html(response.thread);
      document.querySelector('.message_aria_check').checked = true;
      pjax_thread_dict(href);
    })
    .fail(function (response) {
      console.log(response);
    })
});

// バツボタンを押した時の処理
$(document).on('click', '.bi-x', function () {
  document.querySelector('.message_aria_check').checked = false;
  const href = $(this).attr('href');
  pjax_thread_dict(href);
});

// chatSocket の websocket 処理
chatSocket.onmessage = function (event) {
  let data = JSON.parse(event.data);
  if (data['command'] === 'create_message') {
    document.getElementById('message_form_button').setAttribute('disabled', true);
    const response = data['message'];
    $('#chat_section_main_area').append(response.message_lists);
    $('#joined').html(response.joined);
    $('#thread').html(response.thread);
    const login_user_id = document.getElementById('user_id').textContent;
    if (login_user_id != response.user_id) {
      $('#edit_button_' + response.message_id).remove();
      $('#edit_update_main_' + response.message_id).remove();
    }
    const obj = document.getElementById('chat_section_main_area');
    obj.scrollTop = obj.scrollHeight;
  } else if (data['command'] === 'create_reply_message') {
    const response = data['message'];
    if ('/chat/detail/' + chat_id + '/thread/' + response.parent_id === location.pathname) {
      document.getElementById('reply_form_button').setAttribute('disabled', true);
      $('#joined').html(response.joined);
      $('#reply_num_' + response.parent_id).html('返信 ' + response.reply_num + ' 件');
      $('#chat_section_thread_area_' + response.parent_id).append(response.reply_lists);
      const login_user_id = document.getElementById('user_id').textContent;
      if (login_user_id != response.user_id) {
        $('#edit_button_' + response.message_id).remove();
        $('#edit_update_main_' + response.message_id).remove();
      }
      const obj = document.querySelector('.chat_section_thread');
      obj.scrollTop = obj.scrollHeight;
      pjax_thread_dict(location.pathname)
    } else {
      $('#joined').html(response.joined);
      $('#reply_num_' + response.parent_id).html('返信 ' + response.reply_num + ' 件');
    }
  } else if (data['command'] === 'update_message') {
    const response = data['message'];
    // 成功した時、背景色を戻す
    const highlight = document.querySelector('#message_aria_list_' + response.message_id);
    highlight.style.removeProperty('background-color');
    $('#message_aria_list_2_' + response.message_id).html(response.text);
    $('#message_aria_list_thread_' + response.message_id).html(response.text);
    pjax_thread_dict(location.pathname)
  } else if (data['command'] === 'delete_message') {
    const response = data['message'];
    const highlight = document.querySelector('#message_aria_list_cross_' + response.message_id);
    if (highlight !== null) {
      highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
    }
    $('#message_aria_list_' + response.message_id).remove();
    $('#edit_update_main_' + response.message_id).remove();
    $('#message_aria_list_thread_' + response.message_id).html('スレッドが削除されました!');
    $('#joined').html(response.joined);
    $('#thread').html(response.thread);
  } else if (data['command'] === 'delete_reply_message') {
    const response = data['message'];
    const url = location.pathname;
    if ('/chat/detail/' + chat_id + '/thread/' + response.parent_id === url) {
      $('#message_aria_list_' + response.message_id).remove();
      $('#joined').html(response.joined);
      $('#reply_num_' + response.parent_id).html('返信 ' + response.reply_num + ' 件');
      pjax_thread_dict(location.pathname)
    } else {
      $('#joined').html(response.joined);
      $('#reply_num_' + response.parent_id).html('返信 ' + response.reply_num + ' 件');
    }
  }
};

chatSocket.onopen = function (event) {
  console.log('open', event);
}

chatSocket.onerror = function (event) {
  console.log('error', event);
}

chatSocket.onclose = function (event) {
  console.log('close', event);
}



var quillChat = new Quill('#quill_chat', {
  modules: {
    toolbar: [
      ['bold', 'underline', 'strike'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      ['code-block', 'blockquote', 'link', 'image'],
    ]
  },
  placeholder: '',
  theme: 'snow'
});

const target = document.getElementById('message_form_button');
console.log('target', target)

// messageショートカット
quillChat.on('text-change', function() {
  // const text = editorHtml.replace(/<p><br><\/p>/g, '')

  // focus時にそれ以外のtextareaを無効化する
  const targetElem = document.querySelectorAll('.form_button');
  const targetCount = targetElem.length;
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].setAttribute('disabled', true);
  }

  const message = $('#text').val(quillChat.root.innerHTML);
  if (message) {
    // disabled属性を削除
    document.getElementById('message_form_button').removeAttribute('disabled');
    console.log()
  } else if ((message === '<p><br></p>')) {
    document.getElementById('message_form_button').setAttribute('disabled', true);
  }

  $(document).on('textarea', message, function (event) {
    event.preventDefault();
    if (!message || message === '<p><br></p>') {
      // disabled属性を設定
      document.getElementById('message_form_button').setAttribute('disabled', true);
    } else {
      // disabled属性を削除
      document.getElementById('message_form_button').removeAttribute('disabled');
      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#message_form_button').click();
      });
      shortcut.add('meta+Enter', function () {
        $('#message_form_button').click();
      });
    }
  });
});



// メッセージ作成
$('#message_form').submit(function (event) {
  event.preventDefault();
  const chat_id = JSON.parse(document.getElementById('obj_id').textContent);
  // const message = $('form [name=text]').val();
  const message = $('#text').val(quillChat.root.innerHTML);
  const delta = $('#delta').val(JSON.stringify(quillChat.getContents()));
  // const csrf = $(this).attr('csrf');

  // console.log('csrf', csrf)
  console.log('message', message)
  console.log('delta', delta)

  $('#message_form')[0].reset();
  // document.getElementById('message_form_area').style.height = '40px';
  document.getElementById('message_form_button').setAttribute('disabled', true);



  chatSocket.send(JSON.stringify({
    'command': 'create_message',
    'chat_id': chat_id,
    'message': message,
    'delta': delta,
    // 'csrfmiddlewaretoken': csrf,
  }));
});




// let replyEditorInput = document.getElementById('reply_editor_input');
let quillChatReply = new Quill('reply_form_area', {
  modules: {
    toolbar: [
      ['bold', 'underline', 'strike'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      ['code-block', 'blockquote', 'link', 'image'],
    ]
  },
  placeholder: '',
  theme: 'snow'
});

quillChatReply.on('text-change', function() {
  let editorHtml = editor.querySelector('.ql-editor').innerHTML;
  const text = editorHtml.replace(/<p><br><\/p>/g, '')
  // replyEditorInput.value = editorHtml;
  if (!text || !text.match(/\S/g)) {
    // disabled属性を設定
    document.getElementById('reply_form_button').setAttribute('disabled', true);
  } else {
    // disabled属性を削除
    document.getElementById('reply_form_button').removeAttribute('disabled');
  }
  // ショートカット
  shortcut.add('Ctrl+Enter', function () {
    $('#reply_form_button').click();
  });
  shortcut.add('meta+Enter', function () {
    $('#reply_form_button').click();
  });
});




// リプライ作成
$('#reply_form').submit(function (event) {
  event.preventDefault();
  const chat_id = JSON.parse(document.getElementById('obj_id').textContent);
  const parent_id = document.getElementById('parent_id').getAttribute('value');
  // const message = $('form [name=reply]').val().replace(/\n+$/g, '');
  const message = $('#text').val(quillChat.root.innerHTML);
  const delta = $('#delta').val(JSON.stringify(quillChat.getContents()));
  $('#reply_form')[0].reset();
  document.getElementById('reply_form_area').style.height = '40px';
  document.getElementById('reply_form_button').setAttribute('disabled', true);
  chatSocket.send(JSON.stringify({
    'command': 'create_reply_message',
    'chat_id': chat_id,
    'message': message,
    'delta': delta,
    'parent_id': parent_id,
  }));
});

// メッセージ編集
$(document).on('click', '.edit_button_update', function () {
  const message_id = $(this).parent().attr('message-id');
  document.getElementById('edit_update_main_' + message_id).classList.add('active');
  document.getElementById('message_aria_list_' + message_id).classList.add('active');
  document.getElementById('message_form_update_' + message_id).style.height = '40px';
  $('#message_form_update_' + message_id).textareaAutoHeight();
});

$(document).on('click', '.edit_update_cancel', function () {
  const message_id = $(this).closest('form').attr('message-id');
  document.getElementById('edit_update_main_' + message_id).classList.remove('active');
  document.getElementById('message_aria_list_' + message_id).classList.remove('active');
});

$(document).on('click', '.edit_update_button', function (event) {
  event.preventDefault();
  const message_id = $(this).closest('form').attr('message-id');
  const message = $('#message_form_update_' + message_id).val().replace(/\n+$/g, '');
  document.getElementById('edit_update_main_' + message_id).classList.remove('active');
  document.getElementById('message_aria_list_' + message_id).classList.remove('active');
  document.getElementById('update_form_button_' + message_id).setAttribute('disabled', true);
  // 更新時のアニメーション
  const highlight = document.querySelector('#message_aria_list_' + message_id);
  highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important');
  chatSocket.send(JSON.stringify({
    'command': 'update_message',
    'message_id': message_id,
    'message': message,
  }));
});

// メッセージ削除
$(document).on('click', '.edit_button_delete', function () {
  const message_id = $(this).parent().attr('message-id');
  document.getElementById('modal_content_' + message_id).classList.add('active');
  document.getElementById('mask_' + message_id).classList.add('active');
});

$(document).on('click', '.modal_cancel', function () {
  const message_id = $(this).closest('.edit_button').attr('message-id');
  document.getElementById('modal_content_' + message_id).classList.remove('active');
  document.getElementById('mask_' + message_id).classList.remove('active');
});

$(document).on('click', '.edit_delete_message', function (event) {
  event.preventDefault();
  const message_id = $(this).closest('.edit_button').attr('message-id');
  document.getElementById('modal_content_' + message_id).classList.remove('active');
  document.getElementById('mask_' + message_id).classList.remove('active');
  // 削除時のアニメーション
  const highlight = document.querySelector('#message_aria_list_' + message_id);
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
  chatSocket.send(JSON.stringify({
    'command': 'delete_message',
    'message_id': message_id,
  }));
});

// リプライ削除
$(document).on('click', '.edit_delete_reply', function (event) {
  event.preventDefault();
  const message_id = $(this).closest('.edit_button').attr('message-id');
  document.getElementById('modal_content_' + message_id).classList.remove('active');
  document.getElementById('mask_' + message_id).classList.remove('active');
  // 削除時のアニメーション
  const highlight = document.querySelector('#message_aria_list_' + message_id);
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
  chatSocket.send(JSON.stringify({
    'command': 'delete_reply_message',
    'message_id': message_id,
  }));
});

// replyショートカット
$(document).on('focus', '#reply_form_area', function (event) {
  event.preventDefault();

  // focus時にそれ以外のtextareaを無効化する
  const targetElem = document.querySelectorAll('.form_button');
  const targetCount = targetElem.length;
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].setAttribute('disabled', true);
  }

  const text = $(this).val();
  if (text || text.match(/\S/g)) {
    // disabled属性を削除
    document.getElementById('reply_form_button').removeAttribute('disabled');
  }

  $(document).on('input', '#reply_form_area', function (event) {
    event.preventDefault();
    const text = $(this).val();
    if (!text || !text.match(/\S/g)) {
      // disabled属性を設定
      document.getElementById('reply_form_button').setAttribute('disabled', true);
    } else {
      // disabled属性を削除
      document.getElementById('reply_form_button').removeAttribute('disabled');

      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#reply_form_button').click();
      });
      shortcut.add('meta+Enter', function () {
        $('#reply_form_button').click();
      });
    }
  });
});
