// Pjax処理
let object_dict = {};
history.replaceState(null, null, location.href);

function pjax_dict(href) {
  const obj = document.querySelector('.main_contents').innerHTML;
  object_dict[href] = obj;
  history.pushState(null, null, href);
}

window.addEventListener('popstate', e => {
  const back_url = location.pathname;
  const back_obj = object_dict[back_url];
  $('.main_contents').html(back_obj);
});


// pjax_button ボタンを押した時の処理
$(document).on('click', '.pjax_button', function (event) {
  event.preventDefault();
  const href = $(this).attr('href');
  $.ajax({
    url: '/pjax',
    type: 'GET',
    data: { 'href': href },
    dataType: 'json',
  })
    .done(function (response) {
      $('.main_contents').html(response.html);
      document.querySelector('.side_menu').checked = false;
      document.querySelector('.dropdown_menu_cloud').checked = false;
      document.querySelector('.dropdown_menu_notice').checked = false;
      document.querySelector('.dropdown_menu_profile').checked = false;
      if (document.querySelector('.chat_remove') != null) {
        document.querySelector('.chat_remove').remove();
      }
      pjax_dict(href);
    })
    .fail(function (response) {
      console.log(response);
    })
});


// pjax_button_userpage ボタンを押した時の処理
$(document).on('click', '.pjax_button_userpage', function (event) {
  event.preventDefault();
  const href = $(this).attr('href');
  const nickname = $(this).attr('data');
  $.ajax({
    url: '/pjax',
    type: 'GET',
    data: { 'href': href, 'nickname': nickname },
    dataType: 'json',
  })
    .done(function (response) {
      $('.main_contents').html(response.html);
      if (document.querySelector('.chat_remove') != null) {
        document.querySelector('.chat_remove').remove();
      }
      pjax_dict(href);
    })
    .fail(function (response) {
      console.log(response);
    })
});


// 検索ボタンを押した時の処理
$(document).on('click', '.search_icon', function (event) {
  event.preventDefault();
  const path = location.pathname;
  const search = document.querySelector('.search_input').value;
  const url = `${path}?search=${search}`
  $.ajax({
    url: '/pjax',
    type: 'GET',
    data: { 'href': path, 'search': search },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('.main_contents').html(response.html);
      if (document.querySelector('.chat_remove') != null) {
        document.querySelector('.chat_remove').remove();
      }
      pjax_dict(url);
    })
    .fail(function (response) {
      console.log(response);
    })
});


// 検索タグを押した時の処理
$(document).on('click', '.pjax_search_button', function (event) {
  event.preventDefault();
  const path = location.pathname;
  const href = $(this).attr('href');
  const url = `${path}${href}`
  const search = $(this).attr('search');
  $.ajax({
    url: '/pjax',
    type: 'GET',
    data: { 'href': path, 'search': search },
    dataType: 'json',
    timeout: 10000,
  })
    .done(function (response) {
      $('.main_contents').html(response.html);
      if (document.querySelector('.chat_remove') != null) {
        document.querySelector('.chat_remove').remove();
      }
      pjax_dict(url);
    })
    .fail(function (response) {
      console.log(response);
    })
});
