function sendCode(){
    if (document.querySelector("#verificationInput") != null) return;

    const formData = new FormData();

    const phoneNumber = document.querySelector("#phoneInput").value;
    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    if (!phoneNumber) return alert("Phone Number must be provided");

    formData.append("csrfmiddlewaretoken", csrf);
    formData.append("phone_number", phoneNumber);

    fetch("/api/login/send-code/", {method:"POST", body: formData})
    .then(response => response.json())
    .then(data => {
        if (data.error) return alert(data.error);
        addVerificationForm();
        const submitButton = document.querySelector("#sendCode");
        submitButton.innerText = "Submit";
        submitButton.setAttribute("onclick", "verificateCode()");
    })
}


function verificateCode(){
    const formData = new FormData();

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const insertedCode = document.querySelector("#verificationInput").value;
    const phoneNumber = document.querySelector("#phoneInput").value;

    if (!insertedCode) return alert("Verification Code must be provided");
    if (!phoneNumber) return alert("Phone Number must be provided");

    formData.append("csrfmiddlewaretoken", csrf);
    formData.append("inserted_code", insertedCode);
    formData.append("phone_number", phoneNumber);

    fetch("/api/login/verify-code/", {method:"POST", body:formData})
    .then(response => response.json())
    .then(data => {
        if (data.error) return alert(data.error);
        addUserDataForm();
        const submitButton = document.querySelector("#sendCode");
        submitButton.setAttribute("onclick", "createNewUser()");
        localStorage.setItem("token", data.token);
    })
}


function createNewUser(){
    formData = new FormData();
    
    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const phoneNumber = document.querySelector("#phoneInput").value;
    const firstName = document.querySelector("#firstNameInput").value;
    const lastName = document.querySelector("#lastNameInput").value;
    const login = document.querySelector("#loginInput").value;
    const password = document.querySelector("#passwordInput").value;
    const token = localStorage.getItem("token");

    const user_data = {
        "phone_number": phoneNumber,
        "first_name": firstName,
        "last_name": lastName,
        "username": login,
        "password": password
    };
      
    for (const key in user_data) {
        if (!user_data[key]) return alert(`${key} must be provided`);
    }

    formData.append("csrfmiddlewaretoken", csrf);
    formData.append("phone_number", phoneNumber);
    formData.append("first_name", firstName);
    formData.append("last_name", lastName);
    formData.append("username", login);
    formData.append("password", password);
    formData.append("token", token);

    fetch("/api/login/add-user/", {method:"POST", body: formData})
    .then(response => {
        if (response.status == 201) {
            window.location.href = '/login';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data.error) return alert(data.error);
    })
}

function verificateUser(){
    formData = new FormData();

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const username = document.querySelector("#loginInput").value;
    const password = document.querySelector("#passwordInput").value;

    if (!username) return alert("Username must be provided");
    if (!password) return alert("Password must be provided");

    formData.append("csrfmiddlewaretoken", csrf);
    formData.append("username", username);
    formData.append("password", password);

    fetch("/api/login/verificate-user/", {method: "POST", body: formData})
    .then(response => response.json())
    .then(data => {
        if (data.error) return alert(data.error);
        if (!("token" in data)) return alert("Token missing");
        localStorage.setItem('token', data.token);
        window.location.href = '/user/' + data.user_id;
    })
}

function applyInviteCode(){
    formData = new FormData;

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const inviteCodeInput = document.querySelector("#inviteCodeInput");
    const userID = document.querySelector("#userID").value;

    if (!inviteCodeInput.value) return alert("Invite code must be provided");

    formData.append("csrfmiddlewaretoken", csrf);
    formData.append("invite_code", inviteCodeInput.value);

    fetch("/api/user/" + userID +"/apply-invite-code/", {method: "POST", body: formData})
    .then(response => response.json())
    .then(data => {
        if (data.error) return alert(data.error);
        const submitButton = document.querySelector("#submitButton");
        submitButton.style.visibility = "hidden";
        inviteCodeInput.disabled = true;
        inviteCodeInput.setAttribute("value", inviteCode.value);
    })
}

function addVerificationForm(){
    const parent = document.querySelector(".verification-container");

    const textDiv = document.createElement("div");
    textDiv.innerText = "Enter code from SMS";

    const verificationCodeInput = document.createElement("input");
    verificationCodeInput.setAttribute("type", "number");
    verificationCodeInput.setAttribute("id", "verificationInput");
    verificationCodeInput.classList.add("form-control");

    parent.appendChild(textDiv);
    parent.appendChild(verificationCodeInput);
}

function addUserDataForm(){
    const parent = document.querySelector(".userdata-container");

    const firstNameDiv = document.createElement("div");
    firstNameDiv.innerText = "First Name";

    const firstNameInput = document.createElement("input");
    firstNameInput.setAttribute("type", "text");
    firstNameInput.setAttribute("id", "firstNameInput");
    firstNameInput.classList.add("form-control");

    const secondNameDiv = document.createElement("div");
    secondNameDiv.innerText = "Second Name";

    const lastNameInput = document.createElement("input");
    lastNameInput.setAttribute("type", "text");
    lastNameInput.setAttribute("id", "lastNameInput");
    lastNameInput.classList.add("form-control");

    const loginDiv = document.createElement("div");
    loginDiv.innerText = "Login";

    const loginInput = document.createElement("input");
    loginInput.setAttribute("type", "text");
    loginInput.setAttribute("id", "loginInput");
    loginInput.classList.add("form-control");

    const passwordDiv = document.createElement("div");
    passwordDiv.innerText = "Password";

    const passwordInput = document.createElement("input");
    passwordInput.setAttribute("type", "text");
    passwordInput.setAttribute("id", "passwordInput");
    passwordInput.classList.add("form-control");

    parent.appendChild(firstNameDiv);
    parent.appendChild(firstNameInput);
    parent.appendChild(secondNameDiv);
    parent.appendChild(lastNameInput);
    parent.appendChild(loginDiv);
    parent.appendChild(loginInput);
    parent.appendChild(passwordDiv);
    parent.appendChild(passwordInput);
}
