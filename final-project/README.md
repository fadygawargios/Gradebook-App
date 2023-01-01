# Gestionnaire de Note
#### Video Demo:  https://youtu.be/TnMw7aPmSLs
#### Description:

For my final project, I created a web app using Flask to help the teachers at my french high school digitally keep track of their students' grades. First of all, the teachers sign in and out seamlessly via Google Oauth, using their school google account instead of having to create and remember yet another password. Once signed in, they can create classes, ensuring to provide a class code, a class name, a list of the students enrolled, and a colour that will later be displayed as a sort of banner. From there, they can not only view their classes and students, but go into the class, creating units to house class material that they plan on grading such as projects or quizzes. They can click on the individual task and cycle through students grading them by percentage based on the four criteria (CC, MA HP, C).

All data is stored in a SQL database called "data.db" consisting of five tables: classes -- holding class information such as the class code, name and colour, students -- holding student information in relation to the class they are enrolled in, users -- pertaining to the teacher's information like their name and google id, tasks -- storing units with their respective tasks and finally, grades -- storing the percentage for each criteria in every task in a class (as of now, yet to be implemented). This project also utulizes javascript on several pages to enhance user experience, by for example, creating or deleting table cells, adding input fields when certain options are selected and alerting the user if not all necessary form items are filled before submission.

I truly hope to continue using the extraordinary skills that I have learned throughout this course to not only finish this project in the new year, but to work on many more in the pursuit of my newfound passion in CS! I would like to give one big thank you to everyone who has made this possible, you have made all the difference, and I wish you all the best!

### This Was CS50. 
