document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector("#new-post-form")) {
    document.querySelector("#new-post-form").onsubmit = createPost;
  }
  if (document.querySelector("#profile")) {
    document.querySelector("#profile").addEventListener("click", () => {
      get_self();
    });
  }
  if (document.querySelector("#following")) {
    document.querySelector("#following").addEventListener("click", () => {
      followingPosts();
    });
  }
  getPosts(1);
});

const getPosts = (page) => {
  fetch(`/posts?page=${page}`)
    .then((response) => response.json())
    .then((data) => {
      load_posts(data);
    });
};

const load_posts = (data) => {
  const { posts, page, current_user, liked } = data;
  const postContainer = document.querySelector(".all-posts");
  postContainer.innerHTML = "";
  const allPostContainer = document.createElement("div");
  postContainer.style.display = "block";
  document.querySelector(".user-container").style.display = "none";
  allPostContainer.classList = "posts";
  posts.forEach((post) => {
    const { user, text, timestamp, likes, user_id, id } = post;
    const item = document.createElement("div");
    item.setAttribute("id", `post-${id}`);
    const person = document.createElement("button");
    const time = document.createElement("p");
    const message = document.createElement("p");
    const likeCounter = document.createElement("div");
    likeCounter.classList = "heart";
    const editButton = document.createElement("button");
    editButton.classList = "edit";
    editButton.innerText = "Edit";
    editButton.addEventListener("click", () => {
      edit(id);
    });

    person.setAttribute("class", "btn btn-link");
    person.addEventListener("click", () => {
      get_user(user_id);
    });
    person.innerText = user;
    message.innerText = text;
    time.innerText = timestamp;
    likeCounter.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 4.248c-3.148-5.402-12-3.825-12 2.944 0 4.661 5.571 9.427 12 15.808 6.43-6.381 12-11.147 12-15.808 0-6.792-8.875-8.306-12-2.944z"/></svg>
    <p>${likes}</p>`;
    likeCounter.style.fill = "white";
    likeCounter.style.stroke = "black";
    if (liked.includes(id)) {
      likeCounter.style.fill = "red";
    }
    likeCounter.addEventListener("click", () => {
      like(id);
    });
    if (user_id == current_user) {
      item.append(person, message, likeCounter, editButton, time);
    } else {
      item.append(person, message, likeCounter, time);
    }
    allPostContainer.appendChild(item);
  });
  const pagination = document.createElement("ul");
  pagination.classList = "pagination";
  const prevUpper = document.createElement("li");
  prevUpper.classList = "page-item";
  const prev = document.createElement("button");
  prev.classList = "page-link";
  prev.setAttribute("aria-label", "Previous");
  prev.innerHTML = "<span aria-hidden='true'>&laquo;</span>";
  if (page["has_prev"]) {
    prev.addEventListener("click", () => {
      getPosts(page["current"] - 1);
    });
  } else {
    prev.disabled = true;
  }
  prevUpper.appendChild(prev);
  pagination.appendChild(prev);
  for (i = 1; i <= page["num_pages"]; i++) {
    const list = document.createElement("li");
    list.classList = "page-item";
    const page = document.createElement("button");
    page.classList = "page-link";
    page.innerText = i;
    page.setAttribute("id", i);
    page.addEventListener("click", () => {
      getPosts(page.id);
    });
    list.appendChild(page);
    pagination.appendChild(list);
  }
  const nextUpper = document.createElement("li");
  nextUpper.classList = "page-item";
  const next = document.createElement("button");
  next.classList = "page-link";
  next.setAttribute("aria-label", "Next");
  next.innerHTML = "<span aria-hidden='true'>&raquo;</span>";
  if (page["has_next"]) {
    next.addEventListener("click", () => {
      getPosts(page["current"] + 1);
    });
  } else {
    next.disabled = true;
  }
  nextUpper.appendChild(next);
  pagination.appendChild(next);
  postContainer.append(allPostContainer, pagination);
};

const createPost = () => {
  let text = document.querySelector("#new-post").value;
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/create", {
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
    body: JSON.stringify({
      text: text,
    }),
  })
    .then((response) => response.json())
    .then(() => {
      document.querySelector("#new-post").value = "";
      location.reload();
      getPosts(1);
    })
    .catch((error) => console.log(error));
  return false;
};

const follow_user = (id) => {
  fetch(`/follow/${id}`)
    .then(() => {
      location.reload();
    })
    .catch((error) => console.log(error));
};

const get_user = (id) => {
  document.querySelector(".user-container").style.display = "block";
  document.querySelector(".post-container").style.display = "none";
  fetch(`/user/${id}`)
    .then((response) => response.json())
    .then((profile) => {
      const {
        follower_count,
        following_count,
        user,
        posts,
        followers,
        following,
        following_status,
        liked,
      } = profile;
      const container = document.querySelector(".user-container");
      const name = document.createElement("h3");
      const follow = document.createElement("button");
      const followContainer = document.createElement("div");
      const followingContainer = document.createElement("div");
      const followerContainer = document.createElement("div");
      const userPosts = document.createElement("div");
      posts.forEach((post) => {
        const { user, text, timestamp, likes } = post;
        const item = document.createElement("div");
        const person = document.createElement("h5");
        const time = document.createElement("p");
        const message = document.createElement("p");
        const likeCounter = document.createElement("div");
        likeCounter.classList = "heart";
        person.innerText = user;
        message.innerText = text;
        time.innerText = timestamp;
        likeCounter.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 4.248c-3.148-5.402-12-3.825-12 2.944 0 4.661 5.571 9.427 12 15.808 6.43-6.381 12-11.147 12-15.808 0-6.792-8.875-8.306-12-2.944z"/></svg>
        <p>${likes}</p>`;
        likeCounter.style.fill = "white";
        likeCounter.style.stroke = "black";
        if (liked.includes(id)) {
          likeCounter.style.fill = "red";
        }
        item.append(person, message, likeCounter, time);
        userPosts.appendChild(item);
      });
      followContainer.style.display = "flex";
      followingContainer.innerHTML = `<button class="btn btn-link">${following_count}<p>Following</p></button>`;
      followerContainer.innerHTML = `<button class="btn btn-link">${follower_count}<p>Follower</p> </button>`;
      followerContainer.addEventListener("click", () => {
        container.innerHTML = "";
        const followerUsers = document.createElement("div");
        followers.forEach((follower) => {
          const individual = document.createElement("button");
          individual.classList = "btn btn-link";
          individual.innerText = follower;
          followerUsers.append(individual);
        });
        container.append(followerUsers);
      });
      followingContainer.addEventListener("click", () => {
        container.innerHTML = "";
        const followingUsers = document.createElement("div");
        following.forEach((follow) => {
          const individual = document.createElement("button");
          individual.classList = "btn btn-link";
          individual.innerText = follow;
          followingUsers.append(individual);
        });
        container.append(followingUsers);
      });
      name.innerText = user;
      if (following_status) {
        follow.innerText = "Unfollow";
      } else {
        follow.innerText = "Follow";
      }
      follow.classList = "btn btn-link";
      follow.addEventListener("click", () => {
        follow_user(id);
      });
      followContainer.append(followerContainer, followingContainer);
      container.append(name, follow, followContainer, userPosts);
    })
    .catch((error) => console.log(error));
};

const get_self = () => {
  if (document.querySelector(".user-container").innerHTML.trim() == "") {
    fetch("/profile")
      .then((response) => response.json())
      .then((profile) => {
        const { id } = profile;
        get_user(id);
      });
  }
};

const followingPosts = () => {
  const postContainer = document.querySelector(".post-container");
  postContainer.style.display = "block";
  postContainer.childNodes[1].innerHTML = "<h1>Following Posts</h1>";
  postContainer.childNodes[3].innerHTML = "";
  document.querySelector(".user-container").style.display = "none";
  fetch("following/posts")
    .then((response) => response.json())
    .then((posts) => {
      posts.forEach((post) => {
        const { user, text, timestamp, likes, user_id } = post;
        const postContainer = document.querySelector(".post-container");
        const item = document.createElement("div");
        const person = document.createElement("button");
        const time = document.createElement("p");
        const message = document.createElement("p");
        const likeCounter = document.createElement("div");
        likeCounter.classList = "heart";
        person.setAttribute("class", "btn btn-link");
        person.addEventListener("click", () => {
          get_user(user_id);
        });
        person.innerText = user;
        message.innerText = text;
        time.innerText = timestamp;
        likeCounter.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 4.248c-3.148-5.402-12-3.825-12 2.944 0 4.661 5.571 9.427 12 15.808 6.43-6.381 12-11.147 12-15.808 0-6.792-8.875-8.306-12-2.944z"/></svg>
        <p>${likes}</p>`;
        likeCounter.style.fill = "white";
        likeCounter.style.stroke = "black";
        item.append(person, message, likeCounter, time);
        postContainer.appendChild(item);
      });
    })
    .catch((error) => console.log(error));
};

const edit = (id) => {
  fetch(`/edit/${id}`)
    .then((response) => response.json())
    .then((post) => {
      const { text } = post;
      const container = document.querySelector(`#post-${id}`);
      container.innerHTML = "";
      const formGroup = document.createElement("div");
      formGroup.classList = "form-group";
      const formContainer = document.createElement("form");
      const label = document.createElement("label");
      label.setAttribute("for", "edit");
      label.value = "Edit Post";
      const textInput = document.createElement("textarea");
      textInput.setAttribute("name", "edit");
      textInput.setAttribute("col", "40");
      textInput.setAttribute("row", "3");
      textInput.setAttribute("id", "edit-post");
      const submitBtn = document.createElement("input");
      submitBtn.classList = "btn btn-primary";
      submitBtn.setAttribute("type", "submit");
      submitBtn.addEventListener("click", () => {
        update(id);
      });
      textInput.value = text;
      formContainer.append(textInput, submitBtn);
      formGroup.append(label, formContainer);
      container.append(formGroup);
    });
};

const update = (id) => {
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const text = document.querySelector("#edit-post").value;
  fetch(`/update/${id}`, {
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
    body: JSON.stringify({
      text: text,
    }),
  }).then((response) => getPosts(1));
};

const like = (id) => {
  fetch(`/like/${id}`)
    .then((response) => response.json())
    .then((post) => getPosts(1));
};
