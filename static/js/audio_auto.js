// 要素を取得
let audios = document.querySelectorAll('audio');

// 再生中はその他のaudioは停止する
for (let i=0; i<audios.length; i++) {
    audios[i].addEventListener('play', function() {
        for (let j=0; j<audios.length; j++) {
            if (audios[j] != this) {
                audios[j].pause();
                this.ontimeupdate = function() {
                    let time = this.currentTime;
                    if (time > 30 && this.classList.contains('audio_auto')) {
                        this.load();
                    }
                }
            }
        }
    }, false);
}
