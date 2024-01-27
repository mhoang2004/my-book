const moreBtn = document.getElementById('more-btn')
const cutoffText = document.querySelector('.cutoff-text')
const inputComment = document.querySelector('.comment-input-wrapper input')
const cmtWrapperBtn = document.querySelector('.comment-input-btns')
const cmtCancelBtn = document.getElementById('comment-cancel-btn')
const cmtBtn = document.getElementById('comment-btn')
const ratingStar = document.querySelector('.rating-star')
const ratingContent = document.querySelector('.rating-content')

if (cutoffText.offsetHeight < 240) {
    moreBtn.style.display = 'none'
}

moreBtn.addEventListener('click', () => {
    moreBtn.style.display = 'none'

    cutoffText.style.overflow = 'visible'

    cutoffText.style.maxHeight = 'fit-content'
})

inputComment.addEventListener('focus', () => {
    cmtWrapperBtn.style.display = 'block'
})

cmtCancelBtn.addEventListener('click', () => {
    cmtWrapperBtn.style.display = 'none'
    inputComment.value = ''
    cmtBtn.disabled = true
    cmtBtn.classList.remove('btn-primary')
})

inputComment.addEventListener('keyup', () => {
    if (inputComment.value != '') {
        cmtBtn.disabled = false
        cmtBtn.classList.add('btn-primary')
    } else {
        cmtBtn.disabled = true
        cmtBtn.classList.remove('btn-primary')
    }
})

ratingStar.addEventListener('mouseover', (e) => {
    const ratingTexts = ['Poor!', 'Fair!', 'Good!', 'Very Good!', 'Excellent!']
    ratingText = ratingTexts[parseInt(e.target.id)]
    ratingContent.innerHTML = ratingText ? ratingText : ''
})

ratingStar.addEventListener('mouseout', () => {
    ratingContent.innerHTML = ''
})

ratingStar.addEventListener('click', (e) => {
    // do somethings about UI and server stuff...
    let indexStar = parseInt(e.target.id)
    const allStars = document.querySelectorAll('.rating-star i')
    allStars.forEach((star) => {
        if (parseInt(star.id) <= indexStar) {
            star.classList.add('yellow-star')
        } else {
            star.classList.remove('yellow-star')
        }
    })

    fetch('/add_rating', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_id: parseInt(ratingStar.getAttribute('book_id')),
            rating: indexStar + 1,
        }),
    })

    alert('Thank you for rating the book!')
})
