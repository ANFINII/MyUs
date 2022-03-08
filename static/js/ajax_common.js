// 検索タグの作成ボタンの処理
$(document).on('click', '.main_tag_2', function (event) {
  event.preventDefault();
  const url = $(this).closest('form').attr('action');
  const searchtag = $('form [name=searchtag]').val();
  $('#tag_form')[0].reset();
  document.querySelector('.main_tag_2').setAttribute('disabled', true);
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'searchtag': searchtag, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      document.querySelector('.main_tag_2').setAttribute('disabled', true);
      let searchtag_add =
        '<a class="tag_n_add" href="?search=' + response.searchtag + '">' + response.searchtag + '</a>'
      $('.tag_n_list').append(searchtag_add);
    })
    .fail(function (response) {
      console.log(response);
    })
});

// 検索タグスクロールボタンを押した時の処理 右に0.2秒かけて500px移動
$(document).on('click', '.main_tag_right', function () {
  $('.main_tag_n').animate({
    scrollLeft: $('.main_tag_n').scrollLeft() + 300,
  }, 200);
  return false;
});

// 検索タグスクロールボタンを押した時の処理 左に0.2秒かけて500px移動
$(document).on('click', '.main_tag_left', function () {
  $('.main_tag_n').animate({
    scrollLeft: $('.main_tag_n').scrollLeft() - 300,
  }, 200);
  return false;
});


// フォローボタンクリック時の処理
$(document).on('click', '.follow_form', function (event) {
  event.preventDefault();
  const url = $(this).attr('action');
  const nickname = $(this).children().attr('value');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'nickname': nickname, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
  })
    .done(function (response) {
      if (response['followed']) {
        $('.follow_change').removeClass('btn-success');
        $('.follow_change').addClass('btn-danger');
        $('.btn-danger').html('解除する');
        $('.follower_count').html(response['follower_count']);
      } else {
        $('.follow_change').removeClass('btn-danger');
        $('.follow_change').addClass('btn-success');
        $('.btn-success').html('フォローする');
        $('.follower_count').html(response['follower_count']);
      }
    })
    .fail(function (response) {
      console.log(response);
    })
});


// いいねボタンクリック時の処理
$(document).on('click', '.like_form', function (event) {
  event.preventDefault();
  const id = $(this).attr('value');
  const url = $(this).parent().attr('action');
  const path = $(this).parent().attr('path');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'id': id, 'path': path, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
  })
    .done(function (response) {
      if (response['liked']) {
        $('.like_color').removeClass('bi-hand-thumbs-up');
        $('.like_color').parent().removeClass('like_no');
        $('.like_color').addClass('bi-hand-thumbs-up-fill');
        $('.like_color').parent().addClass('like_fill');
        $('#like_count_object_' + id).html(response['total_like']);
      } else {
        $('.like_color').removeClass('bi-hand-thumbs-up-fill');
        $('.like_color').parent().removeClass('like_fill');
        $('.like_color').addClass('bi-hand-thumbs-up');
        $('.like_color').parent().addClass('like_no');
        $('#like_count_object_' + id).html(response['total_like']);
      }
    })
    .fail(function (response) {
      console.log(response);
    })
});


// コメントいいねボタンクリック時の処理
$(document).on('click', '.like_form_comment', function (event) {
  event.preventDefault();
  const url = $(this).parent().attr('action');
  const comment_id = $(this).attr('value');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'comment_id': comment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
  })
    .done(function (response) {
      if (response['comment_liked']) {
        $('.like_color_' + comment_id).removeClass('bi-hand-thumbs-up');
        $('.like_color_' + comment_id).parent().removeClass('like_no');
        $('.like_color_' + comment_id).addClass('bi-hand-thumbs-up-fill');
        $('.like_color_' + comment_id).parent().addClass('like_fill');
        $('#like_count_' + comment_id).html(response['total_like']);
      } else {
        $('.like_color_' + comment_id).removeClass('bi-hand-thumbs-up-fill');
        $('.like_color_' + comment_id).parent().removeClass('like_fill');
        $('.like_color_' + comment_id).addClass('bi-hand-thumbs-up');
        $('.like_color_' + comment_id).parent().addClass('like_no');
        $('#like_count_' + comment_id).html(response['total_like']);
      }
    })
    .fail(function (response) {
      console.log(response);
    })
});


// 通知リンクをクリックした時の処理
$(document).on('click', '.notification_aria_anker', function () {
  const url = $(this).attr('action');
  const notification_id = $(this).attr('notification-id');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'notification_id': notification_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function () {
    })
    .fail(function () {
    })
});


// 通知のバツボタンをクリックした時の処理
$(document).on('click', '.notification_aria_list_2', function (event) {
  event.preventDefault();
  const url = $(this).closest('form').attr('action');
  const notification_id = $(this).attr('notification-id');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'notification_id': notification_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      document.getElementById('notification_aria_link_' + notification_id).remove();
      if (response.notification_count === 0) {
        $('.bi-bell-fill').removeClass('active');
        $('.bi-exclamation-lg').removeClass('active');
      }
    })
    .fail(function (response) {
      console.log(response);
    })
});


// 通知設定のトグルボタンをクリックした時の処理
$(document).on('click', '.toggle_button', function (event) {
  event.preventDefault();
  const url = $(this).closest('form').attr('action');
  const notification = $(this).closest('form').attr('notification');
  const notification_type = $(this).closest('form').attr('notification-type');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'notification': notification, 'notification_type': notification_type, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#notification_table').html(response.notification_setting_lists);
    })
    .fail(function (response) {
      console.log(response);
    })
});


// MyPageの全体広告のトグルボタンをクリックした時の処理
$(document).on('click', '.toggle_mypage', function (event) {
  event.preventDefault();
  const url = $(this).closest('form').attr('action');
  const advertise = $(this).closest('form').attr('advertise');
  $.ajax({
    url: url,
    type: 'POST',
    data: { 'advertise': advertise, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#auto_advertise').html(response.advertise);
    })
    .fail(function (response) {
      console.log(response);
    })
});
