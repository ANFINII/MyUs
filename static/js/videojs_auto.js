let figure = $(".video").hover(hoverVideo, hideVideo);

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

// ホバーアウトするとサムネイル表示
function hideVideo(e) {
    $('video', this).get(0).load();
}
