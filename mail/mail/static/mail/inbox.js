document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views

  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", () => {
    compose_email();
  });
  document.querySelector("#compose-form").onsubmit = send_email;

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#selected-view").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
      emails.forEach((email) => {
        const { sender, subject, timestamp, read, id } = email;
        const main = document.querySelector("#emails-view");
        const container = document.createElement("div");
        container.setAttribute("id", id);
        container.setAttribute("class", "email-wrapper");
        const name = document.createElement("p");
        const subject_line = document.createElement("p");
        const time = document.createElement("p");
        time.innerText = timestamp;
        name.innerText = sender;
        subject_line.innerText = subject;
        if (read) {
          container.style.backgroundColor = "gray";
        }
        container.append(name, subject_line, time);
        main.appendChild(container);
        container.addEventListener("click", () => get_email(id));
      });
    });
}

function send_email() {
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  // Send email to API for it to send
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then(() => {
      // Redirect to sent mailbox
      load_mailbox("sent");
    })
    .catch((error) => console.log(error));
  return false;
}

const get_email = (id) => {
  const view = document.querySelector("#selected-view");
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  view.style.display = "block";

  fetch(`emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({ read: true }),
  });

  fetch(`emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      const { sender, body, subject, recipients, timestamp, archived } = email;
      const container = document.createElement("div");
      const send = document.createElement("p");
      const content = document.createElement("p");
      const subject_line = document.createElement("p");
      const receiver = document.createElement("p");
      const time = document.createElement("p");
      const archiveBtn = document.createElement("button");
      const reply = document.createElement("button");
      send.innerText = `From: ${sender}`;
      content.innerText = body;
      subject_line.innerText = `Subject: ${subject}`;
      receiver.innerText = "To: ";
      time.innerText = `Time: ${timestamp}`;
      for (i = 0; i < recipients.length; i++) {
        receiver.innerText += recipients[i];
      }
      if (archived) {
        archiveBtn.innerText = "Unarchive";
      } else {
        archiveBtn.innerText = "Archive";
      }
      archiveBtn.classList = "btn btn-sm btn-outline-primary";
      archiveBtn.addEventListener("click", () => {
        fetch(`emails/${id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: !archived,
          }),
        });
      });
      reply.innerText = "Reply";
      reply.addEventListener("click", () => replyEmail(id));
      reply.classList = "btn btn-sm btn-outline-primary";
      container.append(
        send,
        receiver,
        subject_line,
        time,
        archiveBtn,
        reply,
        content
      );
      view.appendChild(container);
    });
};

const replyEmail = (id) => {
  const compose = document.querySelector("#compose-view");
  compose.style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#selected-view").style.display = "none";

  fetch(`emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      const { subject, body, sender, timestamp } = email;
      const to = document.querySelector("#compose-recipients");
      const subject_line = document.querySelector("#compose-subject");
      const message = document.querySelector("#compose-body");

      to.value = sender;
      if (subject.startsWith("Re:")) {
        subject_line.value = subject;
      } else {
        subject_line.value = `Re: ${subject}`;
      }
      message.value = `On ${timestamp}, ${sender} wrote: ${body}`;
    });
};
