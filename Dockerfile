# 가볍고 최적화된 Python 3.11 slim 이미지를 베이스로 사용합니다.
FROM python:3.11-slim

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /usr/src/app

# 시스템 의존성 패키지 설치를 최소화하고 pip 캐시를 사용하지 않아 이미지 용량 최적화
# (scikit-learn, pandas 등은 wheel 형태로 설치되므로 slim 이미지로도 충분합니다)
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사 (requirements.txt 분리로 캐싱 최적화)
COPY ./app ./app

# FastAPI 포트 노출
EXPOSE 8000

# 서버 실행 (보안상 python -m uvicorn 사용)
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
