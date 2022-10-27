# insert into `is212_G1T1`.`Course` (`Course_ID`, `Course_Name`, `Course_Desc`, `Course_Is_Active`, `Course_Type`, `Course_Category`) values 
# (("IS-1",Course_Name="Information Systems & Innovation",Course_Desc="case aborum.",Course_Is_Active=1,Course_Type="Internal",Course_Category="Technical")
# ("IS-2","Business Process Analysis and Solutioning","modeling, lorem ipsum doloraborum.",1,"External","Technical"
# ("IS-3","Enterprise Solution Management","incident management, problem management, change management, borum.",1,"Internal","Technical"
# ("IS-4","Software Project Management","agile, scrum, waterfall",0,"Internal","Technical"
# (("IS-5",Course_Name="Digital Business - Technology and Transformation",Course_Desc="emerging technologies",Course_Is_Active=1,Course_Type="Internal",Course_Category="Technical")
# (("IS-6",Course_Name="Introduction to Programming",Course_Desc="basic python",Course_Is_Active=1,Course_Type="Internal",Course_Category="Technical")
# ("IS-7","Data Management","mySQL, ERD",0,"Internal","Technical"
# ("IS-8","Interaction Design and Prototyping","Prototyping, product management",1,"Internal","Technical"
# ("IS-9","Web Application Development I","php, html",1,"Internal","Technical"
# ("IS-10","Web Application Development II","css, javascript, bootstrap, vue.js",1,"External","HR"
# ("IS-11","Enterprise Solution Development","Microserivces, API, REST",1,"Internal","Finance");

db.session.add_all([
    Skill(Skill_ID=1, Skill_Name="Basic programming 1", Skill_Is_Active=1),
    Skill(Skill_ID=2, Skill_Name="Basic programming 2", Skill_Is_Active=1),
    Skill(Skill_ID=3, Skill_Name="Intermediate programming 1", Skill_Is_Active=1),
    Skill(Skill_ID=4, Skill_Name="Intermediate programming 2", Skill_Is_Active=1),
    Skill(Skill_ID=5, Skill_Name="Modeling 1", Skill_Is_Active=1),
    Skill(Skill_ID=6, Skill_Name="Agile 1", Skill_Is_Active=1),
    Skill(Skill_ID=7, Skill_Name="Critical thinking 1", Skill_Is_Active=1),
    Skill(Skill_ID=8, Skill_Name="Database 1", Skill_Is_Active=1),
    Skill(Skill_ID=9, Skill_Name="Front end 1", Skill_Is_Active=1),
    Skill(Skill_ID=10, Skill_Name="Business process management 1", Skill_Is_Active=1),
    Skill(Skill_ID=11, Skill_Name="Prototyping 1", Skill_Is_Active=0)
])
db.session.commit()

# delete from `is212_G1T1`.`Staff`;
# insert into `is212_G1T1`.`Staff` (`Staff_ID`, `Staff_FName`, `Staff_LName`, `Dept`, `Email`, `Position_ID`) values 
# (1,"John","Smith","IT","john.smith@gmail.com",1),
# (2,"Jane","Doe","IT","jane.doe@gmail.com",1),
# (3,"Maria","Lee","HR","maria.lee@gmail.com",1),
# (4,"David","Lai","Production","david.lai@gmail.com",2),
# (5,"Ana","Yee","Operations","ana.yee@gmail.com",2),
# (6,"Michael","Teo","Operations","michael.teo@gmail.com",2),
# (7,"Carlos","Tan","Services","carlos.tan@gmail.com",3),
# (8,"James","Yang","Customer Relations","james.yang@gmail.com",3),
# (9,"Sandra","Chua","HR","sandra.chua@gmail.com",3),
# (10,"Sarah","Lim","Accounting","sarah.lim@gmail.com",2),
# (11,"Mark","Chen","Accounting","mark.chen@gmail.com",1);

# delete from `is212_G1T1`.`Role`;
# insert into `is212_G1T1`.`Role` (`Role_ID`, `Role_Name`, `Role_Desc`, `Role_Is_Active`) values 
# (1,"SWE", "Software Engineer", 1),
# (2,"PM", "Project Manager", 1),
# (3,"BA", "Business Analyst", 0);

# delete from `is212_G1T1`.`Registration`;
# insert into `is212_G1T1`.`Registration` (`Reg_ID`, `Course_ID`, `Staff_ID`, `Reg_Status`, `Completion_Status`) values 
# (12345,"IS-1",4,"Registered","Completed"),
# (12346,"IS-1",5,"Registered","Completed");

# delete from `is212_G1T1`.`Course_Skill`;
# insert into `is212_G1T1`.`Course_Skill` (`Course_ID`, `Skill_ID`) values 
# ("IS-1",1),
# ("IS-1",2);

# delete from `is212_G1T1`.`Skill_Role`;
# insert into `is212_G1T1`.`Skill_Role` (`Skill_ID`, `Role_ID`) values 
# (1,1),
# (2,2),
# (2,1);

# delete from `is212_G1T1`.`Learning_Journey`;
# insert into `is212_G1T1`.`Learning_Journey` (`LJ_ID`, `Staff_ID`, `Role_ID`, `LJ_Number`) values 
# (1,1,1,1),
# (2,1,2,2),
# (3,1,3,3),
# (4,4,1,1),
# (5,4,2,2),
# (6,4,3,3);

# delete from `is212_G1T1`.`Learning_Journey_Course`;
# insert into `is212_G1T1`.`Learning_Journey_Course` (`LJ_ID`, `Course_ID`,`Skill_ID`) values 
# (1,"IS-1",1),
# (1,"IS-2",2),
# (2, "IS-3", 3),
# (2, "IS-4", 4),
# (3,"IS-5",5),
# (3,"IS-6",6),
# (4,"IS-1",1),
# (4,"IS-2",2),
# (5, "IS-3", 3),
# (5, "IS-4", 4),
# (6,"IS-5",5);

