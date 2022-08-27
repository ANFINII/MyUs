// Pjax処理
let object_dict = {};
history.replaceState(null, null, location.href);

window.addEventListener('popstate', e => {
  const back_url = location.pathname;
  const back_obj = object_dict[back_url];
  $('.main_contents').html(back_obj);
});

function pjax_dict(href) {
  const obj = document.querySelector('.main_contents').innerHTML;
  object_dict[href] = obj;
  history.pushState(null, null, href);
}

function ajax_data(href, data) {
  $.ajax({
    url: '/pjax',
    type: 'GET',
    data: data,
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
}


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
  data = { 'href': href, 'nickname': nickname }
  ajax_data(href, data)
});


// 検索ボタンを押した時の処理
$(document).on('click', '.search_icon', function (event) {
  event.preventDefault();
  const href = location.pathname;
  const search = $('.search_input').val();
  const url = `${href}?search=${search}`
  const nickname = $('.userpage_image').attr('title');
  data = { 'href': href, 'search': search, 'nickname': nickname }
  ajax_data(url, data)
});


// 検索タグを押した時の処理
$(document).on('click', '.pjax_search', function (event) {
  event.preventDefault();
  const href = location.pathname;
  const search = $(this).attr('search');
  const url = `${href}?search=${search}`
  const nickname = $('.userpage_image').attr('title');
  data = { 'href': href, 'search': search, 'nickname': nickname }
  ajax_data(url, data)
});


// ハッシュタグを押した時の処理
$(document).on('click', '.pjax_hash_search', function (event) {
  event.preventDefault();
  let href = location.pathname;
  if (href.match('/video'))   { href = 'video' }
  if (href.match('/live'))    { href = 'live' }
  if (href.match('/music'))   { href = 'music' }
  if (href.match('/picture')) { href = 'picture' }
  if (href.match('/blog'))    { href = 'blog' }
  if (href.match('/chat'))    { href = 'chat' }
  if (href.match('/collabo')) { href = 'collabo' }
  const search = $(this).attr('search');
  const url = `/${href}?search=${search}`
  const nickname = $('.userpage_image').attr('title');
  data = { 'href': href, 'search': search, 'nickname': nickname }
  ajax_data(url, data)
});
