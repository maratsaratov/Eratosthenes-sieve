# Eratosthenes-sieve

Web version of the "Sieve of Eratosthenes" algorithm for visualizing the process of finding prime numbers.

## Project Description

The client-server application "Sieve of Eratosthenes" is designed to visualize the algorithm for finding prime numbers using the Sieve of Eratosthenes method. It allows users to visually see the process of number filtering and prime number highlighting, which promotes better understanding of mathematical concepts.

## Functionality

- **User Authentication**: User registration and login system
- **Sieve Visualization**: Generation of graphical representation of the Sieve of Eratosthenes
- **ASCII Representation**: Creation of text-based sieve version
- **Operation History**: Saving and viewing previous generations
- **Security**: Password hashing and session management

## Technologies

- **Backend**: Python, Flask
- **Database**: SQLite
- **Visualization**: Matplotlib, PIL
- **Frontend**: HTML, CSS, JavaScript
- **Security**: SHA-256 hashing

## Project Structure

```
Eratosthenes-sieve/
├── server.py              # Main server file
├── users.db               # Database (created automatically)
├── templates/             # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── menu.html
│   ├── generate_sieve.html
│   └── history.html
└── README.md
```

## Installation and Launch

1. Ensure Python 3.x is installed
2. Install required dependencies:
   ```bash
   pip install requirements.txt
   ```
3. Run the application:
   ```bash
   python server.py
   ```
4. Open your browser and go to: `http://localhost:5000`

## Usage

1. **Registration**: Create an account with email and password (at least 10 characters)
2. **Login**: Authenticate in the system
3. **Sieve Generation**: Enter a number to build the Sieve of Eratosthenes
4. **View History**: Review previous results
5. **Logout**: End the working session

## Implementation Features

- Sieve of Eratosthenes algorithm optimized for efficient prime number finding
- Dual visualization: graphical and ASCII representation
- Automatic determination of optimal grid size
- Saving results in database with user association
- Responsive interface design

## Database

The application uses SQLite database with the following tables:
- `users` - user data (email and password hashes)
- `history` - sieve generation history (number, image, ASCII representation)

## Security

- Passwords stored in hashed form (SHA-256)
- Session management for authentication
- Input data validation
- Minimum password length - 10 characters

## Author

The project is developed as a web implementation of a classical mathematical algorithm for educational purposes.