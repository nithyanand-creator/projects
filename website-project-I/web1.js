const defaultstudents = [
    { name: "Asha", marks: 85 },
    { name: "Rahul", marks: 42 },
    { name: "Maya", marks: 91 },
    { name: "Arun", marks: 36 },
    { name: "Priya", marks: 74}
];

const savedstudents = localStorage.getItem("students")
const students = savedstudents? JSON.parse(savedstudents) : defaultstudents;
class Student{
    constructor(name, marks)
    {
        this.name = name;
        this.marks = marks;
    }
    introduce()
    {
        console.log(`I am ${this.name}, I secured ${this.marks} marks.`)
    }
    result()
    {
        console.log(`${this.name}'s result: ${this.marks >= 40 ? "Pass" : "Fail"}`)
    }
    topper()
    {
        console.log(`${this.name} is the topper of the class and secured ${this.marks} marks.`);
    }
    getGrade()
    {
        if (this.marks >= 90) return "A";
        else if (this.marks >= 75) return "B";
        else if (this.marks >= 60) return "C";
        else if (this.marks >= 40) return "D";
        else return "Fail";
    }
};
let highest = students.reduce((max, current) => {
    return current.marks>max.marks ? current : max;
}, students[0]);
const sum = students.reduce((initial, total) => {return (initial + total.marks)}, 0)
const avg = sum/students.length;

const passed = students.filter(student => student.marks >= 40);

const totalstudents = document.getElementById("total-students");
const classaverage = document.getElementById("class-average");
const topper = document.getElementById("topper");
const table = document.getElementById("student-table");

function renderDashboard() {
    const total = students.length;

    const sum = students.reduce((total, student) => {
        return total + student.marks;
    }, 0);

    const average = total > 0 ? sum / total : 0;

    const highest = students.reduce((max, current) => {
        return current.marks > max.marks ? current : max;
    }, students[0]);

    totalstudents.textContent = total;
    classaverage.textContent = average.toFixed(1);
    topper.textContent = highest ? highest.name : "Not available";

    table.innerHTML = "";

    students.forEach((data, index) => {
        const student = new Student(data.name, data.marks);
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${student.name}</td>
            <td>${student.marks}</td>
            <td>${student.getGrade()}</td>
            <td>${student.marks >= 40 ? "Pass" : "Fail"}</td>
            <td><button class="delete-btn">Delete</button></td>
        `;
        row.querySelector(".delete-btn").addEventListener("click", () => {
            students.splice(index, 1);
            localStorage.setItem("students", JSON.stringify(students))
            renderDashboard()
        });

        table.appendChild(row);
    });
}

renderDashboard();
const studentForm = document.getElementById("student-form");
const nameInput = document.getElementById("student-name");
const marksInput = document.getElementById("student-marks");

studentForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const name = nameInput.value.trim();
    const marks = Number(marksInput.value);

    if (name === "" || marksInput.value === "" ||
        marks < 0 || marks > 100) {
        alert("Please enter a name and marks between 0 and 100.");
        return;
    }

    students.push({ name: name, marks: marks });
    localStorage.setItem("students", JSON.stringify(students))
    renderDashboard();

    studentForm.reset();
});
