Chatterbox: A Real-time WebSocket Chat Application
Chatterbox is a professional-grade, real-time communication platform built during the Infosys Springboard Virtual Internship. The application leverages WebSockets and the FastAPI framework to provide instantaneous, bidirectional communication between multiple users across isolated chat rooms.

Project Journey
The project was developed in four distinct milestones, evolving from a basic connection to a feature-rich multi-room system:
Milestone 1: Established the foundation using the WebSocket protocol for persistent, two-way communication.
Milestone 2: Implemented message broadcasting and identity handling via usernames.
Milestone 3: Introduced room-based architecture and real-time user interaction features like typing indicators.
Milestone 4: Final integration, UI/UX enhancement, and professional error handling for production readiness.

Key Features
Persistent Two-Way Communication: Unlike the standard Request-Response model, Chatterbox creates a continuous channel where both client and server can send data anytime without page refreshes.
Room-Based Architecture: Users can join specific rooms (e.g., General, Tech, Fun). Messages are isolated so they are only visible to users within the same room.
Real-time Typing Indicators: Enhances User Experience (UX) by showing "X is typing..." alerts when a user interacts with the input field.
System Notifications: Automated alerts (Join/Leave) keep the room updated on user activity
Modern UI/UX: A responsive dark-themed interface featuring auto-scrolling to the latest messages and visual differentiation between user and system messages.

Technology Stack
Backend: FastAPI (Python)
Server: Uvicorn (ASGI server)
Frontend: HTML5, CSS3, and Vanilla JavaScript
Communication Protocol: WebSockets (Bi-directional, low-latency)

Project Structure
Chatterbox/
├── main.py          # FastAPI Backend (Connection handling, logic, and broadcasting)
├── index.html       # Frontend (User Interface and Client-side WebSocket events)
└── README.md        # Project documentation and setup guide

Installation and Setup
1. Install Dependencies:
Ensure you have Python installed, then run the following command to install the required libraries:
pip install fastapi uvicorn
2. Run the Application:
Start the WebSocket server by executing the Python file:
python main.py
3. Access the Chat:
Open your browser and navigate to the local host address:
http://localhost:8000
4. Testing Multi-user Support:
Open multiple browser tabs or different browsers to simulate different users and test real-time interaction between rooms.

How It Works (Technical Flow)
Handshake: The client connects automatically via JavaScript using new WebSocket().
Join Event: The client sends a JSON object containing the username and selected room.
Broadcasting: The server receives messages and uses a custom broadcast() function to push data to every client whose state matches the specific room.
State Management: The backend maintains dictionaries to map WebSocket connections to usernames and room locations.
