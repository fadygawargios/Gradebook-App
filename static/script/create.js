var table = document.getElementById("student_table");

document.getElementById("add_row").addEventListener("click", insert_row);
document.getElementById("remove_row").addEventListener("click", function() {
  if (table.tBodies[0].rows.length != 0)
  {
    table.deleteRow(-1);
  }
});

function insert_row() {

  var length = table.tBodies[0].rows.length;


  var newRow = table.insertRow(length + 1);
  
  var number_cell = newRow.insertCell(0);
  var name_cell = newRow.insertCell(1);
  var email_cell = newRow.insertCell(2);


  new_number = (length + 1).toString();
  new_number = new_number.concat(".");
  number_cell.innerHTML = new_number;
  number_cell.classList.add("student_number");

  
  var new_name = document.createElement("input");

  new_name.setAttribute("type", "text");
  new_name.setAttribute("autocomplete", "off");
  new_name.classList.add("create-box", "form-control");


  var new_email = document.createElement("input");

  new_email.setAttribute("type", "text");
  new_email.setAttribute("autocomplete", "off");
  new_email.classList.add("create-box", "form-control");

  new_name.setAttribute("name", "name_".concat((length + 1).toString()));
  new_email.setAttribute("name", "email_".concat((length + 1).toString()));

  name_cell.appendChild(new_name);
  email_cell.appendChild(new_email);
}

// Make sure all form fields are filled


function validate() {

  var class_code = document.getElementById("class_code");
  var class_name = document.getElementById("class_name");
  var class_colour = document.getElementById("class_colour");

  if (class_code.value == "") {
    alert("SVP ajoutez le code du cours.");
    return false;
  } 
  
  if (class_name.value == "") {
    alert("SVP nommez votre cours.");
    return false;
  } 
  
  if (class_colour.value == "#FFFFF") {
    alert("SVP choissisez une couleur.");
    return false;
  }

  return true;
}
