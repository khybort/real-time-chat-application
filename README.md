# Real-Time Chat Application

A real-time chat application built with Django and React that allows users to communicate in different chat rooms. This project demonstrates real-time messaging using WebSockets, efficient database design, and seamless integration between Django and React.

---

## Table of Contents

- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Running the Application Locally](#running-the-application-locally)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)

- [Contributing](#contributing)
- [Optional Features](#optional-features)

---

## Features

### Backend Features (Django)
- **Authentication**: Token-based authentication with register and login endpoints.
- **Chat System**:
  - Create and join chat rooms.
  - Send and receive messages in real-time using WebSockets.
  - Store chat history in a relational database.
- **Optimized Database Design**:
  - Proper relationships between users, chat rooms, and messages.
  - Indexed fields for faster queries.

### Frontend Features (React)
- **User Interface**:
  - Login user
  - Register user
  - List of chat rooms.
  - Chat interface with message history.
- **Real-Time Messaging**:
  - WebSocket integration for instant updates.
  - State management using React hooks.
- **Styling**:
  - Responsive UI with Tailwind CSS.

---

## Setup Instructions

### Requirements
- Python 3.12+
- Node.js 20+
- npm 11+
- PostgreSQL 15+ (or other compatible databases)

### Environment Setup

#### 1. Clone the Repository
```sh
git clone https://github.com/khybort/real-time-chat-application.git
cd real-time-chat-application
```

#### 2. Start the application
```sh
make build-prod
make up-prod
```

#### 3. Configure the Database
Update environment file
```sh
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=http://localhost,http://127.0.0.1,localhost,ui-prod,api-prod
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://ui-prod
DB_NAME=chatdb
DB_USER=chat
DB_PASSWORD=chat
DB_HOST=db
DB_PORT=5432
DJANGO_SETTINGS_MODULE=config.settings.production

ACCESS_TOKEN_LIFETIME=10
REFRESH_TOKEN_LIFETIME=5
```

#### 4. Apply Migrations
```sh
Migrations are automatically generated but you can use also these commands
python manage.py makemigrations
python manage.py migrate
```


---

## Running the Application Locally

#### 1. Start real time chat application with docker
```sh
make build-prod
make up-prod
```

#### 2. Access the Application
- **Frontend**: [http://localhost](http://localhost)
- **Backend API**: [http://localhost:8000](http://localhost:8000)

#### 3. Down the Application
```sh
make down
```

---

## API Documentation

### Authentication

#### Register User
**POST** `/auth/register/`

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```
**Response:** JSON token

#### Login User
**POST** `/auth/login/`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```
**Response:** JSON token

### Chat Rooms

#### Get All Chat Rooms
**GET** `/chat/rooms/`

**Response:** List of chat rooms

#### Create a Chat Room
**POST** `/chat/rooms/`

**Request Body:**
```json
{
  "name": "string"
}
```
**Response:** New chat room details

### Messages

#### Get Messages in a Room
**GET** `/chat/messages/{room_id}/messages/`

**Response:** List of messages in the room

#### Send a Message
**POST** `/chat/rooms/{room_id}/messages/`

**Request Body:**
```json
{
  "message": "string"
}
```
**Response:** New message details

---

## Database Schema

### Models

#### User
```python
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
```

#### ChatRoom
```python
class Room(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Message
```python
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Relationships
- A **user** can be in multiple **chat rooms**.
- A **room** can have multiple **messages**.
- A **user** can send multiple **messages**.

### Indexes
- `Room.name` is indexed for faster lookups.
- `Message.created_at` is indexed for efficient ordering.

---

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```sh
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```sh
   git commit -m 'Add your feature'
   ```
4. Push to the branch:
   ```sh
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request.

If you encounter any issues, please open an issue in the Issues Tab.

---

This README provides a comprehensive guide to setting up and understanding the real-time chat application. It covers all necessary steps to run the application locally and explains the architecture and design choices.

