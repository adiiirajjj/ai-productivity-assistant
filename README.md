 🧠 AI Productivity Assistant

An end-to-end AI/ML project using **FastAPI** and **Hugging Face API**  
to predict productivity categories ("Low", "Medium", "High")  
and generate intelligent insights.

---

 🚀 How to Run Locally

```bash
# 1. Clone repo
git clone https://github.com/adiiirajjj/ai-productivity-assistant.git
cd ai-productivity-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate data and train model
python data_generator.py
python train_model.py

# 4. Run FastAPI server
uvicorn main:app --reload
