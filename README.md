# AI Code Review Agent

An AI-powered system that analyzes code or GitHub repositories and provides insights such as code quality, issues, complexity, and improvement suggestions using Machine Learning and Large Language Models.

---

## Features

* Analyze raw code snippets
* Analyze GitHub repositories
* Detect issues such as bad practices, bugs, and inefficient logic
* Generate code quality score
* Provide improvement suggestions
* Support multilingual feedback (English, Hindi, Hinglish)
* Interactive frontend interface

---

## Tech Stack

### Frontend

* Next.js (React)
* Tailwind CSS

### Backend

* FastAPI (Python)
* Scikit-learn (Machine Learning models)
* LangChain and LangGraph (LLM integration)

### DevOps and Deployment

* Docker and Docker Compose
* AWS EC2
* GitHub Actions (CI/CD)
* DuckDNS (Domain mapping)

---

## Project Structure

```id="struct1"
AI_Code_Review_Agent/
│
├── backend/
│   ├── app/
│   ├── ml_models/
│   ├── temp_repo/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/app/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## Dataset

### dataset.csv

Contains code snippets with associated issues, complexity, and score.

### multilang.csv

Contains multilingual feedback with labels such as bug, readability, optimization, and good.

### Real-time data

* GitHub repositories
* User input code

---

## Working

1. User provides code or GitHub repository URL
2. Backend clones the repository if required
3. Code is extracted and processed
4. Machine Learning model generates score and classification
5. LLM generates detailed analysis and suggestions
6. Results are displayed on the frontend

---

## Docker Setup

Run the application locally:

```bash id="cmd1"
docker-compose up -d --build
```

Access:

* Frontend: http://localhost:3000
* Backend: http://localhost:8000/docs

or live :
http://54.209.50.231:3000

---

## AWS EC2 Deployment

1. Launch an EC2 instance
2. Install Docker and Docker Compose
3. Clone the repository

```bash id="cmd2"
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

4. Start services

```bash id="cmd3"
docker-compose up -d --build
```

---

## CI/CD Pipeline

Configured using GitHub Actions.

On every push to the main branch:

* Code is pulled on EC2
* Docker containers are rebuilt
* Application is restarted

---

## Results

* Accuracy: 88–92%
* Precision: ~85%
* Recall: ~87%
* F1 Score: ~86%
* Response time: 2–5 seconds

---

## Limitations

* Large repositories may increase processing time
* Dependency on internet for GitHub cloning
* Limited programming language coverage
* LLM response latency

---

## Future Scope

* Support for more programming languages
* Integration with IDEs such as VS Code
* Automated pull request review
* Improved ML models
* Performance optimization

---

## Author

Harsh Kumar

---

## License

This project is for academic and educational purposes.

