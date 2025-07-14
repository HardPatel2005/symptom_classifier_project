Here’s a complete and well-structured `README.md` for your **🩺 AI Symptom Classifier (Django + LangGraph + Gemini API)** project:

---


# 🩺 AI Symptom Classifier (Django + LangGraph + Gemini API)

This project is a web-based symptom classifier built with Django, leveraging the power of **LangGraph** for orchestrating conversational flows and the **Google Gemini API** for intelligent symptom analysis. It provides initial symptom classification and general information, guiding users toward appropriate next steps.

> ⚠️ **Disclaimer:** This AI-powered tool is for demonstration purposes only and does **not** provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

---

## ✨ Features

- 📝 **Symptom Input**: Submit symptoms via a clean, responsive web form.
- 🤖 **AI-Powered Classification**: Categorizes symptoms into:
  - **Emergency**
  - **Mental Issue**
  - **General**
- 🔁 **Dynamic Routing**: LangGraph adjusts the conversation flow based on symptom classification.
- 📚 **Category Information**: Provides a short general overview of the symptom category.
- ❓ **Follow-Up Questions**: For general symptoms, prompts relevant clarifying questions.
- 💡 **Initial Advice**: Offers basic advice with a disclaimer to consult a doctor.
- 🧾 **Conversation Summary**: Summarizes the entire AI-user interaction.
- 🗃️ **Database Logging**: Stores symptoms, classification, and AI responses in PostgreSQL (or SQLite in development).
- 📱 **Responsive UI**: Built with Tailwind CSS for a clean and mobile-friendly design.

---

## 🚀 Tech Stack

| Component        | Technology                                |
|------------------|--------------------------------------------|
| Backend          | Django                                     |
| AI Orchestration | LangGraph                                  |
| LLM Integration  | LangChain + Google Gemini API (1.5 Flash)  |
| Frontend         | HTML + Tailwind CSS                        |
| Database         | PostgreSQL / SQLite                        |
| Env Management   | `venv`, `.env`, environment variables      |
| Deployment       | Render.com, Gunicorn                       |

---

## ⚙️ Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/symptom-classifier-django.git
cd symptom-classifier-django
````

> 🔁 Replace `your-username` with your actual GitHub username.

---

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
```

#### Activate it:

* **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```
* **Windows (CMD)**:

  ```cmd
  venv\Scripts\activate.bat
  ```
* **Windows (PowerShell)**:

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` not yet generated, run:

```bash
pip install Django langgraph langchain-google-genai google-generativeai langchain_core psycopg2-binary dj-database-url
pip freeze > requirements.txt
```

---

### 4. Set Your Gemini API Key

#### On macOS/Linux:

```bash
export GOOGLE_API_KEY="your_actual_gemini_api_key"
```

#### On Windows (CMD):

```cmd
set GOOGLE_API_KEY="your_actual_gemini_api_key"
```

#### On Windows (PowerShell):

```powershell
$env:GOOGLE_API_KEY="your_actual_gemini_api_key"
```

> 🔐 Never commit your API key to version control.

---

### 5. Configure Django Settings

In `symptom_classifier_project/settings.py`:

* Ensure these are configured:

```python
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    ...,
    'classifier_app',
]

TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]

STATIC_URL = '/static/'
```

* For development:

  ```python
  DEBUG = True
  ALLOWED_HOSTS = []
  ```

---

### 6. Apply Database Migrations

```bash
python manage.py makemigrations classifier_app
python manage.py migrate
```

---

### 7. Run the Server

```bash
python manage.py runserver
```

> Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🧑‍💻 Usage

1. Enter your symptom in the text field.
2. Click **"Classify Symptom"**.
3. View the following AI-generated results:

   * Classification (Emergency / Mental Issue / General)
   * Brief category info
   * Initial advice
   * Follow-up questions (if needed)
   * Summary of conversation
   * Full AI conversation log

---

## ☁️ Deployment (Render.com)

### 🔧 Prepare for Deployment

* Set `DEBUG = False`
* Add production domain to `ALLOWED_HOSTS`
* Use environment variables:

  ```python
  SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
  GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
  ```
* Add:

  ```python
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
  ```

### 📁 Files to Add

* `requirements.txt` (already created)
* `Procfile`:

  ```procfile
  web: gunicorn symptom_classifier_project.wsgi --log-file -
  ```

---

### ⚙️ Render Configuration

* **Build Command**:

  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```

* **Start Command**:

  ```bash
  gunicorn symptom_classifier_project.wsgi --log-file -
  ```

* **Environment Variables**:

  * `DJANGO_SECRET_KEY`
  * `GOOGLE_API_KEY`
  * `DATABASE_URL` (auto-created if using Render PostgreSQL)

---

## 🛡️ Disclaimer

> ⚠️ **Important Medical Disclaimer:**
>
> This AI Symptom Classifier is a demonstration tool only. It is **not** intended to diagnose, treat, or prevent any medical condition. Always seek the guidance of a qualified doctor or health professional regarding any medical condition or concerns.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Hard Patel**
GitHub: [@HardPatel2005](https://github.com/HardPatel2005)
Twitter: [@Hard\_patel\_201](https://x.com/Hard_patel_201)
Instagram: [@hard\_patel201](https://www.instagram.com/hard_patel201)

---

## ⭐️ Show Your Support

If you like this project, please give it a ⭐️ on [GitHub](https://github.com/your-username/symptom-classifier-django)!

```

---

Would you like this saved into a `README.md` file and exported?
```
