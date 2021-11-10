let figure = $(".video").hover(hoverVideo, hideVideo);

// ホバーすると再生開始
function hoverVideo(e) {
    $('video', this).get(0).play();
}

// ホバーアウトするとサムネイル表示
function hideVideo(e) {
    $('video', this).get(0).load();
}
