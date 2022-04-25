document.addEventListener('DOMContentLoaded', () => {
    const follow_btn = document.getElementById('follow-btn')
    if (follow_btn) {
        follow_btn.addEventListener('click', (event) => {
            event.preventDefault()
            const csrfToken = getCookie('csrftoken')
            const targetLink = event.target
            const url = targetLink.href
            const userId = targetLink.dataset.id
            const followAction = targetLink.dataset.action
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: userId,
                    action: followAction
                })
            })
                .then(response => {
                    if (response.ok) return response.json()
                    throw new Error()
                })
                .then(data => {
                    console.log(data)
                    if (data['status'] === 'ok') {
                        targetLink.dataset.action = followAction === 'follow' ? 'unfollow' : 'follow'
                        targetLink.innerHTML = followAction === 'follow' ? 'Unfollow' : 'Follow'
                        const prevFollowers = document.getElementsByClassName('followers-count')[0]
                        let prevFollowersCount = parseInt(prevFollowers.innerHTML)
                        if (followAction === 'follow') {
                            prevFollowersCount += 1
                            if (prevFollowersCount === 1) {
                                prevFollowers.innerHTML = `${prevFollowersCount} follower`
                            } else {
                                prevFollowers.innerHTML = `${prevFollowersCount} followers`
                            }
                        } else {
                            prevFollowersCount -= 1
                            if (prevFollowersCount === 1) {
                                prevFollowers.innerHTML = `${prevFollowersCount} follower`
                            } else {
                                prevFollowers.innerHTML = `${prevFollowersCount} followers`
                            }
                        }
                    } else if (data['status'] === 'error') {
                        throw new Error()
                    }
                })
                .catch(error => {
                    console.log('Something went wrong. Please try again later.')
                })
        })
    }

    // Edit post
    const editPostBtnList = document.querySelectorAll('.edit-post-btn')
    if (editPostBtnList.length) {
        editPostBtnList.forEach(editPostBtn => {
            editPostBtn.addEventListener('click', (event) => {
                event.preventDefault()
                const editTargetBtn = event.currentTarget
                editTargetBtn.style.display = 'none'
                editTargetBtn.parentNode.querySelector('.save-post-btn').style.display = 'inline'
                editTargetBtn.parentNode.querySelector('.cancel-post-btn').style.display = 'inline'
                const postContentWrap = editTargetBtn.closest('.post').querySelector('.post-body')
                postContentWrap.querySelector('.post-body-content').style.display = 'none'
                const postContent = postContentWrap.querySelector('.post-body-content-editable')
                postContent.style.display = 'block'
                postContent.focus()
            })
        })
    }

    // Save post
    const savePostBtnList = document.querySelectorAll('.save-post-btn')
    if (savePostBtnList.length) {
        savePostBtnList.forEach(saveBtn => {
            saveBtn.addEventListener('click', (event) => {
                event.preventDefault()
                const saveBtnTarget = event.currentTarget
                saveBtnTarget.style.display = 'none'
                saveBtnTarget.parentNode.querySelector('.cancel-post-btn').style.display = 'none'
                saveBtnTarget.parentNode.querySelector('.edit-post-btn').style.display = 'inline'
                const postContentWrap = saveBtnTarget.closest('.post').querySelector('.post-body')
                const updatedBodyText = postContentWrap.querySelector('.post-body-content-editable').value
                console.log(updatedBodyText)
            })
        })
    }

    // Cancel post editing
    const cancelPostBtnList = document.querySelectorAll('.cancel-post-btn')
    if (cancelPostBtnList.length) {
        cancelPostBtnList.forEach(cancelBtn => {
            cancelBtn.addEventListener('click', event => {
                event.preventDefault()
                const cancelTargetBtn = event.currentTarget
                cancelTargetBtn.style.display = 'none'
                cancelTargetBtn.parentNode.querySelector('.save-post-btn').style.display = 'none'
                cancelTargetBtn.parentNode.querySelector('.edit-post-btn').style.display = 'inline'
                const postContentWrap = cancelTargetBtn.closest('.post').querySelector('.post-body')
                postContentWrap.querySelector('.post-body-content-editable').style.display = 'none'
                postContentWrap.querySelector('.post-body-content').style.display = 'block'
            })
        })
    }
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}