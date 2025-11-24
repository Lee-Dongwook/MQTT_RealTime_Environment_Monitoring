# MQTT_RealTime_Environment_Monitoring

실시간 환경 모니터링 시스템

목표: 집이나 실험실 환경의 온도, 습도, 공기질 데이터를 수집하고 실시간 웹 대시보드로 표시

사용 기술: 라즈베리파이, DHT22/PM2.5 센서, MQTT, Python, Flask/Django

단계별 구성:

센서 연동: DHT22, PM2.5 센서를 라즈베리파이에 연결하고 Python으로 데이터 읽기

통신 구현: MQTT 브로커를 로컬 또는 클라우드(Mosquitto)로 구성, 센서 데이터 전송

데이터 처리: 수집된 데이터 간단한 필터링, 이상치 제거

웹 대시보드: Flask/React를 이용해 실시간 그래프 표시
