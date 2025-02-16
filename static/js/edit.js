function addNewfield(){
    const inputFields = document.getElementById('inputFields');
    
    // Create a new user entry
    const newEntry = document.createElement('div');
    newEntry.classList.add('user-entry');
    newEntry.innerHTML = `
        <div class="row">
            <div class="col-sm-2">
            <label>Visit:</label>
            <input type="text" name="visit" required>
            </div>
            <div class="col-sm-2">
                <label>Visit Date:</label>
                <input type="date" name="visitdate" required>
            </div>
            <div class="col-sm-2">
                <label>Next Visit:</label>
                <input type="text" name="nextvisit" required>
            </div>
            <div class="col-sm-2">
            <label>Next Visit Date:</label>
            <input type="date" name="nextvisitDate">
            </div>
        </div>
    `;
    
    inputFields.appendChild(newEntry);
}

function addNewPhoneCall(){
    const phoneCall = document.getElementById('inputPhoneCall');
    const newTC = document.createElement('div');
    newTC.classList.add('user-entry');
    newTC.innerHTML = `
        <div class="row">
            <div class="col-sm-2">
                <label>Phone Call:</label>
                <input type="text" name="PhoneCall" required>
            </div>
            <div class="col-sm-2">
                <label>Phone Call Date:</label>
                <input type="date" name="PhoneCallDate" required>
            </div>
        </div>
    `;
    phoneCall.appendChild(newTC);
}