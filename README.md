# QA Automation Portfolio — API Testing | pytest | Python | Pydantic

Hi! I'm **Maurice Cabrejas Martínez**, a passionate **QA Automation Engineer** with over 15 years of experience ensuring software quality through automation. This repository showcases my expertise in **API Test Automation** using modern Python frameworks, schema validation, and performance testing against the **Restful Booker** platform.

---

## 🛠️ Skills Highlight
- **Programming Languages:** <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white " alt="Python">  
- **Test Frameworks:** <img src="https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white " alt="pytest">  
- **API Testing:** <img src="https://img.shields.io/badge/Requests-2C2C2C?logo=python&logoColor=white " alt="Requests"> <img src="https://img.shields.io/badge/REST-API-FF6C37?logo=fastapi&logoColor=white " alt="REST API">  
- **Schema Validation:** <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white " alt="Pydantic">  
- **Data Generation:** <img src="https://img.shields.io/badge/Faker-00BFA5?logo=faker&logoColor=white " alt="Faker">  
- **Tools & Methodologies:** <img src="https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white " alt="Git"> <img src="https://img.shields.io/badge/Agile-009B77?logo=agile&logoColor=white " alt="Agile">  
- **Specialties:** API Testing, Performance SLA Validation, Data Contract Testing, CI/CD Integration  

---

## 🚀 Project Overview
This portfolio demonstrates:
- **Comprehensive API test automation** for Restful-Booker RESTful service
- **Schema validation** using Pydantic models ensuring data contract integrity
- **Dynamic test data generation** with Faker factories for reproducible tests
- **Performance & SLA testing** with precise response time thresholds
- **Robust authentication handling** and teardown strategies with pytest fixtures
- **Clean architecture** separating concerns: config, schemas, factories, and tests

---

## 📂 Repository Structure
```plaintext
.
├── config/                 # Configuration constants
│   └── config.py          # Base URLs, endpoints, credentials
├── schemas/                # Pydantic data models
│   ├── booking_schemas.py # Data validation & serialization
│   └── factories.py       # Fake data generators
├── tests/                  # Test suites
│   ├── test_auth.py       # Authentication & authorization tests
│   ├── test_booking.py    # CRUD operations tests
│   └── test_booking_performance.py  # Performance & SLA tests
├── conftest.py            # pytest fixtures (auth_token, existing_booking_id)
├── requirements.txt       # Python dependencies
└── README.md              # You are here!
```

---

## 🏃‍♂️ How to Run Tests

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/qa-automation-api-booker.git 
   cd qa-automation-api-booker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute tests**:
   ```bash
   # Run all tests
   python -m pytest -v
   
   # Run specific test suite
   python -m pytest tests/test_booking.py -v
   
   # Run with parallel execution (requires pytest-xdist)
   python -m pytest -n 4 -v
   
   # Run performance tests only
   python -m pytest tests/test_booking_performance.py -v
   ```

---

## 🔍 Key Features
- **🔐 Token-based Authentication** → Automated token retrieval and lifecycle management
- **✅ Schema Contract Validation** → Pydantic models enforce strict API response contracts
- **🎲 Smart Test Data** → Faker-generated valid data with optional overrides for edge cases
- **⚡ Performance Assertions** → SLA validation for POST/GET/PUT/DELETE operations
- **🧹 Automated Teardown** → Fixtures ensure test isolation and cleanup
- **🎯 Business Logic Validation** → Check-in < Check-out date & data type integrity
- **🚫 Negative Testing** → Invalid token handling & 403 Forbidden validation

---

## 📌 Experience Context
With roles like:
- **QA Automation Engineer** @ GSoft Innovation (200+ automated tests in Selenium/C#)  
- **Software Analyst/Project Manager** (Agile, TestRail, Redmine, Jira)  
- **15+ years** refining QA processes across industries  

This project reflects my commitment to **reliable, maintainable, and scalable** test automation with emphasis on **data integrity** and **performance compliance**.

---

## 📬 Contact
Let's connect!  
📧 **mauro211@gmail.com**  
🔗 **[LinkedIn](https://www.linkedin.com/in/mauricecabrejas/ )**
