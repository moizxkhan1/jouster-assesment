# Text Analysis FastAPI Application

A FastAPI-based text analysis tool that processes unstructured text to extract summaries, metadata, sentiment, and keywords using OpenAI's structured outputs and persistent database storage.

## How to Run

1. **Set up environment:**

   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key and database URL
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database:**

   ```bash
   alembic upgrade head
   ```

4. **Run the application:**

   ```bash
   python main.py
   ```

5. **Access the application:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Docker Deployment

1. **Set up environment:**

   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key and external database URL
   ```

2. **Build and run with Docker:**

   ```bash
   docker-compose up -d --build
   ```

3. **Access the application:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Project Structure

- **`app/`** - Main application code with clean separation of concerns
- **`app/lib/`** - External service integrations (OpenAI client, NLTK keyword extraction)
- **`app/database/`** - SQLAlchemy models and database configuration
- **`app/routers/`** - API endpoints and web interface routes

## Design Choice / Why I choose this structure?

This is a fairly normal structure for most Fast API apps. I'll simply list down some benefits

- Clear separation of concerns
- Since this is a modular design, it is easy and cleaner to add more stuff to it. Also makes the code more maintainable in general
- Structured logging provides clear visibility to your activity
- Pydantic ensure validation

## What challenges you faced?

- I was using gemini with openai sdk, but I wanted to add output validation. So I decided to use OpenAI's structured output and switched to that, saving me from manual validation

## Trade offs you made:

- The frontend, didn't really want to spend too much time on setting it up separately, so decided to go for a simpler approach

## Time spent?

- Roughly around 1.5 hours. Did run into issues trying to manually validate the output when using Gemini initally
