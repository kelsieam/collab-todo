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
  let loginFormData = new FormData(document.getElementById("login-form"));
  fetch("/login", {
    method: "POST",
    body: loginFormData,
  })
    .then((response) => response.json())
    .then((responseJson) => {
      console.log(responseJson);
    });
});


createGroupSubmit.addEventListener("click", function (evt) {
  evt.preventDefault();
  let createGroupFormData = new FormData(
    document.getElementById("create-group-form")
  );
  fetch("/create-group", {
    method: "POST",
    body: createGroupFormData,
  }).then((response) => {
    // const group = response.json().group
    // const success = response.json().success

    const { group, success } = response.json().data; // getResponseData(response)
    addGroupToList(group);

    console.log(group);
  });
});


joinGroupSubmit.addEventListener("click", function (evt) {
  evt.preventDefault();
  let joinGroupFormData = new FormData(
    document.getElementById("join-group-form")
  );
  fetch("/join-group", {
    method: "POST",
    body: joinGroupFormData,
  })
    .then((response) => {
      return response.json();
    })
    .then((responseJson) => {
      console.log(responseJson);
    });
});


taskSubmit.addEventListener("click", function (evt) {
  // evt.preventDefault();
});


function activateGroup(group) {
  tasksContainer.innerHTML = "";

  // deselect
  const prevSelected = groupsList.getElementsByClassName("selected");
  if (prevSelected) {
    prevSelected.classList.remove("selected"); //
    prevSelected.style.color = "black";
  }

  // select
  group.setAttribute('class', 'selected'); //
  group.style.color = "red";
}


function addGroupToList(group) {
  console.log(group.name);

  const groupButton = document.createElement("button");
  groupButton.innerHTML = group.name;

  groupButton.addEventListener("click", function (evt) {
    evt.preventDefault();

    activateGroup(group);

    // getGroupData(id)
    // const currentGroupUrl = ;
    fetch(`/current-group/${group.group_id}`)
    //   .then((res) => res.json())
      .then((res) => {
        const groupTasks = res.json()
        // console.log(groupTasks);
        groupTasks.forEach((task) => {
          tasksContainer.innerHTML += task.content;
        });
      });
  });

  groupsList.appendChild(groupButton);
}


function displayUserGroups() {
  fetch("/groups")
    .then((response) => response.json())
    .then((res) => {
      groupsList.innerHTML = "";
      // let selectedGroup = null;

      // const userGroups = res.json().data.groups;
      console.log(res.data)
      const { groups } = res.data;
      groups.forEach((x) => addGroupToList(x));

    // console.log(groups);
    // groups.forEach((group) => addGroupToList(group));
  });
}

displayUserGroups();

