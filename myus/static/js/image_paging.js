document.addEventListener('DOMContentLoaded', function () {
  const images = document.querySelectorAll('.comic_page')

  function showImage(index) {
    for (i = 0; i < images.length; i++) {
      images[i].style.display = 'none'
    }
    images[index].style.display = 'block'
  }

  let currentIndex = 0
  function prevImage() {
    currentIndex--
    if (currentIndex < 0) {
      currentIndex = images.length - 1
    }
    showImage(currentIndex)
  }

  function nextImage() {
    currentIndex++
    if (currentIndex >= images.length) {
      currentIndex = 0;
    }
    showImage(currentIndex)
  }

  const prevButton = document.getElementById('prevButton')
  const nextButton = document.getElementById('nextButton')
  prevButton.addEventListener('click', prevImage)
  nextButton.addEventListener('click', nextImage)
  showImage(currentIndex)
})
