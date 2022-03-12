// 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#comment_form').submit(function (event) {
  event.preventDefault();
  const url = $(this).attr('action');
  const id = $(this).attr('obj-id');
  const text = $('form [name=text]').val();
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      function scrollBottom() {
        let target = $('.chat_section_main_area').last();
        let position = target.position().top + $('.chat_section_main_area').scrollTop();
        $('.chat_section_main_area').animate({ scrollTop: position }, 500, 'swing');
      }

      let comment_aria_list_add =
        '<div id="comment_aria_list_' + response.comment_id + '" class="comment_aria_list">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="comment_aria_list_1">' +
        '<p>' + response.nickname + '</p>' +
        '<time>' + response.created + '</time>' +
        '</div>' +
        '<div id="comment_aria_list_2_' + response.comment_id + '" class="comment_aria_list_2">' + response.text + '</div>' +
        '<a href="/chat/detail/' + id + '/' + response.title + '/thread/' + response.comment_id + '" class="comment_aria_thread">' +
        'スレッド表示' +
        '<span id="reply_count_' + response.comment_id + '">返信 0 件</span>' +
        '</a>' +
        '<div class="edit_button">' +
        '<a type="button" name="update" comment-id="' + response.comment_id + '" class="edit_button_update">編集</a>' +
        '<a type="button" name="delete" comment-id="' + response.comment_id + '" class="edit_button_delete">削除</a>' +
        '<div id="modal_content_' + response.comment_id + '" class="modal_content">' +
        '<h2 class="modal_content_header">メッセージの削除</h2>' +
        '<span class="modal_content_body_span">このメッセージを削除しますか？</span>' +
        '<div class="modal_content_body">' +
        '<div class="comment_aria_list">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="comment_aria_list_1">' +
        '<p>' + response.nickname + '</p>' +
        '<time>' + response.created + '</time>' +
        '</div>' +
        '<div class="comment_aria_list_2">' + response.text + '</div>' +
        '</div>' +
        '</div>' +
        '<form method="POST" action="/chat/detail/message/delete/' + response.comment_id + '" class="modal_content_footer">' +
        '<input type="button" name="cancel" value="キャンセル" comment-id="' + response.comment_id + '" class="btn btn-light modal_cancel">' +
        '<input type="button" name="delete" value="削除" comment-id="' + response.comment_id + '"  obj-id="' + id + '" class="btn btn-danger edit_delete">' +
        '</form>' +
        '</div>' +
        '<div comment-id="' + response.comment_id + '" id="mask_' + response.comment_id + '" class="mask modal_cancel"></div>' +
        '</div>' +
        '</div>' +
        '<div id="edit_update_main_' + response.comment_id + '" class="edit_update_main_chat">' +
        '<form method="POST" action="/chat/detail/message/update/' + response.comment_id + '" comment-id="' + response.comment_id + '" class="edit_update_chat">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="edit_textarea_caht">' +
        '<textarea name="update_text" rows="1" class="textarea_br" placeholder="メッセージ入力" id="comment_form_update_' + response.comment_id + '" required>' + response.text + '</textarea>' +
        '<div class="chat_frame"></div>' +
        '<div class="comment_input_chat"></div>' +
        '<div class="edit_update_footer">' +
        '<input type="button" name="cancel" value="キャンセル" comment-id="' + response.comment_id + '" class="btn btn-light btn-xs edit_update_cancel">' +
        '<input type="submit" name="update" value="更新" class="btn btn-success btn-xs">' +
        '</div>' +
        '</div>' +
        '</form>' +
        '</div>';
      let obj = document.getElementById('comment_aria_add');
      obj.scrollTop = obj.scrollHeight;
      $('#comment_form')[0].reset();
      $('#user_count').html(response.user_count);
      $('#comment_count').html(response.comment_count);
      $('#comment_aria_add').append(comment_aria_list_add);
      scrollBottom();
      console.log(response)
    })
    .fail(function (response) {
      console.log(response);
    })
});


// 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#reply_form').submit(function (event) {
  event.preventDefault();
  const url = $(this).attr('action');
  const id = $(this).attr('obj-id');
  const comment_id = $(this).attr('comment-id');
  const text = $('form [name=reply]').val();
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'text': text, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      let reply_aria_list_add =
        '<div id="comment_aria_list_' + response.comment_id + '" class="comment_aria_list">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="comment_aria_list_1">' +
        '<p>' + response.nickname + '</p>' +
        '<time> ' + response.created + '</time>' +
        '</div>' +
        '<div id="comment_aria_list_2_' + response.comment_id + '" class="comment_aria_list_2">' + response.text + '</div>' +
        '<div class="edit_button">' +
        '<a type="button" name="update" comment-id="' + response.comment_id + '" class="edit_button_update">編集</a>' +
        '<a type="button" name="delete" comment-id="' + response.comment_id + '" class="edit_button_delete">削除</a>' +
        '<div id="modal_content_' + response.comment_id + '" class="modal_content">' +
        '<h2 class="modal_content_header">メッセージの削除</h2>' +
        '<span class="modal_content_body_span">このメッセージを削除しますか？</span>' +
        '<div class="modal_content_body">' +
        '<div class="comment_aria_list">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="comment_aria_list_1">' +
        '<p>' + response.nickname + '</p>' +
        '<time>' + response.created + '</time>' +
        '</div>' +
        '<div class="comment_aria_list_2">' + response.text + '</div>' +
        '</div>' +
        '</div>' +
        '<form method="POST" action="/chat/detail/message/delete/' + response.comment_id + '" class="modal_content_footer">' +
        '<input type="button" name="cancel" value="キャンセル" comment-id="' + response.comment_id + '" class="btn btn-light modal_cancel">' +
        '<input type="button" name="delete" value="削除" comment-id="' + response.comment_id + '"  obj-id="' + id + '" class="btn btn-danger edit_delete">' +
        '</form>' +
        '</div>' +
        '<div comment-id="' + response.comment_id + '" id="mask_' + response.comment_id + '" class="mask modal_cancel"></div>' +
        '</div>' +
        '</div>' +
        '<div id="edit_update_main_' + response.comment_id + '" class="edit_update_main_chat">' +
        '<form method="POST" action="/chat/detail/message/update/' + response.comment_id + '" comment-id="' + response.comment_id + '" class="edit_update_chat">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="edit_textarea_caht">' +
        '<textarea name="update_text" rows="1" class="textarea_br" placeholder="メッセージ入力" id="comment_form_update_' + response.comment_id + '" required>' + response.text + '</textarea>' +
        '<div class="chat_frame"></div>' +
        '<div class="comment_input_chat"></div>' +
        '<div class="edit_update_footer">' +
        '<input type="button" name="cancel" value="キャンセル" comment-id="' + response.comment_id + '" class="btn btn-light btn-xs edit_update_cancel">' +
        '<input type="submit" name="update" value="更新" class="btn btn-success btn-xs">' +
        '</div>' +
        '</div>' +
        '</form>' +
        '</div>';
      let obj = document.getElementById('reply_aria_add');
      obj.scrollTop = obj.scrollHeight;
      $('#reply_form')[0].reset();
      $('#user_count').html(response.user_count);
      $('#comment_count').html(response.comment_count);
      $('#reply_count_' + comment_id).html('返信 ' + response.reply_count + ' 件');
      $('#reply_aria_add').append(reply_aria_list_add);
      console.log(response);
    })
    .fail(function (response) {
      console.log(response);
    })
});


// コメント 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('#comment_form').submit(function (event) {
  event.preventDefault();
  const url = $(this).attr('action');
  const id = $(this).attr('obj-id');
  const path = $(this).attr('path');
  const text = $('form [name=text]').val();
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'path': path, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      let comment_aria_list_add =
        '<div class="comment_aria_list">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="comment_aria_list_1">' +
        '<p>' + response.nickname + '</p>' +
        '<time>' + ' ' + response.created + '</time>' +
        '</div>' +
        '<div class="comment_aria_list_2">' + response.text + '</div>' +
        '<div class="comment_aria_list_3">' +
        '<i class="bi bi-hand-thumbs-up icon-font" title="いいね数">' + ' ' + '</i>' +
        '<label for="reply_aria_check_id" class="reply_aria_check_id">' + '返信' + '</label>' +
        '</div>' +
        '</div>';
      $('#comment_form')[0].reset();
      $('#comment_count').html(response.comment_count);
      $('#comment_aria_add').append(comment_aria_list_add);
      console.log(response);
    })
    .fail(function (response) {
      console.log(response);
    })
});

// コメントリプライ 送信ボタンにイベントリスナーを設定。内部に Ajax 処理を記述
$('.reply_form').submit(function (event) {
  event.preventDefault();
  const url = $(this).attr('action');
  const id = $(this).attr('obj-id');
  const path = $(this).attr('path');
  const comment_id = $(this).attr('comment-id');
  const text = $('form [name=reply]').val();
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'path': path, 'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      let reply_aria_list_add =
        '<div class="comment_aria_list">' +
        '<a href="/userpage/' + response.nickname + '">' +
        '<img src="' + response.user_image + '" title="' + response.nickname + '" class="profile_image_comment">' +
        '</a>' +
        '<div class="comment_aria_list_1">' +
        '<p>' + response.nickname + '</p>' +
        '<time>' + ' ' + response.created + '</time>' +
        '</div>' +
        '<div class="comment_aria_list_2">' + response.text + '</div>' +
        '<div class="comment_aria_list_3">' +
        '<i class="bi bi-hand-thumbs-up icon-font" title="いいね数">' + ' ' + '</i>' +
        '<label for="reply_aria_check_id" class="reply_aria_check_id">' + '返信' + '</label>' +
        '</div>' +
        '</div>';
      $('#comment_aria_list_reply_' + comment_id)[0].reset();
      $('#reply_count_' + comment_id).html(response.reply_count);
      $('#reply_aria_add').append(reply_aria_list_add);
      console.log(response);
    })
    .fail(function (response) {
      console.log(response);
    })
});


$('#comment_form').submit(function (event) {
  event.preventDefault();
  const url = $(this).attr('action');
  const id = $(this).attr('obj-id');
  const text = $('form [name=text]').val().replace(/\n+$/g, '');
  $('#comment_form')[0].reset();
  document.getElementById('comment_form_area').style.height = '40px';
  document.getElementById('comment_form_button').setAttribute('disabled', true);
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      document.getElementById('comment_form_button').setAttribute('disabled', true);
      $('#user_count').html(response.user_count);
      $('#comment_count').html(response.comment_count);
      $('#chat_section_main_area').append(response.comment_lists);
      const obj = document.getElementById('chat_section_main_area');
      obj.scrollTop = obj.scrollHeight;
      console.log(response);
    })
    .fail(function (response) {
      console.log(response);
    })
});

$('#reply_form').submit(function (event) {
  event.preventDefault();
  const url = $(this).attr('action');
  const id = $(this).attr('obj-id');
  const comment_id = $(this).attr('comment-id');
  const reply = $('form [name=reply]').val().replace(/\n+$/g, '');
  $('#reply_form')[0].reset();
  document.getElementById('reply_form_area').style.height = '40px';
  document.getElementById('reply_form_button').setAttribute('disabled', true);
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'reply': reply, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#user_count').html(response.user_count);
      $('#reply_count_' + comment_id).html('返信 ' + response.reply_count + ' 件');
      $('#chat_section_thread_area').append(response.reply_lists);
      const obj = document.getElementById('chat_section_thread');
      obj.scrollTop = obj.scrollHeight;
      console.log(response);
    })
    .fail(function (response) {
      console.log(response);
    })
});

$(document).on('click', '.edit_update_button', function (event) {
  event.preventDefault();
  const url = $(this).closest('form').attr('action');
  const comment_id = $(this).attr('comment-id');
  const text = $('#comment_form_update_' + comment_id).val().replace(/\n+$/g, '');
  document.getElementById('edit_update_main_' + comment_id).classList.remove('active');
  document.getElementById('comment_aria_list_' + comment_id).classList.remove('active');
  document.getElementById('update_form_button_' + comment_id).setAttribute('disabled', true);
  // 更新時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + comment_id);
  highlight.style.setProperty('background-color', 'rgb(235, 255, 245)', 'important');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'comment_id': comment_id, 'text': text, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      // 成功した時、背景色を戻す
      highlight.style.removeProperty('background-color');
      $('#comment_aria_list_2_' + comment_id).html(response.text);
      console.log(response);
    })
    .fail(function (response) {
      // 失敗した時、背景色を戻す
      highlight.style.removeProperty('background-color');
      console.log(response);
    })
});


$(document).on('click', '.edit_delete_comment', function (event) {
  event.preventDefault();
  const url = $(this).parent().attr('action');
  const id = $(this).attr('obj-id');
  const comment_id = $(this).attr('comment-id');
  document.getElementById('modal_content_' + comment_id).classList.remove('active');
  document.getElementById('mask_' + comment_id).classList.remove('active');
  // 削除時のアニメーション
  const highlight_1 = document.querySelector('#comment_aria_list_' + comment_id);
  const highlight_2 = document.querySelector('#comment_aria_list_cross_' + comment_id);
  highlight_1.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
  if (highlight_2 !== null) {
    highlight_2.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
  }
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_aria_list_' + comment_id).remove();
      $('#edit_update_main_' + comment_id).remove();
      $('#comment_aria_list_2_' + comment_id).html('スレッドが削除されました！');
      $('#user_count').html(response.user_count);
      $('#comment_count').html(response.comment_count);
      console.log(response);
    })
    .fail(function (response) {
      // 失敗した時、背景色を戻す
      highlight_1.style.removeProperty('background-color');
      highlight_2.style.removeProperty('background-color');
      console.log(response);
    })
});


// ホバーすると再生開始
function hoverVideo(e) {
  $('video', this).get(0).play();
  const targetElem = document.querySelectorAll('video');
  const targetCount = targetElem.length;
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].playbackRate = 2.0;
  }
}

$(document).on('click', '.edit_delete_reply', function (event) {
  event.preventDefault();
  const url = $(this).parent().attr('action');
  const id = $(this).attr('obj-id');
  const comment_id = $(this).attr('comment-id');
  // 削除時のアニメーション
  const highlight = document.querySelector('#comment_aria_list_' + comment_id);
  highlight.style.setProperty('background-color', 'rgb(255, 235, 240)', 'important');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#comment_aria_list_' + comment_id).remove();
      $('#user_count').html(response.user_count);
      $('#reply_count_' + response.parent_id).html('返信 ' + response.reply_count + ' 件');
      console.log(response);
    })
    .fail(function (response) {
      // 失敗した時、背景色を戻す
      highlight.style.removeProperty('background-color');
      console.log(response);
    })
});

// 要素を取得
let audios = document.querySelectorAll('audio');

// 再生中はその他のaudioは停止する
for (let i = 0; i < audios.length; i++) {
  audios[i].addEventListener('play', function () {
    for (let j = 0; j < audios.length; j++) {
      if (audios[j] != this) {
        audios[j].pause();
        this.ontimeupdate = function () {
          let time = this.currentTime;
          if (time > 3 && this.classList.contains('audio_auto')) {
            this.load();
          }
        }
      }
    }
  }, false);
}



// スレッドボタンを押した時の処理
$(document).on('click', '.comment_aria_thread', function (event) {
  event.preventDefault();
  const url = $(this).attr('href');
  const comment_id = $(this).attr('comment-id');
  console.log(url)
  console.log(obj_id)
  console.log(comment_id)
  $.ajax({
    url: url,
    type: 'GET',
    data: { 'obj_id': obj_id, 'comment_id': comment_id, 'url': url, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
  })
    .done(function (response) {
      // console.log(response.url)
      // window.location.href = 'http://localhost:8000/'+ url;
      // console.log(response.thread)
      $('#chat_section_thread').html(response.thread);
      console.log(response);
    })
    .fail(function (response) {
      console.log(response);
    })
});
