# Instructions for dummies

```powershell
# Create python virtual environment
python -m venv venv

# Activate python virtual environment
.\venv\Scripts\activate

# Download requirements
pip install -r requirements.txt

# Ensure docker before :)
# Activates a mongo instance
docker-compose up -d

# Run dev server
uvicorn app.main:app --reload
```
