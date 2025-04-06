// ! SOCKET
const socket = io();

// ! SEARCH-FOR-ATTENDEE (emit)
let sfa_btn = document.querySelector("#sfa-btn");
sfa_btn.addEventListener('click', () => {
    let sfa_inp = document.querySelector("#sfa-inp");
    socket.emit('sfa', sfa_inp.value);
})

// ! SEARHC-FOR-ATTENDEE (lister)
socket.on('sfa-out', (data) => {
    document.querySelector("#sfa-out-id").innerHTML = data[0];
    document.querySelector("#sfa-out-name").innerHTML = data[1];
    document.querySelector("#sfa-out-role").innerHTML = data[2];
    document.querySelector("#sfa-out-email").innerHTML = data[3];
    document.querySelector("#sfa-out-mobile").innerHTML = data[4];
    document.querySelector("#sfa-out-edit").style.display = "inline";
    document.querySelector("#sfa-out-delete").style.display = "inline";

    document.querySelector("edit-id").value = data[0];
    document.querySelector("edit-name").value = data[1];
    document.querySelector("edit-role").value = data[2];
    document.querySelector("edit-email").value = data[3];
    document.querySelector("edit-mobile").value = data[4];
})

// ! FILTER-ATTENDEE (emit)
let aa_btn = document.querySelector("#aa-btn");
aa_btn.addEventListener('click', () => {
    let aa_inp = document.querySelector("#aa-inp");
    socket.emit('aa', aa_inp.value);
    document.querySelector("#aa-all").style.display = "none";
})

// ! FILTER-ATTENDEE (listen)
socket.on('aa-out', (data) => {
    const container = document.getElementById('aa-src');
    container.innerHTML = ''; // Clear previous results
    
    if (data === "No Attendees Found!") {
        container.innerHTML = '<p>No attendees found</p>';
        return;
    }

    data.forEach(attendee => {
        // Create the UL element with required classes and style
        const ul = document.createElement('ul');
        ul.className = 'links flex gap-10';
        ul.style.fontSize = '12px';
        
        // Create LI elements for name and role
        const liId = document.createElement('li');
        liId.textContent = attendee[0]; // Id

        const liName = document.createElement('li');
        liName.textContent = attendee[1]; // Name
        
        const liRole = document.createElement('li');
        liRole.textContent = attendee[2]; // Role
        
        // Append LIs to UL
        ul.appendChild(liId);
        ul.appendChild(liName);
        ul.appendChild(liRole);
        
        // Append UL to container
        container.appendChild(ul);
    });
});

// ! DELETE-ATTENDEE (emit)
let del_btn = document.querySelector("#sfa-out-delete");
del_btn.addEventListener('click', () => {
    let id = document.querySelector("#sfa-out-id").innerHTML;
    socket.emit('del', id);
    window.open("/dash", "_self");
})

// ! RESET-DATA (emit)
let reset_btn = document.querySelector("#reset-data");
reset_btn.addEventListener('click', () => {
    document.querySelector("#ask-reset").style.display = "flex";
    document.querySelector("#ask-reset").style.opacity = "1";

    document.querySelector("#reset-no").addEventListener('click', () => {
        document.querySelector("#ask-reset").style.opacity = "0";
        setTimeout(() => {
            document.querySelector("#ask-reset").style.display = "none";
        }, 500);
    });

    document.querySelector("#reset-yes").addEventListener('click', () => {
        socket.emit('reset', true);
        document.querySelector("#ask-reset").style.opacity = "0";
        setTimeout(() => {
            document.querySelector("#ask-reset").style.display = "none";
        }, 500);
        window.open("/dash", "_self");
    });
})

// | Edit Attendee
let edit_btn = document.querySelector("#sfa-out-edit");
edit_btn.addEventListener('click', () => {
    document.querySelector("#edit-id").value = document.querySelector("#sfa-out-id").innerHTML
    document.querySelector("#edit-name").value = document.querySelector("#sfa-out-name").innerHTML
    document.querySelector("#edit-role").value = document.querySelector("#sfa-out-role").innerHTML
    document.querySelector("#edit-email").value = document.querySelector("#sfa-out-email").innerHTML
    document.querySelector("#edit-mobile").value = document.querySelector("#sfa-out-mobile").innerHTML
})

// Frame Buttons
let daily = document.querySelector("#attendance-rec").querySelector("#daily");
let weekly = document.querySelector("#attendance-rec").querySelector("#weekly");
let monthly = document.querySelector("#attendance-rec").querySelector("#monthly");
let all = document.querySelector("#attendance-rec").querySelector("#all");

// Frames
let daily_frame = document.querySelector("#daily_frame");
let weekly_frame = document.querySelector("#weekly_frame");
let monthly_frame = document.querySelector("#monthly_frame");
let all_frame = document.querySelector("#all_frame");

// | Change Frame (daily)
daily.addEventListener('click', () => {
    daily.style.backgroundColor = "var(--secondary)";
    weekly.style.backgroundColor = "var(--hover)";
    monthly.style.backgroundColor = "var(--hover)";
    all.style.backgroundColor = "var(--hover)";

    daily_frame.style.display = "table";
    weekly_frame.style.display = "none";
    monthly_frame.style.display = "none";
    all_frame.style.display = "none";
})

// | Change Frame (weekly)
weekly.addEventListener('click', () => {
    daily.style.backgroundColor = "var(--hover)";
    weekly.style.backgroundColor = "var(--secondary)";
    monthly.style.backgroundColor = "var(--hover)";
    all.style.backgroundColor = "var(--hover)";

    daily_frame.style.display = "none";
    weekly_frame.style.display = "table";
    monthly_frame.style.display = "none";
    all_frame.style.display = "none";
})

// | Change Frame (montly)
monthly.addEventListener('click', () => {
    daily.style.backgroundColor = "var(--hover)";
    weekly.style.backgroundColor = "var(--hover)";
    monthly.style.backgroundColor = "var(--secondary)";
    all.style.backgroundColor = "var(--hover)";

    daily_frame.style.display = "none";
    weekly_frame.style.display = "none";
    monthly_frame.style.display = "table";
    all_frame.style.display = "none";
})

// | Change Frame (all)
all.addEventListener('click', () => {
    daily.style.backgroundColor = "var(--hover)";
    weekly.style.backgroundColor = "var(--hover)";
    monthly.style.backgroundColor = "var(--hover)";
    all.style.backgroundColor = "var(--secondary)";

    daily_frame.style.display = "none";
    weekly_frame.style.display = "none";
    monthly_frame.style.display = "none";
    all_frame.style.display = "table";
})

// | Alert for update
let disabled_btns = document.querySelectorAll(".aside .btns .btn");

disabled_btns.forEach((elem) => {
    elem.addEventListener('click', () => {
        alert("This feature is not released yet!");
    });
});

// | Open Profile
let profile_btn = document.querySelector("#profile");
profile_btn.addEventListener('click', () => {
    document.querySelector('.profile-box').style.display = "grid";
    document.querySelector('.profile').style.display = "flex";
})

// ? GOTO [Search for Attendee]
document.addEventListener('keypress', (key) => {
    if(key.key == "/"){
        setTimeout(() => {
            document.querySelector("#sfa-inp").focus();
        }, 100);
    }
})

document.addEventListener('keydown', (key) => {
    if (key.ctrlKey && key.key == 'q'){
        setTimeout(() => {
            document.querySelector("#sfa-inp").focus();
        }, 100);
    }
})

// ? GOTO [Add new Attendee]
document.addEventListener('keydown', (key) => {
    if(key.ctrlKey && key.altKey && key.key == 'n'){
        setTimeout(() => {
            document.querySelector("#new-att").focus();
        }, 100);
    }
})

// ? GOTO [Filter Attendess]
document.addEventListener('keydown', (key) => {
    if(key.ctrlKey && key.altKey && key.key == 'f'){
        setTimeout(() => {
            document.querySelector("#aa-inp").focus();
        }, 100);
    }
})

// ! CLOSe BROWSER LOGGING
console.error = function() {};  
console.warn = function() {};   
console.log = function() {};    