// This is a hook to manage the input. Create react app seems overkill for this project so I will just put it all here
const useInput = (validateValue) => {

    const [enteredValue, setEnteredValue] = React.useState("")                            // Manage state slice to read the input's value
    const [wasTouched, setWasTouched] = React.useState(false)                             // Manage state slice to track whether the user touched the input
    const valueIsValid = validateValue(enteredValue);                               // This will run the function we send into the hook to test the validity (some regex or whatever)
    const hasError = !valueIsValid && wasTouched;                                   // Track whether the input is allowed or not and expose that to the caller

    // Give the user immediate feedback on the state of the input
    const valueChangeHandler = event => {
        setEnteredValue(event.target.value)
        setWasTouched(true)
    }
    //const valueBlurHandler = () => { setWasTouched(true); }                         // Track when the user leaves the input changed this in favor of immediate feedback

    // This is a reset function we can call in the case that the form was submitted successfully (remember to set value prop on input)
    const resetInput = () => {
        setEnteredValue("");
        setWasTouched(false)
    }

    // Return the state slices to the caller for use in the form
    return {
        value: enteredValue,
        valueIsValid: valueIsValid,
        hasError: hasError,
        resetInput,
        valueChangeHandler,
        // valueBlurHandler
    }
}

// Set up a simple regex to check the contents of the post
const textCheck = (value) => {
    const re = /^[a-zA-Z0-9.,!"'?:;\s@#$%^&*()[\]_+=-{}]{5,75}$/
    return re.test(value.trim())
}






// Need to fetch all posts
// Need to be able to edit a post
// Need to be able to like a post
// Need to be able to follow a user



function App() {

    const [loggedIn, setIsLoggedIn] = React.useState(false)
    const [postSuccess, setPostSuccess] = React.useState(false);
    const [isPending, setIsPending] = React.useState(false);
    const [apiError, setApiError] = React.useState(false)
    const [apiMessage, setApiMessage] = React.useState("")

    // State slices for the posts
    const [postErrorMessage, setPostErrorMessage] = React.useState("")
    const [postsPending, setPostsPending] = React.useState(false)

    // Check if there is a sessionid for this user
    const isLoggedIn = () => {
        let sessioncookie = Cookies.get('sessionid')
        console.log(sessioncookie)
        if (sessioncookie != "") {
            setIsLoggedIn(true)
        } else {
            setIsLoggedIn(false)
        }
    }

    React.useEffect(() => {
        isLoggedIn()
        console.log(loggedIn)
    }, [])


    // NEW POST LOGIC - RUN THROUGH MY HOOK TO DEAL WITH VALIDITY
    //=================================
    const {
        value: newPost,
        valueIsValid: newPostIsValid,
        hasError: newPostHasError,
        resetInput: resetNewPostInput,
        valueChangeHandler: newPostChangeHandler
    } = useInput(textCheck)

    const clearForm = () => {
        resetNewPostInput();
    }

    let formIsValid = false; // set up a variable to handle the overall form validity
    if (newPostIsValid) { formIsValid = true; } // If form isn't valid don't give them a button
    const addPost = async (event) => {

        event.preventDefault(); // Prevent the form from firing
        if (!formIsValid) { return; }// in case they somehow got into here

        setPostSuccess(false) // deal with the response from server
        setIsPending(true); // turn on the loading screen while we submit

        const formPost = { "content": newPost }

        // Post the form
        try {
            const results = await fetch('/newpost', {
                method: "POST",
                body: JSON.stringify(formPost),
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            // If fetch failed
            if (!results.ok) { throw new Error(results) }
            const data = await results.json()

            // If my API returns an error throw it to the catch
            if (data.type != "success") { throw new Error(data.message) }

            // Update the api message state
            setApiMessage(data.message)
            setPostSuccess(true)
            setIsPending(false)
            clearForm()
        } catch (error) {
            setApiMessage("Catastrpophic error")
            setPostSuccess(false)
            setIsPending(false)
            console.log(error)
        }
    }

    const resetStates = () => {
        setApiMessage("")
        setPostSuccess(false)
        setIsPending(false)
        setApiError(false)
    }


    // helper class for form feedback
    const newPostClasses = newPostHasError ? 'form-control is-invalid' : 'form-control'

    // Get all posts
    const getPosts = async () => {
        try {
            const results = await fetch("/allposts");
            if (!results.ok) { throw new Error("Unable to fetch the results") }
        } catch (error) {
            console.log(error)
        }

    }




    return (

        <React.Fragment>
            <div className="container">
                {!isPending && apiError && apiMessage &&
                    <div className="alert alert-success text-center alert-dismissible" role="alert">
                        {apiMessage}
                        <button type="button" className="btn-close" onClick={() => resetStates()}></button>
                    </div>
                }
                {!isPending && postSuccess && apiMessage &&
                    <div className="alert alert-success text-center alert-dismissible" role="alert">
                        {apiMessage}
                        <button type="button" className="btn-close" onClick={() => resetStates()}></button>
                    </div>
                }
            </div>
            {loggedIn &&
                <div className="container">
                    <h2>New Post</h2>
                    {newPostHasError && <p className="text-danger">Post must be 5-75 characters long. Allowed characters are a-zA-Z0-9 and punctuation.</p>}
                    {!newPostHasError && <p>Enter your post content below:</p>}

                    <form onSubmit={addPost}>
                        <div className="mb-3">
                            <textarea className={newPostClasses} onChange={newPostChangeHandler} cols="10" rows="3" maxLength="75" value={newPost}></textarea>
                        </div>

                        <div className="text-end">
                            <button className="btn btn-silver" onClick={clearForm}>Clear Form</button>
                            <button disabled={!formIsValid} className="btn btn-logo mx-1" type="submit">Submit</button>
                        </div>
                    </form>
                    <hr />
                </div>
            }
        </React.Fragment>
    )
}






ReactDOM.render(<App />, document.querySelector("#root"))