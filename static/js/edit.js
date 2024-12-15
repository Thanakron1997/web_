function addNewfield(){
    const inputFields = document.getElementById('inputFields');
    
    // Create a new user entry
    const newEntry = document.createElement('div');
    newEntry.classList.add('user-entry');
    newEntry.innerHTML = `
        <label>Visit: <input type="text" name="visit" required></label>
        <label>Visit Date: <input type="date" name="visitdate" required></label>
        <label>Next Visit: <input type="date" name="nextvisit" required></label><br>
    `;
    inputFields.appendChild(newEntry);
}
