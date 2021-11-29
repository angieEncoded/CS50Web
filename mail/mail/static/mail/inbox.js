document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Get the form and assign to a var
  const form = document.querySelector("#compose-form")
  form.onsubmit = (event) => {

    // I know there are no event handlers on this to leak
    document.querySelector("#errors-root").textContent = ""

    // stop it from submitting the form to the server
    event.preventDefault();

    // get values
    const recipients = document.querySelector("#compose-recipients").value
    const subject = document.querySelector("#compose-subject").value
    const body = document.querySelector("#compose-body").value

    // Set up submission form 
    const submission = {
      recipients: recipients,
      subject: subject,
      body: body
    }
    console.log(submission)
    // Submit the email
    fetch("/emails", {
      method: 'POST',
      body: JSON.stringify(submission)
    })
      .then(results => {
        return results.json()
      })
      .then(results => {
        if (results.error) {

          // Alert the user that there was a problem
          const errorMessage = document.createElement("div")
          errorMessage.innerHTML =
            `
            <div class="alert alert-danger text-center" role="alert">
            ${results.error}
            </div>
          `
          document.querySelector("#errors-root").append(errorMessage);

          // console.log("Could not send the email")
        } else {
          load_mailbox('sent');
        }

      })
      .catch(error => {
        console.log(error)
      })
  }

});




function compose_reply(mailid) {

  //console.log("got to the correct function")
  // clear out any old errors
  document.querySelector("#errors-root").textContent = ""

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none'

  // load the email data from the server
  fetch(`/emails/${mailid}`)
    .then(results => {
      return results.json()
    })
    .then(results => {
      console.log(results)

      // update the composition field with the sender's information
      document.querySelector('#compose-recipients').value = results.sender;

      // Check if there is already a "Re:" in the field
      if (!results.subject.startsWith("Re:")) {
        document.querySelector('#compose-subject').value = `Re: ${results.subject}`;
      } else {
        document.querySelector('#compose-subject').value = results.subject;
      }

      // Set up the body field:
      const bodyText =
        `
        \n
        On ${results.timestamp} ${results.sender} wrote: \n
        ${results.body}
    
      `
      document.querySelector('#compose-body').value = bodyText;
    })
}



function compose_email() {

  // clear out any old errors
  document.querySelector("#errors-root").textContent = ""

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none'

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // get the root element
  const emailsView = document.querySelector('#emails-view')

  // Show the mailbox and hide other views
  emailsView.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none'
  // Show the mailbox name
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the relevant emails to display
  fetch(`/emails/${mailbox}`)
    .then((results) => {
      if (results.ok) {
        return results.json()
      }
    }).then(results => {
      // create an element for every email
      const header = document.createElement("div")
      header.innerHTML =
        `         
      <div class="row text-center">
        <div class="col"><strong>Sender:</strong></div>
        <div class="col"><strong>Subject:</strong></div>
        <div class="col"><strong>Timestamp:</strong></div>
      </div>
      <hr>
      `
      emailsView.append(header);

      for (let item of results) {
        // console.log(item)
        const element = document.createElement("div")

        // Add data attributes to keep track of the email id and the type of mail it is
        element.setAttribute("data-mailtype", mailbox)
        element.setAttribute("data-emailid", item.id)

        element.innerHTML =
          `
          <div class="row text-center border mb-1 clickable ${mailbox === 'inbox' && !item.read ? "bg-white" : "bg-light"}">
            <div class="col">${item.sender}</div>
            <div class="col">${item.subject}</div>
            <div class="col">${item.timestamp}</div>
          </div>
          `
        element.addEventListener('click', function (event) {
          // Scope queryselector in only this element
          const specificMail = element.dataset.emailid
          const mailtype = element.dataset.mailtype
          // call up the specific mail function
          getSingleEmail(specificMail, mailtype)

        });
        emailsView.append(element);
      }
    })
}

function runArchive() {
  const button = document.querySelector("#archiveButton")

  // console.log(button.dataset.archived)
  // console.log(button.dataset.emailid)
  // The email is archived
  if (button.dataset.archived === "true") {
    fetch(`/emails/${button.dataset.emailid}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })
    })
      .then(results => {
        console.log(results)
        // load the inbox
        load_mailbox("inbox")
      })
    // The email is not archived
  } else {
    fetch(`/emails/${button.dataset.emailid}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })
      .then(results => {
        console.log(results)
        load_mailbox("inbox")
      })
  }
}


function getSingleEmail(specificMail, mailtype) {

  // clear any old emails being displayed
  document.querySelector('#single-email-view').textContent = "";

  // Clear all other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';

  // Clear all errors
  document.querySelector("#errors-root").textContent = "";

  // Fetch email
  fetch(`/emails/${specificMail}`)
    .then(results => {
      return results.json()
    })
    .then(results => {
      // Create the template for the email display
      const email = document.createElement('div')
      email.innerHTML = `
        <div><strong>Sender:</strong> ${results.sender}</div>
        <div><strong>Recipients:</strong> ${results.recipients}</div>
        <div><strong>Subject:</strong> ${results.subject}</div>
        <div><strong>Timestamp:</strong> ${results.timestamp}</div>

        <div>
          <strong>Body:</strong>
          <br />
          ${results.body}
        </div>
        <hr>  
      `
      // Don't add the button for sent mails. Passed in via data attributes
      if (mailtype !== "sent") {
        email.innerHTML +=
          `
          <button class="btn btn-logo" onclick="compose_reply(${results.id})">
            Reply to message
          </button>
          <button class="btn btn-silver" data-archived=${results.archived} data-emailid=${results.id} onclick="runArchive()" id="archiveButton">
             ${results.archived ? "Unarchive Email" : "Archive Email"}
          </button>
        `
      }


      document.querySelector("#single-email-view").append(email)
      // console.log(results)
    })

  // Mark the mail as read
  fetch(`/emails/${specificMail}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

}