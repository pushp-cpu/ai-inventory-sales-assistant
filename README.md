AI Inventory & Sales Assistant

An AI-powered inventory and sales management application that allows users to query business data using natural-language questions.

## Live Demo

https://ai-inventory-sales-assistant.vercel.app/

## Architecture

```text
Next.js → FastAPI → Neon PostgreSQL
              ↓
          Gemini API

Features
- Natural-language queries for inventory and sales data
- AI-powered business question answering using Gemini
- Inventory and stock-level lookup
- Low-stock detection based on reorder levels
- Total revenue reporting
- Best-selling product analysis
- Sales transaction lookup
- Supplier information lookup
- Interactive quick-question interface
- REST API with FastAPI and Swagger documentation
- PostgreSQL database hosted on Neon
- Production deployment using Vercel and Render
AI Tool Calling
The application uses Gemini function calling to connect natural-language questions with backend business-data tools.
Available tools include:
- get_products
- get_sales
- get_low_stock_products
- get_total_revenue
- get_best_selling_products
When a question requires business data, Gemini can request the appropriate backend tool. The application executes the tool, sends the result back to Gemini, and generates the final natural-language response.
Tech Stack
Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- React Markdown
Backend
- Python
- FastAPI
- Pydantic
- Uvicorn
Database
- PostgreSQL
- Neon
AI
- Google Gemini API
- Gemini Function Calling
Deployment
- Vercel
- Render
- Neon
Project Structure
ai-inventory-sales-assistant/
├── api/
│   └── routes.py
├── services/
│   ├── ai_service.py
│   ├── ai_tools.py
│   └── database_service.py
├── frontend/
│   ├── app/
│   ├── package.json
│   └── ...
├── database.py
├── main.py
├── requirements.txt
├── render.yaml
└── README.md

API Endpoints
Method	Endpoint	Purpose
GET	/products	Retrieve products
GET	/suppliers	Retrieve suppliers
GET	/sales	Retrieve sales
GET	/reports/revenue	Calculate total revenue
GET	/reports/low-stock	Find low-stock products
GET	/reports/best-selling	Rank products by quantity sold
POST	/ask	Ask the AI assistant
GET	/health	Backend health check


Running Locally
Backend
Install the Python dependencies:
pip install -r requirements.txt

Create a .env file in the project root:
DATABASE_URL=your_neon_database_url
GEMINI_API_KEY=your_gemini_api_key

Start the backend:
uvicorn main:app --reload

Backend:
http://127.0.0.1:8000

Swagger documentation:
http://127.0.0.1:8000/docs

Frontend
Open a new terminal and move into the frontend:
cd frontend

Install dependencies:
npm install

Create frontend/.env.local:
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

Start the frontend:
npm run dev

Frontend:
http://localhost:3000

Deployment
The application is deployed using:
- Vercel — Next.js frontend
- Render — FastAPI backend
- Neon — PostgreSQL database
- Google Gemini API — AI functionality
Environment variables are configured separately in the deployment platforms and are not committed to the repository.
Development Approach
The project was developed using AI-assisted programming as a development aid. AI tools were used for code guidance, debugging, implementation assistance, and understanding unfamiliar concepts. The application was tested locally and through the deployed production environment.
License
This project is intended for educational and portfolio purposes.