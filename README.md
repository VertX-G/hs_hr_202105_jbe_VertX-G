# Humanstate May 2021 Junior Backend Web Developer assignment

The purpose of this assignment is the creation of a login app made of:

- a login page where the user must enter their credentials and
- a "protected page" with information about previous login attempts the user sees when their credentials are valid.

The application user’s information is stored in a database you will find in the `/db` folder of the github repository of this assignment. The database is provided in 2 formats: a ready to use sqlite3 database file and a SQL dump file (in sqlite3 format but easy to convert into another DB engine format).

The database contains a single table:

```sql
CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    password TEXT NOT NULL,
    isadmin INT NOT NULL
);
```

with 3 existing users. The user’s password is encrypted using **SHA256**.

Here are the username / “clear text passwords” it contains:

```
username    password
----------  -------------
admin       riverBlue33
user1       lakeGreen32
user2       seaPurple31
```

## You will need

- A web development environment
- Internet access
- A github (https://github.com/) account (if you don’t have one, you can create one for free)
- This document
- Your demo site ID you received by email to access [https://interviews.humanstate.com/202105_juniorbackend/[demo site ID]](#)

### Setup your repository

Go to the base repository https://github.com/lppoix/hs_hr_202105_juniorbackend_assignment.
- Create your copy of the repository by clicking on the green "Use this template" button.
- Choose "hs_hr_202105_jbe_[your github username]"  as repository name
- Ask for a Private repository, no need to include all branches
- Once you have your own repository, share it back with us for review
    - Go to its « Settings » > « Manage access »
    - Add our github user « lppoix » as collaborator
    
You can now clone your new repository into your development environment and start working.

## Your task

Using the back end language (asp.net, node.js, perl, php, python, ruby...) and database engine (sqlite3 is provided but you can use another one) of your choice:

- Add a table to record existing user login attempts.
- Create a login page asking for username and password.
- Upon unsuccessful login, show the login page again with a message letting the user know about it.
- Upon successful login, show the "protected page" where you’ll
	- greet the user with their 1st and last names,
	- tell them how many unsuccessful login attempts were made since their last login,
	- tell them when the last successful login happened and
	- provide them with a logout link.
- Upon logout, show the login page with a message acknowledging successful logout.
- The "protected page" should not be accessible without providing valid credentials.
- The message on the "protected page" should handle the 1st successful login special case properly.

This is a back end assignment, **no need to spend time on presentation**, crude HTML (as you can see on the example @ [https://interviews.humanstate.com/202105_juniorbackend/[demo site ID]](#)) is enough.

### Going the extra mile?

If you managed to achieve the main goal, you can add a bit of functionality for extra points. As you saw, there is a Boolean (0/1) field named `isadmin` in the user table. This additional functionality will make use of it:

- Add session management to your app (all languages, web frameworks allow this out of the box).
- When the logged in user is an admin (`isadmin` = 1), add on the “protected page” a link to a “log journal” page.
- Create the “log journal” page:
	- It should only accessible to logged in admin users.
	- It shows a list of all the user login attempts from the most recent to the oldest.
	- The format of the list should be: `[date time] – [successful or not attempt] – [username] ([first name] [last name])`.
	- Links to return to the “protected page” and to log out should be provided.
- When the user navigates back from the “log journal” to the “protected page” their credentials should not be asked again (the session should remember).

## Return your assignment

As you shared your repository back with us (as described earlier in this document), you only need to **commit** your changes to your repository and make sure you **push** your work to github.

When the deadline is reached, we will look at your repository and review the work done.

**Only commits up to the deadline will be considered.**

---


**Good luck and happy coding!**

---

*Laurent @ Humanstate*

