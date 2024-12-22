function addNewfield(){
    const inputFields = document.getElementById('inputFields');
    
    // Create a new user entry
    const newEntry = document.createElement('div');
    newEntry.classList.add('user-entry');
    newEntry.innerHTML = `
        <label>Visit: <input type="text" name="visit" required></label>
        <label>Visit Date: <input type="date" name="visitdate" required></label>
        <label>Next Visit: <input type="text" name="nextvisit" required></label>
        <label>Next Visit Date: <input type="date" name="nextvisitDate"></label><br>

    `;
    
    inputFields.appendChild(newEntry);
}

function addNewPhoneCall(){
    const phoneCall = document.getElementById('inputPhoneCall');
    const newTC = document.createElement('div');
    newTC.classList.add('user-entry');
    newTC.innerHTML = `
        <label>Phone Call: <input type="text" name="PhoneCall" required></label>
        <label>Phone Call Date: <input type="date" name="PhoneCallDate" required></label><br>
    `;
    phoneCall.appendChild(newTC);
}