# eAcademy - Online Learning Platform

eAcademy is a feature-rich online learning platform developed using Django, Python, and PyCharm. It offers a comprehensive set of functionalities to create an interactive and seamless learning experience for both instructors and students. The platform encompasses various features, including course creation and management, membership options, payment gateway integration, and student progress tracking.

## Key Features:

- **Course Creation and Management:** Instructors can easily create and manage courses with multimedia content, lectures, quizzes, and assignments.

- **Membership Options:** eAcademy provides flexible membership options for students to access a variety of courses based on their preferences.

- **Payment Gateway Integration:** Seamless integration of payment gateways allows students to purchase courses securely.

- **Student Progress Tracking:** Instructors can monitor student progress, track course completion, and view performance statistics.

- **User-Friendly Interfaces:** eAcademy features user-friendly interfaces for easy navigation and intuitive interactions.

- **User Authorizations and Authentication:** The platform ensures secure user logins and personalized learning experiences with proper authorizations.

eAcademy aims to revolutionize online education, offering a robust platform that caters to the needs of both instructors and students. It fosters interactive learning, flexibility, and convenience, making it an ideal choice for online education providers.

## Setup and Run Instructions:

To set up and run eAcademy locally, follow these steps:

### Prerequisites:

1. Make sure you have Python installed on your system. You can download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Install Django, Pillow, and Stripe packages using pip. Open your terminal or command prompt and run the following commands:

```
pip install django
pip install Pillow
pip install stripe
```

### Clone the Repository:

1. Clone this repository to your local machine using Git:

```
git clone https://github.com/your-username/eAcademy.git
```

2. Navigate to the project directory:

```
cd eAcademy
```

### Database Setup:

1. Apply the database migrations to set up the initial database:

```
python manage.py migrate
```

2. Create a superuser account for accessing the Django admin panel:

```
python manage.py createsuperuser
```

### Run the Development Server:

Start the Django development server to run the eAcademy platform locally:

```
python manage.py runserver
```

Once the server is running, you can access the platform by visiting [http://localhost:8000/](http://localhost:8000/) in your web browser.

### Accessing the Django Admin Panel:

You can access the Django admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/) and log in using the superuser account you created earlier. This panel allows you to manage courses, users, and other platform-related data.

## Note:

The eAcademy project is continuously evolving, and new features and improvements are added regularly to enhance the learning experience. We encourage you to keep the repository updated and contribute to its development. If you encounter any issues or have suggestions, please feel free to open an issue or submit a pull request on the GitHub repository. Your contributions are highly appreciated!

Thank you for choosing eAcademy as your online learning platform! Happy learning!
