# This is my CS50 Project
# IYK-SANDWICHES WEB CAFE
#### Video Demo:  <URL - https://youtu.be/3c22qLb2d4w>

## PART A
#### Description:
Iyk-sandwiches web café is a web application that simulates sandwich online ordering for a food business. It  allows users who are registered online to Iyk-sandwiches company systems to make orders for their choice sandwiches and sides.
Users have the option of selecting precisely what goes into their plates and can view a summary of the selection of what they hope to enjoy from the restaurant. There are wide selections of bread, fillings and sides to choose from based on their dietary needs, with the cost for each item and the total cost for each order.

The purpose of the application is to help users, and the restaurant streamline the process in product selection, order placement and payment. Once order is placed, it helps the kitchen know what food items they are to prepare ahead of time.
An administrator dashboard displays details of registered users and orders made by customers.

Iyk-sandwiches web application has been implemented to give users a seamless sandwiches ordering platform for the sandwich of their choice and help the business leverage on the opportunities of ecommerce.

##### What is the benefit? 
Users do not have to leave the comfort of their homes when making choices or viewing what is on the menu.
Users can seamlessly place order online and comfortable pick up, seat in or receive their meals on delivery.
The work of the business will be greatly enhanced in organising customers orders.

##### Who would benefit? 
Users seeking to order sandwiches.
Businesses offering food sales online.
Chefs and other food delivery services.

##### What impact it would have?
It provides a time-saving solution for the business to efficiently manage and monitor customer orders.

##### Futher improvement and releases
More futures will be added to this application to improve the user experience and security. Secure payment gateway, email confirmation and dynamic previews will be added in future release. 

## PART B
#### FILE STRUCTURE
This application has a front end, backend logic and database for storing application data.
A flask application (app.py) written in python code has been implemented using the flask framework to control the routes for the application.
Helper functions were included in the application to seamless integration into the route functions for the application. Also, a database with well implemented entity relations was implemented with suitable tables, unique identifier, primary keys and foreign keys.
A customer table was created to store customer credentials. A menu items table was created to store details of menu items. 
A category table for item category was also created and order table.

Two types of users are required access to the application. 
##### Administrator
The administrator manages customer details and orders. The administrator can also upload into the application, view and edit items.

I had to debate the choice of having a seperate design layout for administrative interfaces by creating a layout.html page in an admin folder which had the custom templates for all administrative pages, such as admin dashboard home page (index.html) that shows a list of customers who successful bought items, customer details page (customer.html), and details of all menu items (items.html).

##### Users (Customers)
Customers must register in the application (register.html) and will be refused access to login unless that is done. Once registration is successful, the user can login (login.html) to access products and perform transactions on the products page (products.html) and checkout from the basket page after payment is successful (basket.html). User data is stored in session and generated once user have been successfully authenticated.

Once finished making transaction, the user logs out of the application. As soon as the user logs out of the application, the session is ended for that user and every content of the the basket reverts back to empty.

#### Final thoughts
The application performs and intented and will be improved with more functionality for better user experience and security.




