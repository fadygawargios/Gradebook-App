// Checkboxes
var CC_check = document.getElementById("CC_check");
var MA_check = document.getElementById("MA_check");
var HP_check = document.getElementById("HP_check");
var C_check = document.getElementById("C_check");

// All checked by default
CC_check.checked = true;
MA_check.checked = true;
HP_check.checked = true;
C_check.checked = true;

CC_check.addEventListener("change", compute_grade);
MA_check.addEventListener("change", compute_grade);
HP_check.addEventListener("change", compute_grade);
C_check.addEventListener("change", compute_grade);

// Input fields
var CC = document.getElementById("CC");
var MA = document.getElementById("MA");
var HP = document.getElementById("HP");
var C = document.getElementById("C");

CC.addEventListener("input", compute_grade);
MA.addEventListener("input", compute_grade);
HP.addEventListener("input", compute_grade);
C.addEventListener("input", compute_grade);

function compute_grade() {

    var CC_grade = check_grade(CC.value);
    var MA_grade = check_grade(MA.value);
    var HP_grade = check_grade(HP.value);
    var C_grade = check_grade(C.value);

    var criteria = 4;

    if (CC_check.checked == false) {
        CC_grade = 0;
        criteria--;
    }

    if (MA_check.checked == false) {
        MA_grade = 0;
        criteria--;
    }

    if (HP_check.checked == false) {
        HP_grade = 0;
        criteria--;
    }
    
    if (C_check.checked == false) {
        C_grade = 0;
        criteria--;
    }
    
    var avg = (CC_grade + MA_grade + HP_grade + C_grade) / criteria;
    document.getElementById("grade").innerHTML = avg + "%"; 
}

function check_grade(grade) {

    if (grade == "" || grade < 0) {
        return 0;
    }

    if (grade > 100) {
        return 100;
    }

    return parseInt(grade);
}


const students = document.getElementsByClassName("student_name");
var student_list = [];

for (let i = 0; i < students.length; i++) {
    student_list[i] = students[i].value;
}



next_arrow = document.getElementById("next")
back_arrow = document.getElementById("back")

next_arrow.setAttribute("value", student_list[1]);
back_arrow.setAttribute("value", student_list[student_list.length - 1]);





