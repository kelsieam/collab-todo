const groupsList = document.getElementById('user-groups-list');
const taskSubmit = document.getElementById('create-task-submit');
const taskHolder = document.getElementById('task-holder');
const createUserSubmit = document.getElementById('create-user-submit');
const createGroupSubmit = document.getElementById('create-group-submit');
const joinGroupSubmit = document.getElementById('join-group-submit');
const loginSubmit = document.getElementById('login-submit');

let activeGroupEntry = null;


createUserSubmit.addEventListener('click', function(evt) {
    evt.preventDefault();
    let createUserFormData = new FormData(document.getElementById('create-user-form'));
    fetch('/users', {
        method: 'POST',
        body: createUserFormData
    })
    .then((response) => {
        return response.json();
    })
    .then((newUserData) => {
        console.log(newUserData);
    })
})


loginSubmit.addEventListener('click', function(evt) {
    evt.preventDefault();
    let loginFormData = new FormData(document.getElementById('login-form'));
    fetch ('/login', {
        method: 'POST',
        body: loginFormData
    })
    .then((response) => {
        return response.json();
    })
    .then((responseJson) => {
        console.log(responseJson);
    })
})

createGroupSubmit.addEventListener('click', function(evt) {
    evt.preventDefault();
    let createGroupFormData = new FormData(document.getElementById('create-group-form'));
    fetch ('/create-group', {
        method: 'POST',
        body: createGroupFormData
    })
    .then((response) => {
        return response.json();
    })
    .then ((responseJson) => {
        console.log(responseJson);
        displayUserGroups();
    })
})



joinGroupSubmit.addEventListener('click', function(evt) {
    evt.preventDefault();
    let joinGroupFormData = new FormData(document.getElementById('join-group-form'));
    fetch('/join-group', {
        method: 'POST',
        body: joinGroupFormData
    })
    .then((response) => {
        return response.json();
    })
    .then((responseJson) => {
        console.log(responseJson);
    })
})

taskSubmit.addEventListener('click', function(evt) {
    // evt.preventDefault();
    
})

displayUserGroups()

function displayUserGroups() {
    fetch('/groups')
    .then((response) => {
        return response.json();
    })
    .then((userGroups) => {
        console.log(userGroups);
        userGroups.forEach(group => {
            console.log(group.name);
            const groupEntry = document.createElement('button');
            groupEntry.innerHTML = group.name;
            groupEntry.addEventListener('click', function(evt) {
                evt.preventDefault();
                if (activeGroupEntry) {
                    activeGroupEntry.style.color = 'black';
                }
                groupEntry.style.color = 'red';
                activeGroupEntry = groupEntry;
                taskHolder.innerHTML = ''

                const url = `/current-group/${group.group_id}`
                fetch(url)
                .then ((response) => {
                    return response.json();
                })
                .then ((groupTasks) => {
                    console.log(groupTasks);
                    groupTasks.forEach(task => {
                        taskHolder.innerHTML += task.content;
                    })
                })
            })
            groupsList.appendChild(groupEntry);
        })

    })
}
