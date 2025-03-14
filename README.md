# FTL-Hackathon-1

A web application that helps users track their electricity consumption, estimate bills, and get energy-saving tips. Built with Flask and SQLAlchemy, this tool uses Ethiopian Electric Utility tariff rates to provide accurate cost estimations.

## Features
- 📊 Dashboard for monitoring electricity usage
- 💡 Real-time bill estimation based on appliance usage
- 💰 Ethiopian Electric Utility tariff-based calculations
- 📱 User registration and consumption tracking
- 💪 Dynamic form handling with HTMX
- 📋 Energy-saving tips and recommendations
- 💵 Current pricing information

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation
1. Clone the repository
```bash
git clone https://github.com/jae-red21/FTL-Hackathon-1.git
cd FTL-Hackathon-1
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
```

5. Initialize the database
```bash
flask db upgrade
```

6. Run the application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Bill Estimation
1. Navigate to the estimation page
2. Enter your appliances' power ratings (in watts)
3. Specify usage duration (in hours)
4. Add or remove rows as needed
5. Get instant cost estimation in ETB

### Tariff Ranges
The application uses the following Ethiopian Electric Utility tariff ranges:
- 0-50 kWh: 0.2730 ETB/kWh
- 51-100 kWh: 0.3564 ETB/kWh
- 101-200 kWh: 0.4993 ETB/kWh
- 201-300 kWh: 0.5500 ETB/kWh
- 301-400 kWh: 0.5666 ETB/kWh
- 401-500 kWh: 0.5880 ETB/kWh
- >500 kWh: 0.6943 ETB/kWh

## Tech Stack
- Backend: Flask (Python)
- Database: SQLite with SQLAlchemy
- Frontend: HTML, HTMX
- API: Flask-RESTful
- Styling: CSS

## Project Structure
```
FTL-Hackathon-1/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## API Documentation

### Authentication
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
```

### Consumption Endpoints
```
GET /api/consumption
POST /api/consumption
PUT /api/consumption/<id>
DELETE /api/consumption/<id>
```

## Testing
Run the test suite:
```bash
python -m pytest
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Team Members
- [Hilina Amare](https://github.com/Hilina123amare)
- [Mussie Leake](https://github.com/mussieleake)
- [Yared Zenebe](https://github.com/jae-red21)

## Acknowledgments
- Ethiopian Electric Utility for providing tariff information
- [Flask Documentation](https://flask.palletsprojects.com/)
- [HTMX](https://htmx.org/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
Yared Zenebe  - yared.zenebe.asmelash@gmail.com

Project Link: [https://github.com/jae-red21/FTL-Hackathon-1](https://github.com/jae-red21/FTL-Hackathon-1)