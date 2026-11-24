# Làm việc nhóm 2 người

## Phân công đề xuất

- **Thành viên A – AI/Backend:** `app/`, `scripts/`, `models/`, database và API.
- **Thành viên B – Frontend/Deploy:** `frontend/`, `Dockerfile`, `docker-compose.yml`, responsive/PWA và kiểm thử trình duyệt.

Mỗi pull request phải chạy `pytest`, `cd frontend; npm test` và `cd frontend; npm run build`.
Không commit secret trong `.env`; dùng `.env.example`. Checkpoint model phải đi kèm
`plant_health.labels.txt`, metadata và evaluation report.

## Deploy

1. Copy `.env.example` thành `.env`, đặt `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
2. Đảm bảo `models/plant_health.pt` tồn tại.
3. Chạy `docker compose up --build -d`.
4. Truy cập frontend qua cổng `8080`, API docs tại `/docs`.
