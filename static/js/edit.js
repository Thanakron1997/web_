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
                <input type="text" name="nextvisit" required  oninvalid="this.setCustomValidity('If there is no study visit, enter NoVisit. Otherwise, enter the next study visit as Extra visit')" oninput="this.setCustomValidity('')">
            </div>
            <div class="col-sm-2">
            <label>Next Visit Date:</label>
            <input type="date" name="nextvisitDate">
            </div>
            <div class="col-sm-2">
                <label>Notes:</label>
                <input type="text" name="notes">
            </div>
            <div class="col-sm-2 divbtnDel">
                <button onclick="removeField(this)" class="btnDel"><i class="material-icons iconDel">delete</i> Delete </button>
            </div>
        </div>
    `;
    
    inputFields.appendChild(newEntry);
}

function removeField(button) {
    event.preventDefault(); // Prevents page refresh or redirection
    if (confirm("Are you sure you want to delete this visit entry?")) {
        button.closest('.user-entry').remove();
    }
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
            <div class="col-sm-2 divbtnDel">
                <button onclick="removeField(this)" class="btnDel"><i class="material-icons iconDel">delete</i> Delete </button>
            </div>
        </div>
    `;
    phoneCall.appendChild(newTC);
}