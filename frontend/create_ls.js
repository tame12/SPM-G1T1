$(function () {
    //navbar
    $("#navigation").load("navbar.html");

    //display role
    var role_name = localStorage.getItem("role_name");
    var role_id = localStorage.getItem("role_ID");
    localStorage.setItem("rolesSelected", JSON.stringify([]));
    console.log(role_name, role_id);

    axios
        .get("http://localhost:456/role/search/" + role_name)
        .then(function (response) {
            console.log(response.data.data[0]);

            if (response.data.code == "201") { //success
                $("#role-selected").text(role_name);
                $("#role-desc").text(response.data.data[0].Role_Desc);

                // nested axios - get skills

            }
        })
        .catch(function (error) {
            console.log(error);
        })

    axios
        .get("http://localhost:456/role/assigned_skill/" + role_id)
        .then(function (response) {
            console.log(response.data.data);

            skills = response.data.data;

            if (response.data.code == "201") { //success
                //populate skills

                const urls = []
                for (skill of skills) {
                    // console.log(skill);
                    urls.push(skill.Skill_ID)
                }
                const promises = urls.map(url => axios.get("http://localhost:456/skill/get_assigned_courses_by_ID/" + url));
                Promise.all(promises).then(get_courses => {
                    // courses = response[0].data.message[0].courses
                    // console.log(courses)
                    skill_html = '';

                    for (i = 0; i < skills.length; i++) {
                        skill = skills[i]
                        console.log(skill)
                        courses = get_courses[i].data.message[0].courses
                        course_html = ''

                      
                        for (course of courses) {
                            // original
                            //course_html += `<div class=" border-box px-4 py-2 bg-grey border border-0" text-black data-id='${course.Course_ID}'>${course.Course_Name}</div>`

                            course_html += `<div> <button onclick="courseButtonSelected('${skill.Skill_ID.toString()} ${course.Course_ID.toString()}')" style="background-color:#E8E8E8; border-radius: 8px; border: 1px solid; margin: 4px 2px; font-size: 17px;" data-id='${course.Course_ID}' id='${skill.Skill_ID} ${course.Course_ID}'>${course.Course_ID}: ${course.Course_Name}</button> </div>`
                        }



                        console.log(course_html)
                        // console.log(skill);

                        skill_html +=
                            `<div class="accordion-item border-box">
                                <h2 class="accordion-header" id="${skill.Skill_ID}">
                                    <button class="accordion-button gradient-box text-black m-0 border border-0" type="button"
                                        data-bs-toggle="collapse" data-bs-target="#skill${skill.Skill_ID}" aria-expanded="true">
                                        ${skill.Skill_Name}
                                    </button>
                                </h2>
                                <div id="skill${skill.Skill_ID}" class="accordion-collapse collapse">
                                    <!-- courses - to be populated by js -->
                                    <div class="accordion-body d-flex flex-wrap gap-3">
                                        ${course_html}
                                    </div>
                                </div>
                            </div>`;
                    }
                    $('#accordionPanelsStayOpenExample').html(skill_html);
                });
            }
        })
});


// turns the course button blue when selected and black when deselected, and updates local storage if the 
function courseButtonSelected(id) {
    console.log("course_ID: ", id)
    courseButton = document.getElementById(id)

    var rolesSelectedStorage = JSON.parse(localStorage.getItem("rolesSelected"));
    
    console.log("updatedSelectedRoles: ", rolesSelectedStorage)
    if (rolesSelectedStorage.includes(id)) {
        console.log("id is in rolesSelectedStorage")
        courseButton.style.borderColor = "black"
        courseButton.style.color = "black"
        // if the course button is selected, deselect it
        rolesSelectedStorage = rolesSelectedStorage.filter(e => e !== id);
    }

    else {
        console.log("id is NOT in rolesSelectedStorage")
        courseButton.style.borderColor = "blue"
        courseButton.style.borderWidth = "2px"
        courseButton.style.color = "blue"
        // if the course button is not selected, select it
        rolesSelectedStorage.push(id)
        
    }
    localStorage.setItem("rolesSelected", JSON.stringify(rolesSelectedStorage));
    console.log("rolesSelected before click: ", rolesSelectedStorage);
}

function createLearningJourney(){
    var rolesSelectedStorage = JSON.parse(localStorage.getItem("rolesSelected"));
    if(rolesSelectedStorage.length == 0){
        alert("Please select at least one course")
    }
    else{
        console.log("can assign")
    }
}

