// WebSocketオブジェクト
let ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
const obj_id = JSON.parse(document.getElementById('obj_id').textContent);
const chatSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + '/ws/chat/detail/' + obj_id);

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
    if (document.querySelector('.comment_aria_check') != null) {
      document.querySelector('.comment_aria_check').checked = true;
    }
  } else {
    $('.chat_section_thread_area').html(back_obj);
    if (document.querySelector('.comment_aria_check') != null) {
      document.querySelector('.comment_aria_check').checked = false;
    }
  }
});

// スレッドボタンを押した時の処理
$(document).on('click', '.comment_aria_thread', function (event) {
  event.preventDefault();
  const href = $(this).attr('href');
  const url = $(this).attr('thread');
  const comment_id = $(this).attr('comment-id');
  $.ajax({
    url: url,
    type: 'GET',
    data: { 'obj_id': obj_id, 'comment_id': comment_id },
    dataType: 'json',
  })
    .done(function (response) {
      $('.chat_section_thread_area').html(response.thread);
      document.querySelector('.comment_aria_check').checked = true;
      pjax_thread_dict(href);
    })
    .fail(function (response) {
      console.log(response);
    })
});

// バツボタンを押した時の処理
$(document).on('click', '.bi-x', function () {
  document.querySelector('.comment_aria_check').checked = false;
  const href = $(this).attr('href');
  pjax_thread_dict(href);
});

// chatSocket の websocket 処理
chatSocket.onmessage = function (event) {
  let data = JSON.parse(event.data);
  if (data['command'] === 'create_message') {
    document.getElementById('comment_form_button').setAttribute('disabled', true);
    const response = data['message'];
    $('#chat_section_main_area').append(response.comment_lists);
    $('#joined').html(response.joined);
    $('#thread').html(response.thread);
    const login_user_id = document.getElementById('user_id').textContent;
    if (login_user_id != response.user_id) {
      $('#edit_button_' + response.comment_id).remove();
      $('#edit_update_main_' + response.comment_id).remove();
    }
    const obj = document.getElementById('chat_section_main_area');
    obj.scrollTop = obj.scrollHeight;
  } else if (data['command'] === 'create_reply_message') {
    const response = data['message'];
    if ('/chat/detail/' + obj_id + '/thread/' + response.parent_id === location.pathname) {
      document.getElementById('reply_form_button').setAttribute('disabled', true);
      $('#joined').html(response.joined);
      $('#reply_num_' + response.parent_id).html('返信 ' + response.reply_num + ' 件');
      $('#chat_section_thread_area_' + response.parent_id).append(response.reply_lists);
      const login_user_id = document.getElementById('user_id').textContent;
      if (login_user_id != response.user_id) {
        $('#edit_button_' + response.comment_id).remove();
        $('#edit_update_main_' + response.comment_id).remove();
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
    const highlight = document.querySelector('#comment_aria_list_' + response.comment_id);
    highlight.style.removeProperty('background-color');
    $('#comment_aria_list_2_' + response.comment_id).html(response.text);
    $('#comment_aria_list_thread_' + response.comment_id).html(response.text);
    pjax_thread_dict(location.pathname)
  } else if (data['command'] === 'delete_message') {
    const response = data['message'];
    const highlight = document.querySelector('#comment_aria_list_cross_' + response.comment_id);
    if (highlight !== null) {
      highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
    }
    $('#comment_aria_list_' + response.comment_id).remove();
    $('#edit_update_main_' + response.comment_id).remove();
    $('#comment_aria_list_thread_' + response.comment_id).html('スレッドが削除されました!');
    $('#joined').html(response.joined);
    $('#thread').html(response.thread);
  } else if (data['command'] === 'delete_reply_message') {
    const response = data['message'];
    const url = location.pathname;
    if ('/chat/detail/' + obj_id + '/thread/' + response.parent_id === url) {
      $('#comment_aria_list_' + response.comment_id).remove();
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

// メッセージ作成
$('#comment_form').submit(function (event) {
  event.preventDefault();
  const obj_id = JSON.parse(document.getElementById('obj_id').textContent);
  const message = $('form [name=text]').val();
  $('#comment_form')[0].reset();
  document.getElementById('comment_form_area').style.height = '40px';
  document.getElementById('comment_form_button').setAttribute('disabled', true);
  chatSocket.send(JSON.stringify({
    'command': 'create_message',
    'obj_id': obj_id,
    'message': message,
  }));
});

// リプライ作成
$('#reply_form').submit(function (event) {
  event.preventDefault();
  const obj_id = JSON.parse(document.getElementById('obj_id').textContent);
  const parent_id = document.getElementById('parent_id').getAttribute('value');
  const message = $('form [name=reply]').val().replace(/\n+$/g, '');
  $('#reply_form')[0].reset();
  document.getElementById('reply_form_area').style.height = '40px';
  document.getElementById('reply_form_button').setAttribute('disabled', true);
  chatSocket.send(JSON.stringify({
    'command': 'create_reply_message',
    'obj_id': obj_id,
    'message': message,
    'parent_id': parent_id,
  }));
});

// メッセージ編集
$(document).on('click', '.edit_button_update', function () {
  const comment_id = $(this).parent().attr('comment-id');
  document.getElementById('edit_update_main_' + comment_id).classList.add('active');
  document.getElementById('comment_aria_list_' + comment_id).classList.add('active');
  document.getElementById('comment_form_update_' + comment_id).style.height = '40px';
  $('#comment_form_update_' + comment_id).textareaAutoHeight();
});

$(document).on('click', '.edit_update_cancel', function () {
  const comment_id = $(this).closest('form').attr('comment-id');
  document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
  document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
});

$(document).on('click', '.edit_update_button', function (event) {
  event.preventDefault();
  const comment_id = $(this).closest('form').attr('comment-id');
  const message = $('#comment_form_update_' + comment_id).val().replace(/\n+$/g, '');
  document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
  document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
  document.getElementById('update_form_button_' + comment_id).setAttribute('disabled', true);
  // 更新時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + comment_id);
  highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important');
  chatSocket.send(JSON.stringify({
    'command': 'update_message',
    'comment_id': comment_id,
    'message': message,
  }));
});

// メッセージ削除
$(document).on('click', '.edit_button_delete', function () {
  const comment_id = $(this).parent().attr('comment-id');
  document.getElementById('modal_content_' + comment_id).classList.add('active');
  document.getElementById('mask_' + comment_id).classList.add('active');
});

$(document).on('click', '.modal_cancel', function () {
  const comment_id = $(this).closest('.edit_button').attr('comment-id');
  document.getElementById('modal_content_' + comment_id).classList.remove('active');
  document.getElementById('mask_' + comment_id).classList.remove('active');
});

$(document).on('click', '.edit_delete_comment', function (event) {
  event.preventDefault();
  const comment_id = $(this).closest('.edit_button').attr('comment-id');
  document.getElementById('modal_content_' + comment_id).classList.remove('active');
  document.getElementById('mask_' + comment_id).classList.remove('active');
  // 削除時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + comment_id);
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
  chatSocket.send(JSON.stringify({
    'command': 'delete_message',
    'comment_id': comment_id,
  }));
});

// リプライ削除
$(document).on('click', '.edit_delete_reply', function (event) {
  event.preventDefault();
  const comment_id = $(this).closest('.edit_button').attr('comment-id');
  document.getElementById('modal_content_' + comment_id).classList.remove('active');
  document.getElementById('mask_' + comment_id).classList.remove('active');
  // 削除時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + comment_id);
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
  chatSocket.send(JSON.stringify({
    'command': 'delete_reply_message',
    'comment_id': comment_id,
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