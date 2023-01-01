var unit = document.getElementById("selected_unit");
var new_unit_field = document.getElementById("new_unit_box");

unit.addEventListener("change", function() {
  if (unit.value == "new") {

    var new_unit = document.createElement("input");
    

    new_unit.setAttribute("type", "text");
    new_unit.setAttribute("autocomplete", "off");
    new_unit.classList.add("create-box", "form-control");
    new_unit.setAttribute("name", "new_unit");

    new_unit_field.innerHTML = "<label>Nouvelle Unité:</label>"
    new_unit_field.appendChild(new_unit);
  }
  else {
    new_unit_field.innerHTML = "";
  }


});
