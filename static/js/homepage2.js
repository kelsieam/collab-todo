
const groupsList = document.getElementById("user-groups-list");
const taskSubmit = document.getElementById("create-task-submit");
const tasksContainer = document.getElementById("task-holder");
const tasksSection = document.getElementById("create-task-container");
const createUserSubmit = document.getElementById("create-user-submit");
const createGroupSubmit = document.getElementById("create-group-submit");
const joinGroupSubmit = document.getElementById("join-group-submit");
const loginSubmit = document.getElementById("login-submit");
const createTaskContainer = document.getElementById("create-task-container");
const loginSection = document.getElementById("login-div");
const messageHolder = document.getElementById("message-holder");


createUserSubmit.addEventListener("click", function (evt) {
  evt.preventDefault();
  let createUserFormData = new FormData(
    document.getElementById("create-user-form")
  );
  fetch("/users", {
    method: "POST",
    body: createUserFormData,
  })
    .then((response) => response.json())
    .then((newUserData) => {
      console.log("/users", newUserData);
    });
});


loginSubmit.addEventListener("click", function(evt) {
  evt.preventDefault();
  const loginFormData = new FormData(document.getElementById("login-form"));
  fetch("/login", {
    method: "POST",
    body: loginFormData,
  })
    .then((res) => res.json())
    .then((responseJson) => {
    console.log('/login', responseJson);
    if (responseJson.success) {
      loginSection.style.display = 'none';
    }
    messageHolder.innerHTML = responseJson.message;
    });
});


createGroupSubmit.addEventListener("click", function(evt) {
  evt.preventDefault();
  const createGroupFormData = new FormData(document.getElementById("create-group-form"));
  fetch("/create-group", {
    method: "POST",
    body: createGroupFormData
})
    .then((res) => res.json())
    .then((newGroup) => {
      console.log("/create-group", newGroup);
      displayGroup(newGroup.data.group);
      messageHolder.innerHTML = newGroup.message;
    });
});


joinGroupSubmit.addEventListener("click", function(evt) {
  evt.preventDefault();
  const joinGroupFormData = new FormData(document.getElementById("join-group-form"));
  fetch("/join-group", {
      method: "POST",
      body: joinGroupFormData,
  })
      .then((response) => response.json())
      .then((responseJson) => {
      console.log("/join-group", responseJson);
      messageHolder.innerHTML = responseJson.message;
      });
  });


taskSubmit.addEventListener("click", function(evt) {
  evt.preventDefault();
  const createTaskFormData = new FormData(document.getElementById("create-task-form"));
  fetch("/tasks", {
    method: "POST",
    body: createTaskFormData,
  })
    .then((response) => response.json())
    .then((responseJson) => {
      console.log("/tasks", responseJson);
      messageHolder.innerHTML = responseJson.message;
    });
  });


function activateGroup(group) { // sets clicked group as active

  tasksContainer.innerHTML = "";

  // deselect
  const prevSelected = document.getElementById("selected-group");
  if (prevSelected) {
    prevSelected.setAttribute("id", ""); //
    prevSelected.style.color = "black";
  }

  // select
  group.setAttribute('id', 'selected-group'); //
  tasksSection.style.display = "block";
  console.log(tasksSection.style.display);
  group.style.color = "red";

}


function displayGroup(group) { // adds group to group display

  const groupButton = document.createElement("button");
  groupButton.innerHTML = group.name;

  groupButton.addEventListener("click", function (evt) {
    evt.preventDefault();

    activateGroup(groupButton);

    fetch(`/current-group/${group.group_id}`)
      .then((res) => res.json())
      .then((groupTasks) => {
        console.log("/current-group/group-id", groupTasks);
        groupTasks.forEach((task) => {
          console.log("groupTasks.forEach", task.content);
          const taskName = document.createElement("li");
          taskName.innerHTML = task.content;
          tasksContainer.appendChild(taskName);
        });
      });
  });

  groupsList.appendChild(groupButton);
}


addEventListener("DOMContentLoaded", (evt) => {
  fetch('/groups')
    .then((res) => res.json())
    .then((groups) => {
      console.log("/groups", groups);
      groups.data.groups.forEach((group) => displayGroup(group));
    })
})




