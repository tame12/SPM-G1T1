
// load navbar & populate skills
$(function () {
    $("#navigation").load("navbar.html");
    allCookies = document.cookie
    console.log("targetID: ",getCookie("targetID"))

    $("#SkillName").text(getCookie("targetName"))
    getAssignedRoles()
    getAssignedCourses()
    document.cookie = "selected=''"
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function populatePage(targetArr){
    var html = ``
    if (targetArr.length == 0){
        html = `No Roles Assigned Yet`
    }
    cookieAssignedRoles = ``
    for (let i=0 ; i<targetArr.length ; i++){
        cookieAssignedRoles+=`,${targetArr[i].Role_ID}`
        roleID = targetArr[i].Role_ID
        roleName = targetArr[i].Role_Desc
        html += 
        `
        <div id="${targetArr[i].Role_ID}" name="${targetArr[i].Role_Desc}"class="gradient-box d-flex justify-content-between">
            <p class="my-auto">${targetArr[i].Role_Desc}</p>
            <i class="fa fa-trash w3-large pt-1" onclick="selectDelete(roleID , roleName)" data-bs-toggle="modal" data-bs-target="#staticBackdrop"></i>
        </div>
                
        `
    }
    document.cookie = `assignedRoles=${cookieAssignedRoles}`

    $("#SearchResults").html(html)
}

function populatePageCourses(targetArr){
    var html = ``
    if (targetArr.length == 0){
        html = `No Courses Assigned Yet`
    }
    cookieAssignedCourses = ``
    for (let i=0 ; i<targetArr.length ; i++){
        cookieAssignedCourses+=`,${targetArr[i].Course_ID}`
        html += 
        `
        <div id="${targetArr[i].Course_ID}" name="${targetArr[i].Course_Name}"class="gradient-box d-flex justify-content-between">
            <p class="my-auto">${targetArr[i].Course_Name}</p>
        </div>
                
        `
    }
    document.cookie = `assignedCourse=${cookieAssignedCourses}`

    $("#SearchResultsCourses").html(html)
}

function getAssignedRoles(){
    axios.get(
        "http://localhost:456/skill/get_assigned_roles_by_ID/" + getCookie('targetID')
    ).then(function (response){
        var targetArr = response.data.message[0].roles;
        populatePage(targetArr)
    })
}

function getAssignedCourses(){
    axios.get(
        "http://localhost:456/skill/get_assigned_courses_by_ID/" + getCookie('targetID')
    ).then(function (response){
        var targetArr = response.data.message[0].courses;
        // console.log("targetArr: ",targetArr)
        populatePageCourses(targetArr)
    })
}

function populateModal(){
    let assignedRoles = getCookie("assignedRoles").split(",")
    axios.get(
        "http://localhost:456/role"
    ).then(function (response){
        var targetArr = response.data.data
        html = ``
        if (targetArr.length == 0){
            html+=`No available roles yet. Please activate a role, or add a role`
        }
        for (let i=0; i<targetArr.length; i++){
            if (targetArr[i].Role_Is_Active){
                console.log("assignedRoles:",assignedRoles)
                console.log("targetArr[i].Role_ID: ",typeof targetArr[i].Role_ID)
                if (assignedRoles.includes(String(targetArr[i].Role_ID))){
                // if (targetArr[i].Role_ID in assignedRoles){
                    console.log("already assigned assignedRoles:",assignedRoles)
                    html += `
                    <div class="gradient-box d-flex justify-content-between disabled text-secondary box-secondary" id=${targetArr[i].Role_ID}">
                        <p class="my-auto">${targetArr[i].Role_Desc}</p>
                    </div>
                    `
                } else{
                    html += `
                    <div class="gradient-box d-flex justify-content-between" id=${targetArr[i].Role_ID} onclick="select(this)">
                        <p class="my-auto">${targetArr[i].Role_Desc}</p>
                    </div>
                    `
                }
                
            }
        }
        $("#roleViewer").html(html)
    })
}

function populateCourseModal(){
    let assignedCourses = getCookie("assignedCourse").split(",")
    
    axios.get(
        "http://localhost:456/course"
    ).then(function (response){
        var targetArr = response.data.data
        html = ``
        if (targetArr.length == 0){
            html+=`No available courses yet. Please activate a course, or add a course`
        }
        for (let i=0; i<targetArr.length; i++){
            if (targetArr[i].Course_Is_Active){
                // cannot use: targetArr[i].Course_ID in assignedCourses)
                if (assignedCourses.includes(targetArr[i].Course_ID)){
                    html += `
                    <div class="gradient-box d-flex justify-content-between disabled text-secondary box-secondary" id=${targetArr[i].Course_ID}">
                        <p class="my-auto">${targetArr[i].Course_Name}</p>
                    </div>
                    `
                } else{
                    html += `
                    <div class="gradient-box d-flex justify-content-between" id=${targetArr[i].Course_ID} onclick="select(this)">
                        <p class="my-auto">${targetArr[i].Course_Name}</p>
                    </div>
                    `
                }
                
            }
        }
        $("#courseViewer").html(html)
    })
}

function select(e){
    let assignedRoles = getCookie("assignedRoles").split(",")
    // making sure that you cannot deselect an assigned role
    if (e.classList.contains('selected-box')){
        e.classList.remove('selected-box')
        var list = getCookie('selected').split(',')
        // console.log("e", e.id)
        // console.log("current cookie: ",list)
        var filtered = list.filter(function(value){
            return value != e.id
        })
        // console.log("filtered: ",filtered)
        document.cookie = "selected="+filtered.join(',')
    }
    // When you select an option
    else{
        // If this is the first time that you are selecting something
        e.classList.add('selected-box')
        if (getCookie("selected") == ''){
            document.cookie = "selected="+e.id
        }
        else{
            var list = getCookie('selected')
            list = list.split(",")
            var filtered = list.filter(function(value,index,arr){
                return value != e.id
            })
            document.cookie = "selected="+filtered.join(',')+","+e.id
        }

    }
    console.log("updated cookie", getCookie("selected"))
}

function assignSkillToRole(){
    $("#error_success_bar").html("")
    console.log("hello")
    var selectedRoles = getCookie("selected").split(",")
    var assignedRoles = getCookie("assignedRoles").split(",")
    var toBackEnd = selectedRoles.filter(function(value){
        if (!assignedRoles.includes(value)){
            return parseInt(value)
        }
    })
    var targetID = getCookie('targetID')
    console.log(targetID)
    console.log(toBackEnd)
    axios.post(
    "http://localhost:456/skill/assign_to_role",
    {
        Skill_ID : parseInt(targetID),
        Role_ID : toBackEnd,
    }
    ).then(function(response){
        console.log("response: ",response)
        getAssignedRoles()
        populateModal()
        if(getCookie("selected") != "''"){
            document.cookie = "selected=''"
            $("#error_success_bar").html(`
                <div class="p-4 text-white fw-bold bg-success">${response.data.message}</div>
            `);
        }else{
            alert("No Roles were selected. Please select one or more roles to assign this skill to.")
        }
    })
}

function assignSkillToCourse(){
    $("#error_success_bar").html("")
    console.log("hello, assignSkillToCourse")
    var selectedCourses = getCookie("selected").split(",")
    var assignedCourses = getCookie("assignedCourse").split(",")
    console.log("selectedCourses: ",selectedCourses)
    console.log("assignedCourses", assignedCourses)
    var toBackEnd = selectedCourses.filter(function(value){
        if (!assignedCourses.includes(value) && value != "''"){
            return value
        }
    })
    var targetID = getCookie('targetID')
    console.log("The target ID: ", targetID)
    console.log("the backend: ")
    console.log(toBackEnd)
    axios.post(
    "http://localhost:456/skill/assign_to_courses",
    {
        Skill_ID : parseInt(targetID),
        Course_ID : toBackEnd,
    }
    ).then(function(response){
        console.log("response: ",response)
        getAssignedCourses()
        populateCourseModal()
        console.log("cookie: ",getCookie("selected"))
        if(getCookie("selected") != "''"){
            document.cookie = "selected=''"
            $("#error_success_bar").html(`
                <div class="p-4 text-white fw-bold bg-success">${response.data.message}</div>
            `);
        }else{
            alert("No Courses were selected. Please select one or more courses to assign this skill to.")
        }
        
    })
}

function selectDelete(roleID, roleName){
    skillID = getCookie("targetID")
    skillName = getCookie("targetName")
    console.log(skillID)
    console.log(skillName)
    console.log("1 roleID: ",roleID)
    console.log("1 roleName: ",roleName)
    html = 
    `
        Unassign ${roleName} from ${skillName}?
    `
    $("#modalTitle").html(html)

    html2 = 
    `
        <button  type="button" data-bs-dismiss="modal" class="btn btn-primary" onclick="unassignRoleFromSkill(${roleID})">Unassign</button>
    `
    $("#unassignRoleFromSkill").html(html2)
}

function unassignRoleFromSkill(roleIDToUnassign){
    skillID = getCookie("targetID")
    roleID = getCookie("selected")
    console.log("skillID: ", parseInt(skillID))
    console.log("roleID: ",parseInt(roleIDToUnassign))
    axios.delete(
        "http://localhost:456/skill/unassign_role_from_skill", { data: {
            "Skill_ID" : parseInt(skillID),
            "Role_ID" : parseInt(roleIDToUnassign)
        } }
        
    ).then(function(response){
        console.log(response)
        getAssignedRoles()
        populateModal()
        $("#error_success_bar").html(`
            <div class="p-4 text-white fw-bold bg-success">${response.data.message}</div>
        `);
    }).catch(function(error){
        console.log(error.message)
    })
}