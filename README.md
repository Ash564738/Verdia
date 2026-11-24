# Smart Plant Care AI

Nền tảng demo end-to-end cho chẩn đoán và theo dõi sức khỏe cây trồng:

- `POST /api/v1/diagnose`: nhận ảnh lá và trả về chẩn đoán.
- `POST /api/v1/auth/register`, `POST /api/v1/auth/login`: tài khoản và token.
- `/api/v1/my-plants`: CRUD cây trồng của người dùng.
- `/api/v1/diagnoses`: lịch sử chẩn đoán, feedback và top predictions.
- `/api/v1/diseases`: thư viện bệnh cây.
- `/api/v1/analytics`: dashboard và phân tích theo cây.
- `/api/v1/care-logs`, `/api/v1/reminders`: nhật ký và lịch chăm sóc.
- `/api/v1/admin/*`: quản trị (yêu cầu role `ADMIN`).
- `POST /api/v1/qa`: hỏi đáp tiếng Anh về chăm sóc cây.
- `GET /docs`: Swagger UI.

Backend hỗ trợ SQLite cho development và PostgreSQL cho deployment qua `DATABASE_URL`.
Trong Docker Compose, PostgreSQL chạy tự động với volume `postgres-data`. Tạo tài khoản quản trị khi khởi động bằng
`ADMIN_EMAIL` và `ADMIN_PASSWORD`. Mô hình TorchScript đã train đặt tại `models/plant_health.pt`, kèm labels và metrics.
Endpoint chẩn đoán chính từ chối request với HTTP 503 nếu checkpoint không được triển khai,
không sinh kết quả giả.

## 1. Chuẩn bị môi trường

Yêu cầu:

- Windows 10/11, Python 3.12/3.13 và Node.js 22+.
- Nếu chạy Docker: Docker Desktop phải đang **Running**.
- Model thật đã có sẵn tại `models\plant_health.pt`.

Mở PowerShell tại thư mục `E:\Verdia`:

```powershell
cd E:\Verdia
```

## 2. Chạy backend local

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Kiểm tra backend:

```powershell
Invoke-RestMethod http://localhost:8000/health
Start-Process http://localhost:8000/docs
```

Kết quả health phải có `"status": "ok"`, `"database": "ok"` và model không phải
`fallback`.

## 3. Chạy frontend local

Mở PowerShell thứ hai:

```powershell
cd E:\Verdia\frontend
npm install
npm run dev -- --host 0.0.0.0
```

Mở `http://localhost:5173`. Giao diện hỗ trợ:

- Landing page công khai và thư viện bệnh
- Đăng ký, đăng nhập, hồ sơ và đăng xuất
- Dashboard có dữ liệu thật
- Chẩn đoán AI bằng file/camera/drag-drop
- Quản lý cây, lịch sử, chăm sóc, nhắc nhở và thông báo
- Quản trị, model evaluation và audit log cho tài khoản `ADMIN`

Kết quả được lưu trong lịch sử của cây.

## 4. Kiểm thử

Từ PowerShell tại thư mục gốc:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
cd frontend
npm test -- --run
npm run build
```

## 5. Tài khoản quản trị

Sửa `.env`:

```env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=đặt-mật-khẩu-dài-và-mạnh
SECRET_KEY=chuỗi-ngẫu-nhiên-dài
```

Khởi động lại backend, sau đó đăng nhập bằng tài khoản này để gọi các endpoint
`/api/v1/admin/*`.

## 6. Chạy production bằng Docker

Cài và mở Docker Desktop trước, sau đó:

```powershell
cd E:\Verdia
Copy-Item .env.example .env
notepad .env
docker compose up --build -d
docker compose ps
```

Truy cập:

- Frontend: `http://localhost:8080`
- Backend health: `http://localhost:8000/health`
- Swagger: `http://localhost:8000/docs`

Dừng hệ thống:

```powershell
docker compose down
```

Database và model được mount từ `data\` và `models\`, nên dữ liệu không mất khi
container được tạo lại.

## 7. Mở trên điện thoại trong cùng Wi-Fi

Lấy IP máy tính:

```powershell
ipconfig
```

Tìm `IPv4 Address`, ví dụ `192.168.1.20`. Trên điện thoại mở:

```text
http://192.168.1.20:8080
```

Cho phép cổng 8080/8000 trong Windows Firewall nếu thiết bị không kết nối được.
Nút chọn ảnh dùng camera mobile qua thuộc tính `capture="environment"`.

## Dataset, training và đánh giá

PlantVillage Color và PlantDoc đã được tải trong `data/`. Audit cũ trong repo
chỉ đếm file, không kiểm tra ảnh lỗi hay hash trùng; tạo audit có xác minh bằng:

```powershell
.\.venv\Scripts\python.exe scripts\audit_datasets.py
```

Chuẩn bị split theo protocol trong `Requirement.md`:

```powershell
.\.venv\Scripts\python.exe scripts\prepare_training_data.py
```

Script tải danh sách split official PlantVillage Color, dùng `leaf-map.json` để
chia theo nhóm lá, giữ nguyên 10.709 ảnh official test, rồi lấy 10% nhóm lá từ
official train làm validation. Những ảnh train có group trùng official test và
exact duplicate bị loại khỏi training. Audit hiện có 54.305 ảnh PlantVillage
Color hợp lệ và 2.583 ảnh PlantDoc hợp lệ (29 thư mục nhãn), không có ảnh hỏng
và không có exact duplicate giữa hai bộ. 11 nhóm PlantDoc có bản sao chính xác
giữa train/test; script cross-domain loại các bản test trùng khỏi đánh giá.
Manifest PlantVillage hiện có 38.940 train, 4.338 validation và 10.709 test;
285 ảnh bị cách ly do trùng group test, 33 ảnh train bị cách ly do exact
duplicate. Khoảng 12.886 ảnh không có leaf ID chính xác trong metadata nguồn
nên dùng fallback image ID; giữ giới hạn này trong báo cáo đánh giá.

Huấn luyện EfficientNet-B0 transfer learning, chọn checkpoint bằng validation
macro-F1, lưu history và metadata:

```powershell
.\.venv\Scripts\python.exe scripts\train.py `
  --manifest data\prepared\plantvillage\manifest.csv `
  --output models\plant_health.pt `
  --epochs 8 `
  --batch-size 32 `
  --architecture efficientnet_b0
```

Chỉ chạy test sau khi đã chốt checkpoint và ngưỡng trên validation:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py `
  --manifest data\prepared\plantvillage\manifest.csv `
  --split test `
  --checkpoint models\plant_health.pt
```

Đánh giá khả năng tổng quát hóa và từ chối lớp chưa hỗ trợ trên PlantDoc/test
(dùng validation để chọn threshold, không dùng test để tinh chỉnh):

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_plantdoc.py `
  --checkpoint models\plant_health.pt `
  --validation-manifest data\prepared\plantvillage\manifest.csv `
  --plantdoc-root data\plantdoc\test
```

Training xuất TorchScript cùng state dict PyTorch để inference Grad-CAM, loss/accuracy/macro-F1 từng epoch, best validation checkpoint,
metadata và history. Evaluation xuất accuracy, top-3, macro/weighted precision,
recall, F1, confusion matrix, classification report theo lớp và calibration
error vào `models/plant_health.evaluation.json`.
Cross-domain evaluation ghi ngưỡng confidence đã calibrate từ validation vào
`models/plant_health.threshold.json`; backend nạp ngưỡng này khi khởi động.

Checkpoint có sẵn trong repo được huấn luyện trước đây trên PlantDoc train 2.253
ảnh, 28 lớp; test 231 ảnh cho accuracy 47,2% và macro-F1 43,0%. Đây là checkpoint
nghiên cứu cũ, chưa phải model production được nghiệm thu. Không công bố hệ thống
là đã hoàn thành AI production cho đến khi chạy training/evaluation protocol mới,
đánh giá cross-domain/OOD và duyệt ngưỡng từ chối. Phân loại ảnh không đo được
mức độ bệnh học; giao diện hiện ghi mức độ là “Chưa đánh giá” thay vì suy diễn
mức nghiêm trọng từ confidence.

### Triển khai production

Frontend, API, PostgreSQL, migration, local/S3 storage và Docker Compose đã có.
Triển khai Internet vẫn cần domain/HTTPS, PostgreSQL managed, private object
storage, secrets ngẫu nhiên riêng cho môi trường và checkpoint đã được đánh giá.
Không dùng `.env.example` làm secrets production. Xem [DEPLOYMENT.md](DEPLOYMENT.md).

Nếu thiếu checkpoint, endpoint chẩn đoán trả HTTP 503; hệ thống không tạo kết quả giả.
