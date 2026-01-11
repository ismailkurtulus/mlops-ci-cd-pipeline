# MLOps HW2 - CI/CD Pipeline (HCPS)

Bu repo, PDF'teki Part 1 (CI), Part 2 (CD/acceptance), Part 3 (stop-the-line) gereksinimlerini örneklemek için hazırlanmıştır.

## 0) GitHub'a yükle
1) Zip'i aç
2) Yeni bir GitHub repo oluştur
3) Dosyaları commit & push et
4) GitHub Actions sekmesinde pipeline çalışacak: Unit -> Lint -> Component -> Package -> Smoke

## 1) Local run (opsiyonel)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python scripts/init_db.py
export DB_PATH=./db/app.db
uvicorn src.service:app --reload --port 8000
```

Health:
- http://localhost:8000/health

Predict:
```bash
curl -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d '{"user_id":"user_123"}'
```

## 2) Test + Lint
```bash
pytest -q tests/unit
pytest -q tests/component
flake8 .
```

## 3) Docker build & smoke (opsiyonel)
```bash
docker build -t hcps:local -f docker/Dockerfile .
chmod +x scripts/smoke_test_ci.sh
./scripts/smoke_test_ci.sh hcps:local 8000
```

## 4) Part 3 - Stop the Line (sabotage gösterimi)
### A) Unit test fail ettir
- `src/feature_engineering.py` içinde `hashed_feature` fonksiyonunu boz (ör. `return 0`)
- Commit + push
- Beklenen: Unit job fail -> sonraki adımlar (package/smoke) çalışmaz.

### B) Lint / syntax fail ettir
- Herhangi bir .py dosyasına syntax hatası ekle (ör. parantez sil)
- Commit + push
- Beklenen: lint veya test import fail -> pipeline durur.
