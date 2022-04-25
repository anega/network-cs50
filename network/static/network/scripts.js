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