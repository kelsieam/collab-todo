const groupsList = document.getElementById('user-groups-list');
const taskSubmit = document.getElementById('create-task-submit');
let activeGroupEntry = null;

taskSubmit.addEventListener('click', function(evt) {
    // evt.preventDefault();
    
})
fetch ('/groups')
.then ((response) => {
    return response.json();
})
.then ((userGroups) => {
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
            
            const url = `/current-group/${group.group_id}`
            fetch(url)
            .then ((response) => {
                return response.json();
            })
            .then ((groupTasks) => {
                console.log(groupTasks);
            })
        })
        groupsList.appendChild(groupEntry);
    })

})
