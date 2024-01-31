const priorBtn = document.getElementById('prior-btn')
const nextBtn = document.getElementById('next-btn')
const readingHeader = document.querySelector('.reading-header')
priorBtn.addEventListener('click', () => {
    if (!priorBtn.disabled) {
    }
})

nextBtn.addEventListener('click', () => {
    if (!nextBtn.disabled) {
        const pageValue = parseInt(readingHeader.getAttribute('data-page'))

        fetch('/next_page', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                page: pageValue,
            }),
        })
    }
})
