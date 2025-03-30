# API Endpoints Documentation
Hosted at:

## Authentication Endpoints
NB: All urls start with /api/

## POST /api/register/
- Usage: Register a new user
- Request Body:
    ```json
        {
            "username": "Enter your username",
            "email": "Enter your email",
            "password": "Enter your password"
        }
    ```
- Response:
    - STATUS 201 Created: user created successfully  
    - STATUS 400 Bad Request: Validation errors

## POST /api/login/
- Usage: Login registered users and return token
- Request Body:
    ```json
            {
                "username": "Enter your username",  
                "password": "Enter your password"
            }
    ```
- Response:
    - STATUS 200 OK: login successfull    
    - STATUS 401 Bad Unauthorised: Invalid username or password


## Users Endpoints
This endpoints allow CRUD operations on events and also registration for events

## POST /api/events/
- Usage: Create new events for organizers
- Requirements: 
    Add the token displayed after login in the Headers tab in Postman
    ```json
            {
                "key": "Authorization",  
                "Value": "Token your_login_token"
            }
    ```
- Request Body:
    ```json
            {
                "event_title": "Walking in Tech",  
                "event_category": "Tech",  
                "event_description": "Join us for an interactive session on the evolving world of tech",  
                "event_date": "2025-04-05",  
                "event_time": "10:30",  
                "event_location": "Westlands, Nairobi",  
                "event_slots": "100"
            }
    ```

## GET /api/events/
For organizers, this endpoint shows only all events they have created  
For normal users, this endpoint shows all events available
- Usage: View all events
- Requirements: Add authentication token

## GET /api/upcoming-events/
For organizers, this endpoint shows only all events they own that are happening 5 days from the present date  
For normal users, this endpoint shows all events that are happening 5 days from the present date  
- Usage: View upcoming events
- Requirements: Add authentication token

## PUT /api/events/{event_id}/
For event organizers ONLY.
- Usage: Update an event field
- Requirements: Add authentication token
- Request Body:
    ```json
            {
                "event_title": "Walking in Tech",  
                "event_category": "Tech",  
                "event_description": "Join us for an interactive session on the evolving world of tech",  
                "event_date": "2025-04-05",  
                "event_time": "10:30",  
                "event_location": "Westlands, Nairobi",  
                "event_slots": "50"
            }
    ```

## GET /api/events/?title={title/category}/
- Usage: Search event by title or event category
- Requirements: Add authentication token

## DELETE /api/events/{event_id}/
For organizers ONLY
- Usage: Delete an event
- Requirements: Add authentication token

## POST /api/registrations/ 
Event organizers are not allowed to register for their own events
- Usage: Register for an event
- Requirements: Add authentication token
- Request Body: 
    ```json
            {
                "event": "Enter event id",  
                "phone_number": "Enter your phone number"
            }
    ```

## POST /api/registrations/{registration_id}
- Usage: Update registration details for an event
- Requirements: Add authentication token
- Request Body: 
    ```json
            {
                "event": "Enter event id",  
                "phone_number": "Enter your phone number"
            }
    ```


## GET /api/attendees/
For Event organizers ONLY
- Usage: Check list of attendees registered for your event only
- Requirements: Add authentication token



### ANY CONTRIBUTIONS TO THIS PROJECT ARE WARMLY WELCOMED