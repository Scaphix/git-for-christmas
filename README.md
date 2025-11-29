# Git for Christmas

## Project Description

This project is a Django-based web application designed to manage and share Christmas-related content. It includes features such as user authentication, content management, and more.

## Features

- User authentication
- Content management
- Database integration
- Environment variable management

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd git-for-christmas
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create an `env.py` file in the root directory and add your secrets (e.g., `SECRET_KEY`, `DATABASE_PASSWORD`).

5. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

## Wireframes

Below are the wireframes for the project:

### Desktop Wireframes

- **Homepage and Add Participant**
  ![Desktop Homepage and Add Participant Wireframe](Document/images/wireframes/Wireframe_Desktop_home_add_participant.png)
- **Results and Error Pages**
  ![Desktop Results and Error Pages Wireframe](Document/images/wireframes/Wireframe_Desktop_result_error.png)
- **View Participants and Admin Dashboard**
  ![Desktop View Participants and Admin Dashboard Wireframe](Document/images/wireframes/Wireframe_Desktop_view_admin.png)

### Mobile Wireframe

- **Homepage, Add Participant, and Dashboard**
  ![Mobile Combined Wireframe](Document/images/wireframes/Wireframe_mobile_home_add_dashboard.png)

### Tablet Wireframe

- **Homepage, Dashboard, and Add Participant**
  ![Tablet Combined Wireframe](Document/images/wireframes/Wireframe_tablet_home_add_dashboard.png)

## Database Schema

The project uses a simple relational database structure to support the core Secret Santa features: adding participants, preventing invalid pairings, and generating matches.

### Participant Table

Stores information about each person taking part in the Secret Santa.

| Field            | Type   | Description                                      |
|------------------|--------|--------------------------------------------------|
| id (PK)          | int    | Unique identifier for each participant          |
| name             | text   | Participant's name                              |
| email            | text   | Optional email address                          |
| wishlist         | longtext | Optional gift wishlist                          |
| dont_match_with  | int (FK) | Self-referencing field to avoid matching two specific people |

### Match Table

Stores the final Secret Santa pairings once generated.

| Field            | Type   | Description                                      |
|------------------|--------|--------------------------------------------------|
| id (PK)          | int    | Unique identifier for each match record         |
| giver_id (FK)    | int    | Participant who gives the gift                  |
| receiver_id (FK) | int    | Participant who receives the gift               |
| created_at       | datetime | Timestamp of when the match was created         |

### Relationships

- `Participant.dont_match_with → Participant.id`
  (Self-referencing relationship to support "don't match me with X".)

- `Match.giver_id → Participant.id`

- `Match.receiver_id → Participant.id`
  (Each match links a giver and a receiver.)

### ER Diagram

(Insert diagram screenshot here(Document/images/database/ER_digram.png))
