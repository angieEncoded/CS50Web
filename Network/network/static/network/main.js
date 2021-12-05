


// Set up a simple regex to check the contents of the post
const textCheck = (value) => {
    const re = /^[a-zA-Z0-9.,!"'?:;\s@#$%^&*()[\]_+={}\-]{5,75}$/
    return re.test(value.trim())
}

// From Django documentation how to get the csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const editPost = (id) => {

    // get the id of the content
    const postToEdit = document.querySelector(`#edit-root-${id}`)
    const contentToHide = document.querySelector(`#hideme-${id}`)
    const writtenContent = document.querySelector(`#content-${id}`)

    // Hide the post
    contentToHide.style.display = 'none'

    // get the existing content of that post
    const currentData = writtenContent.innerHTML
    const editTemplate = `
            <form onsubmit="submitform(event, ${id})">
            <textarea class="form-control mb-2" id="textarea-${id}" maxlength=75>${currentData}</textarea>
            <div class="float-end">
            <button class="btn btn-sm btn-logo" type="submit">Save</button>
            <button class="btn btn-sm btn-silver" type="button" onclick="cancelPost(${id})">Cancel</button>
            </div>
            </form>
    `
    // Add the content to the root div
    postToEdit.innerHTML = editTemplate;
}

const submitform = async (event, id) => {
    // Stop the form from default submission
    event.preventDefault();

    // Get the contents of the post
    content = document.querySelector(`#textarea-${id}`).value

    // run it through the checker
    if (!textCheck(content)) {
        return document.querySelector(`#feedback-${id}`).innerHTML = `<span class="text-danger">Please enter 75 or fewer alphanumeric characters and punctuation.</span>`
    } else {
        document.querySelector(`#feedback-${id}`).innerHTML = ""
    }

    const submission = {
        content: content
    }

    // send the update to the server
    try {
        const results = await fetch(`/editpost/${id}`, {
            method: "POST",
            body: JSON.stringify(submission),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        // If fetch failed
        if (!results.ok) { throw new Error(results) }

        const data = await results.json()

        // If the server sent back an error because we did something wrong
        if (data.error) {
            throw new Error(data.error)
        }

        // if the server sent back a post success send feedback and swap the forms back
        if (data.success) {
            const successDiv = document.querySelector(`#feedback-${id}`)
            successDiv.innerHTML = `<span class="text-success">${data.success}</span>`
            document.querySelector(`#edit-root-${id}`).innerHTML = ""
            document.querySelector(`#hideme-${id}`).style.display = "block"
            document.querySelector(`#content-${id}`).innerHTML = data.content
        }

        // Clean up after myself - after 10 seconds the message disappears
        setTimeout(() => {
            document.querySelector(`#feedback-${id}`).innerHTML = ``
        }, 10000)


    } catch (error) {
        const errorDiv = document.querySelector(`#feedback-${id}`)
        errorDiv.innerHTML = `<span class="text-danger">${error}</span>`

        // Clean up after myself - after 10 seconds the message disappears
        setTimeout(() => {
            document.querySelector(`#feedback-${id}`).innerHTML = ``
        }, 10000)
    }


}

const cancelPost = (id) => {

    // get the items again
    const postToEdit = document.querySelector(`#edit-root-${id}`)
    const contentToHide = document.querySelector(`#hideme-${id}`)

    // remove the text area stuff
    postToEdit.innerHTML = ""

    // show the old, unedited content
    contentToHide.style.display = 'block'
}


const likePost = async (id) => {

    try {
        const submission = {
            "addlike": 1
        }

        const results = await fetch(`/like/${id}`, {
            method: "POST",
            body: JSON.stringify(submission),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        // If fetch failed
        if (!results.ok) { throw new Error(results) }

        const data = await results.json()

        // If the server sent back an error because we did something wrong
        if (data.error) {
            throw new Error(data.error)
        }

        // reuse the feedback div
        const successDiv = document.querySelector(`#feedback-${id}`)
        successDiv.innerHTML = `<span class="text-success">${data.success}</span>`


        // update the likes count
        const likesResults = await fetch(`/get_likes/${id}`)

        if (!likesResults.ok) { throw new Error(results) }

        const likesData = await likesResults.json()

        // If the server sent back an error because we did something wrong
        if (likesData.error) {
            throw new Error(likesData.error)
        }

        const likesDiv = document.querySelector(`#likes-${id}`)
        likesDiv.innerHTML = `<i class="las la-heart likes-color"></i>: ${likesData.likes}`

        // Change the button to the 'unlike' button
        const buttonDiv = document.querySelector(`#like-unlike-post-${id}`)
        buttonDiv.innerHTML = `<button class="btn btn-sm btn-outline-secondary unlike-button" onclick="unlikePost(${id})">Unlike <i class="las la-thumbs-up la-1x"></i></button>`

        // Clean up after myself - after 10 seconds the message disappears
        setTimeout(() => {
            document.querySelector(`#feedback-${id}`).innerHTML = ``
        }, 10000)

    } catch (error) {
        const errorDiv = document.querySelector(`#feedback-${id}`)
        errorDiv.innerHTML = `<span class="text-danger">${error}</span>`

        // Clean up after myself - after 10 seconds the message disappears
        setTimeout(() => {
            document.querySelector(`#feedback-${id}`).innerHTML = ``
        }, 10000)
    }


}

const unlikePost = async (id) => {

    try {
        const submission = {
            "removelike": 1
        }

        const results = await fetch(`/unlike/${id}`, {
            method: "POST",
            body: JSON.stringify(submission),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        // If fetch failed
        if (!results.ok) { throw new Error(results) }

        const data = await results.json()

        // If the server sent back an error because we did something wrong
        if (data.error) {
            throw new Error(data.error)
        }

        // reuse the feedback div
        const successDiv = document.querySelector(`#feedback-${id}`)
        successDiv.innerHTML = `<span class="text-success">${data.success}</span>`


        // update the likes count
        const likesResults = await fetch(`/get_likes/${id}`)

        if (!likesResults.ok) { throw new Error(results) }

        const likesData = await likesResults.json()

        // If the server sent back an error because we did something wrong
        if (likesData.error) {
            throw new Error(likesData.error)
        }

        const likesDiv = document.querySelector(`#likes-${id}`)
        likesDiv.innerHTML = `<i class="las la-heart likes-color"></i>: ${likesData.likes}`

        // Change the button to the 'like' button
        const buttonDiv = document.querySelector(`#like-unlike-post-${id}`)
        buttonDiv.innerHTML = `<button class="btn btn-sm btn-outline-secondary like-button" onclick="likePost(${id})">Like! <i class="las la-thumbs-up la-1x"></i></button>`

        // Clean up after myself - after 10 seconds the message disappears
        setTimeout(() => {
            document.querySelector(`#feedback-${id}`).innerHTML = ``
        }, 10000)

    } catch (error) {
        const errorDiv = document.querySelector(`#feedback-${id}`)
        errorDiv.innerHTML = `<span class="text-danger">${error}</span>`

        // Clean up after myself - after 10 seconds the message disappears
        setTimeout(() => {
            document.querySelector(`#feedback-${id}`).innerHTML = ``
        }, 10000)
    }



}



