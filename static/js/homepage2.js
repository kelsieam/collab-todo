
const groupsList = document.getElementById("user-groups-list");
const taskSubmit = document.getElementById("create-task-submit");
const tasksContainer = document.getElementById("task-holder");
const createUserSubmit = document.getElementById("create-user-submit");
const createGroupSubmit = document.getElementById("create-group-submit");
const joinGroupSubmit = document.getElementById("join-group-submit");
const loginSubmit = document.getElementById("login-submit");

createUserSubmit.addEventListener("click", function (evt) {
    evt.preventDefault();
    let createUserFormData = new FormData(
      document.getElementById("create-user-form")
    );
    fetch("/users", {
      method: "POST",
      body: createUserFormData,
    })
      .then((response) => {
        return response.json();
      })
      .then((newUserData) => {
        console.log(newUserData);
      });
  });


loginSubmit.addEventListener("click", function (evt) {
evt.preventDefault();
const loginFormData = new FormData(document.getElementById("login-form"));
fetch("/login", {
    method: "POST",
    body: loginFormData,
})
    .then((response) => response.json())
    .then((responseJson) => {
    console.log(responseJson);
    });
});


createGroupSubmit.addEventListener("click", function(evt) {
    evt.preventDefault();
    const createGroupFormData = new FormData(document.getElementById("create-group-form"));
    fetch("/create-group", {
        method: "POST",
        body: createGroupFormData
    })
        .then((response) => response.json())
        .then((newGroup) => {
            console.log(newGroup);
        })
})
