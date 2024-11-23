Cyber Security Project

**Repository Link**:  
(https://github.com/ansonlol/cyber_security_projecct)

Installation Instructions::  
To run the application locally, follow these steps:
1. Clone the repository:  
git clone https://github.com/ansonlol/cyber_security_projecct
2. Navigate to the project directory:  
cd <project_directory>
3. Create and activate a virtual environment:    
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
4. Install the required dependencies: 
   pip install -r requirements.txt
5. Run the development server:  
   python manage.py runserver
6. Open your browser and go to `http://localhost:8000`.

According to the OWASP top ten list in 2021, the top five are broken access control, cryptographic failure, injection, insecure design and security misconfiguration. In this project, this five security flaws will be presented. There are two files namely notes/views.py and notes/secure_views.py where all the flaws and fixes are scripted respectively. 

**FLAW 1: Broken Access Control**

**Description of Flaw 1**:  
Broken Access Control happens when a program does not handle user permissions correctly, enabling users to reach resources they shouldn't have access to. In this scenario, all verified users have the ability to reach any note by entering the note's ID in the URL.
In order to show the vulnerabilities: 
First, create two different user accounts:
- Register user1 (e.g., alice)
- Register user2 (e.g., bob)
Login as user1 and create a note:
  - Click "Create New Note"
  - Create a private note with some content
  - Note the ID number in the URL (e.g., /notes/1/)
 Log out and login as user2
  Try accessing user1's note directly by using the URL: http://localhost:8000/notes/1/
This flaw allows users to view or manipulate notes that do not belong to them, violating the principle of least privilege.

**How to Fix It**:  
Implementing appropriate access control is crucial in order to address this problem, by making sure that users can only access the resources that belong to them. This can be accomplished by verifying the ownership of the note prior to granting access. If the note is not owned by the authenticated user, they must be redirected or denied entry.

---
 **FLAW 2: Cryptographic Failure**

**Description of Flaw 2**:  
A cryptographic failure occurs when an application uses weak or outdated cryptographic methods to protect sensitive data. In this case, the application uses **MD5** hashing for password storage, which is considered insecure due to its vulnerability to brute-force and hash collision attacks. 
In order to show the vulnerabilities: 
1. Register a new user
2. Check the database using Django admin:
   - Create a superuser if you haven't:
     python manage.py createsuperuser
   - Go to http://localhost:8000/admin
   - Look at the Users table
   - The password is stored as a weak MD5 hash
3. You can verify the weak hashing by using an online MD5 decoder
As a result, user passwords stored using MD5 are at risk of being compromised.

**How to Fix It**:  
To fix this flaw, use strong password hashing (bcrypt/Argon2) and proper encryption for sensitive data. The application should switch to a more secure cryptographic algorithm for password hashing. A widely recommended solution is to use Django's built-in password hashing system, which utilizes **PBKDF2** by default and offers far greater security. This change will ensure that user passwords are stored securely, making them resistant to common cryptographic attacks.

---

### **FLAW 3: SQL Injection**

**Description of Flaw 3**:  
SQL Injection is a vulnerability that allows attackers to manipulate database queries through unsanitized input. In this case, the application constructs SQL queries using string concatenation, which is vulnerable to SQL injection attacks. 
In order to show the vulnerabilities: 
1. Create some notes with content
2. In the search box, try these SQL injection payloads:
   - SQL injection: ' OR 1=1 --
3. All the notes will be displayed

An attacker could inject malicious SQL code into the search query, potentially gaining unauthorized access to sensitive data or even modifying the database.

**How to Fix It**:  
To prevent SQL Injection, the application should use **parameterized queries** or Django's built-in ORM, which safely handles user input. By using parameterized queries, user input is treated as data, not executable code, thereby mitigating the risk of SQL injection.

---

### **FLAW 4: Insecure Design**

**Description of Flaw 4**:  
Insecure design refers to weaknesses in the application's architecture that allow for potential abuse. One such weakness is the lack of rate limiting on login attempts. 
In order to show the vulnerabilities: 
1. Try to login with wrong credentials repeatedly
2. Notice there's no limit to login attempts

Without rate limiting, attackers can perform **brute-force attacks**, trying various combinations of usernames and passwords until they gain access to a user account.

**How to Fix It**:  
To mitigate this vulnerability, the application should implement **rate limiting** for login attempts. This can be done by integrating a tool like **django-axes** or **django-ratelimit**, which will track failed login attempts and lock accounts or prompt for additional verification (e.g., CAPTCHA) after a certain number of failed attempts. This will significantly reduce the effectiveness of brute-force attacks.

---

### **FLAW 5: Security Misconfiguration**

**Description of Flaw 5**:  
Security misconfiguration happens when the application is incorrectly set up, leading to unintended exposure of sensitive data or services. In this case, detailed error messages are shown to the user when an exception occurs. 
In order to show the vulnerabilities: 
1. Login to any account
2. Try to cause any error:
   - Type directly an non-existing url such as http://localhost:8000/nothinghere
   - Try creating a note with missing fields
3. Notice that the error page shows detailed error messages that could help attackers understand the application structure

This can expose stack traces, database structure information, or other sensitive data that could help an attacker craft a more effective attack.

**How to Repair the Issue**: 

In order to fix this issue, the app must hide specific error messages when in production. Instead, error messages should be made to be general and only give the user the essential information about the issue without unnecessary details. Furthermore, the server side should securely log error details for later examination by developers or administrators. This guarantees that end users are not exposed to sensitive information, but still enables developers to troubleshoot and resolve problems. 

In conclusion: 

This report highlights and describes the five main security vulnerabilities discovered in the web application, offering remedies for each one. Fixing these weaknesses will enhance the security and robustness of the application, making it more resistant to typical forms of unauthorized access, weak encryption, SQL injection, brute-force attacks, and disclosure of confidential information. Implementing these adjustments will greatly enhance the security of the application and safeguard user data and privacy. 




