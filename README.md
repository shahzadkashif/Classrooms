Have you ever wondered how we manage a class full of noobs? Well, all your questions will be answered today!

Classrooms is a noob management project that allows you to manage all of your noobs!

Start by creating a virtual environment. Fork and Clone the project from here.

You’ll get a Django project with an app that has the following created for you:

a Model called Classroom
CRUD for the model
Start by creating a separate file for the navbar, then include it in the base file using an include tag.

Create a signup, signin and signout views using Django User Model. The url names for these views have to be signup, signin, and signout respectively. Make sure to add buttons to these views in the Navbar.

When no one is logged in, the signin and signup buttons will be shown on the Navbar. Then, when the user logs in, his/her name and the signout button will appear on the Navbar.

Next, add a new field to the Classroom model called teacher, which is a Foreign Key to the User model. This field must automatically save the logged in user to the classroom when he/she creates a new one.

Keep in mind that only a signed in user is allowed to create a new classroom. If you try to create a new classroom without signing, in it will redirect you to the signin page.

After that, create a new model called Student that has the following fields:

name
date_of_birth
gender: a CharField with choices
exam_grade
classroom: Foreignkey to the Classroom model
In the Classroom Detail page, create an Add Student button. Whenever a new student is added, the classroom should be assigned automatically to the student object.

Then, create a table under the Classroom’s details. Inside the table, the students with all their details must be listed in an Alphabetical Order by name then by the exam grade.

Add Update and Delete buttons for every student, and remember that only the classroom’s teacher is allowed to Create, Update and Delete a Student from this classroom. Keep in mind that the Create, Update and Delete buttons will only be visible to the classroom’s teacher. Also, make sure that the url names for these actions are as follows student-create, student-update, student-delete.

Note: At any point during this mini project if the classroom or student id is being sent through the url as a parameter call it classroom_id and student_id respectively.
