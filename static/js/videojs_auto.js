let figure = $(".video").hover(playVideo, hideVideo);

// ホバーすると再生開始
function playVideo(e) {
    $('video', this).get(0).play();
}

// ホバーアウトするとサムネイル表示
function hideVideo(e) {
    $('video', this).get(0).load();
}
