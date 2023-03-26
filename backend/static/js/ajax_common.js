// 検索タグの作成ボタンの処理
$(document).on('click', '.searchtag_2', function (event) {
  event.preventDefault()
  const searchtag = $('form [name=searchtag]').val()
  const csrf = $(this).attr('csrf')
  $('#tag_form')[0].reset()
  document.querySelector('.searchtag_2').setAttribute('disabled', true)
  $.ajax({
    url: '/searchtag/create',
    type: 'POST',
    data: { 'name': searchtag, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      document.querySelector('.searchtag_2').setAttribute('disabled', true)
      let searchtag_add =
        '<a href="?search=' + response.searchtag + '" search="' + response.searchtag + '" class="tag_n_add pjax_search">' + response.searchtag + '</a>'
      $('.searchtag_n_list').append(searchtag_add)
    })
    .fail(function (response) {
      console.log(response)
    })
})

// フォローボタンクリック時の処理
$(document).on('click', '.follow_form', function (event) {
  event.preventDefault()
  const nickname = $(this).attr('value')
  const csrf = $(this).attr('csrf')
  $.ajax({
    url: `/menu/follow/create/${nickname}`,
    type: 'POST',
    data: { 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
  })
    .done(function (response) {
      if (response['is_follow']) {
        $('.follow_change').removeClass('green')
        $('.follow_change').addClass('red')
        $('.red').html('解除する')
        $('.follower_count').html(response['follower_count'])
      } else {
        $('.follow_change').removeClass('red')
        $('.follow_change').addClass('green')
        $('.green').html('フォローする')
        $('.follower_count').html(response['follower_count'])
      }
    })
    .fail(function (response) {
      console.log(response)
    })
})


// いいねボタンクリック時の処理
$(document).on('click', '.like_form', function (event) {
  event.preventDefault()
  const id = $(this).parent().attr('obj-id')
  const path = $(this).parent().attr('path')
  const csrf = $(this).parent().attr('csrf')
  $.ajax({
    url: '/like/form',
    type: 'POST',
    data: { 'id': id, 'path': path, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
  })
    .done(function (response) {
      if (response['is_like']) {
        $('.like_color').removeClass('bi-hand-thumbs-up')
        $('.like_color').parent().removeClass('like_no')
        $('.like_color').addClass('bi-hand-thumbs-up-fill')
        $('.like_color').parent().addClass('like_fill')
        $('#like_count_object_' + id).html(response['total_like'])
      } else {
        $('.like_color').removeClass('bi-hand-thumbs-up-fill')
        $('.like_color').parent().removeClass('like_fill')
        $('.like_color').addClass('bi-hand-thumbs-up')
        $('.like_color').parent().addClass('like_no')
        $('#like_count_object_' + id).html(response['total_like'])
      }
    })
    .fail(function (response) {
      console.log(response)
    })
})


// コメントいいねボタンクリック時の処理
$(document).on('click', '.like_form_comment', function (event) {
  event.preventDefault()
  const comment_id = $(this).parent().attr('comment-id')
  const csrf = $(this).parent().attr('csrf')
  $.ajax({
    url: '/like/form/comment',
    type: 'POST',
    data: { 'comment_id': comment_id, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
  })
    .done(function (response) {
      if (response['is_comment_like']) {
        $('.like_color_' + comment_id).removeClass('bi-hand-thumbs-up')
        $('.like_color_' + comment_id).parent().removeClass('like_no')
        $('.like_color_' + comment_id).addClass('bi-hand-thumbs-up-fill')
        $('.like_color_' + comment_id).parent().addClass('like_fill')
        $('#like_count_' + comment_id).html(response['total_like'])
      } else {
        $('.like_color_' + comment_id).removeClass('bi-hand-thumbs-up-fill')
        $('.like_color_' + comment_id).parent().removeClass('like_fill')
        $('.like_color_' + comment_id).addClass('bi-hand-thumbs-up')
        $('.like_color_' + comment_id).parent().addClass('like_no')
        $('#like_count_' + comment_id).html(response['total_like'])
      }
    })
    .fail(function (response) {
      console.log(response)
    })
})


// 通知リンクをクリックした時の処理
$(document).on('click', '.notification_aria_anker', function () {
  const notification_id = $(this).closest('object').attr('notification-id')
  const csrf = $(this).closest('object').attr('csrf')
  $.ajax({
    url: '/setting/notification/confirmed',
    type: 'POST',
    data: { 'notification_id': notification_id, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function () {
      console.log(response)
    })
    .fail(function () {
      console.log(response)
    })
})


// 通知のバツボタンをクリックした時の処理
$(document).on('click', '.notification_aria_list_2', function (event) {
  event.preventDefault()
  const notification_id = $(this).closest('object').attr('notification-id')
  const csrf = $(this).closest('object').attr('csrf')
  $.ajax({
    url: '/setting/notification/deleted',
    type: 'POST',
    data: { 'notification_id': notification_id, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      document.getElementById('notification_aria_link_' + notification_id).remove()
      if (response.notification_count === 0) {
        $('.bi-bell-fill').removeClass('active')
        $('.bi-exclamation-lg').removeClass('active')
      }
    })
    .fail(function (response) {
      console.log(response)
    })
})


// 通知設定のトグルボタンをクリックした時の処理
$(document).on('click', '.toggle_button', function (event) {
  event.preventDefault()
  const notification = $(this).parent().attr('notification')
  const notification_type = $(this).parent().attr('notification-type')
  const csrf = $(this).closest('#notification_table').attr('csrf')
  $.ajax({
    url: '/setting/notification/update',
    type: 'POST',
    data: { 'notification': notification, 'notification_type': notification_type, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#notification_table').html(response.notification_setting_lists)
    })
    .fail(function (response) {
      console.log(response)
    })
})


// MyPageの全体広告のトグルボタンをクリックした時の処理
$(document).on('click', '.toggle_mypage', function (event) {
  event.preventDefault()
  const is_advertise = $(this).parent().attr('advertise')
  const csrf = $(this).parent().attr('csrf')
  $.ajax({
    url: '/setting/mypage/toggle',
    type: 'POST',
    data: { 'is_advertise': is_advertise, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('#toggle_mypage').html(response.toggle_mypage)
    })
    .fail(function (response) {
      console.log(response)
    })
})


// 広告のリンクをクリックした時の処理
$(document).on('click', '.advertise_anker', function () {
  const advertise_id = $(this).parent().attr('advertise-id')
  const csrf = $(this).parent().attr('csrf')
  $.ajax({
    url: '/url/read',
    type: 'POST',
    data: { 'advertise_id': advertise_id, 'csrfmiddlewaretoken': csrf },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('.advertise_read').html(response.read)
    })
    .fail(function (response) {
      console.log(response)
    })
})
