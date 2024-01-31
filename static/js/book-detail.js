const moreBtn = document.getElementById('more-btn')
const cutoffText = document.querySelector('.cutoff-text')
const commentsContainer = document.querySelector('.comment-items')
const inputComment = document.querySelector('.comment-input-wrapper input')
const cmtWrapperBtn = document.querySelector('.comment-input-btns')
const cmtSubmitBtn = document.getElementById('comment-submit-btn')
const cmtCancelBtn = document.getElementById('comment-cancel-btn')
const ratingStar = document.querySelector('.rating-star')
const ratingContent = document.querySelector('.rating-content')

if (cutoffText.offsetHeight < 240) {
    moreBtn.style.display = 'none'
}

const createCommentBlock = (companyName, commentData) => {
    var commentItem = document.createElement('div')
    commentItem.classList.add('comment-item', 'mt-4')

    var avtImage = document.createElement('img')
    avtImage.src = '../static/img/default-avt.jpg'
    avtImage.width = 44
    avtImage.height = 44
    avtImage.alt = 'avt'
    avtImage.classList.add('cmt-avt')

    var commentInputWrapper = document.createElement('div')
    commentInputWrapper.classList.add('comment-input-wrapper')

    var userNameElement = document.createElement('span')
    userNameElement.innerHTML = '<b>' + companyName + ' User</b>'

    var timeAgoElement = document.createElement('span')
    timeAgoElement.classList.add('comment-time')
    timeAgoElement.textContent = ' just now'

    var commentContentElement = document.createElement('p')
    commentContentElement.classList.add('comment-content')
    commentContentElement.textContent = commentData

    // Append elements to the commentItem
    commentItem.appendChild(avtImage)
    commentItem.appendChild(commentInputWrapper)
    commentInputWrapper.appendChild(userNameElement)
    commentInputWrapper.appendChild(timeAgoElement)
    commentInputWrapper.appendChild(commentContentElement)

    return commentItem
}

const addCommentContent = () => {
    const commentData = inputComment.value
    const companyName = commentsContainer.getAttribute('company_name')

    fetch('/add_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_id: parseInt(ratingStar.getAttribute('book_id')),
            content: commentData,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
        })
        .catch((error) => {
            console.error('Error:', error)
        })

    // create new block of comment
    const commentItem = createCommentBlock(companyName, commentData)
    commentsContainer.insertBefore(commentItem, commentsContainer.firstChild)

    // + 1 comment length
    const commentNum = document.getElementById('comment-num')
    commentNum.innerHTML = parseInt(commentNum.innerHTML) + 1

    // clear input
    cmtCancelBtn.click()
}

moreBtn.addEventListener('click', () => {
    moreBtn.style.display = 'none'
    cutoffText.style.overflow = 'visible'
    cutoffText.style.maxHeight = 'fit-content'
})

inputComment.addEventListener('focus', () => {
    cmtWrapperBtn.style.display = 'block'
})

cmtSubmitBtn.addEventListener('click', () => {
    if (!cmtSubmitBtn.disabled) addCommentContent()
})

cmtCancelBtn.addEventListener('click', () => {
    cmtWrapperBtn.style.display = 'none'
    inputComment.value = ''
    cmtSubmitBtn.disabled = true
    cmtSubmitBtn.classList.remove('btn-primary')
})

inputComment.addEventListener('keyup', (e) => {
    if (inputComment.value != '') {
        cmtSubmitBtn.disabled = false
        cmtSubmitBtn.classList.add('btn-primary')

        if (e.key === 'Enter') {
            addCommentContent()
            inputComment.blur()
            inputComment.focus()
        }
    } else {
        cmtSubmitBtn.disabled = true
        cmtSubmitBtn.classList.remove('btn-primary')
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

    const ratingVotes = document.getElementById('rating-votes')
    ratingVotes.innerHTML = parseInt(ratingVotes.innerHTML) + 1

    alert('Thank you for rating the book!')
})
