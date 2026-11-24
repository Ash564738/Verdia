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

Backend dùng Supabase PostgreSQL và Supabase Storage S3-compatible cho dữ liệu người dùng. Không lưu ảnh upload người dùng xuống đĩa local. SQLite chỉ dùng trong automated tests cô lập. Tạo tài khoản quản trị khi khởi động bằng
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
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
# Điền Supabase DATABASE_URL, bucket name và S3 settings theo phần bên dưới.
\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Kiểm tra backend:

```powershell
Invoke-RestMethod http://localhost:8000/health
Start-Process http://localhost:8000/docs
```

Health phải cho thấy `"database": "supabase_postgres"`,
`"storage": "supabase_s3"` và model đã load. Nếu chưa điền Supabase DSN/bucket,
backend sẽ dừng startup và ghi cụ thể lỗi cấu hình vào `data\logs\backend.log`.

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
if (!(Test-Path .env)) { Copy-Item .env.example .env }
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

Database và ảnh người dùng vẫn nằm trên Supabase khi container được tạo lại. Chỉ
log debug và model/dataset artifacts nằm trên filesystem project.

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

## Cấu hình Supabase bắt buộc

Backend tự đọc `.env` ở thư mục gốc. Các giá trị bí mật không được commit lên Git.
Hiện code dùng JWT riêng của ứng dụng; `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`,
`SUPABASE_SECRET_KEY`, `SUPABASE_JWKS_URL` và `NEXT_PUBLIC_SUPABASE_*` chưa được
code này sử dụng.

1. Trong Supabase Dashboard, vào **Connect** và sao chép PostgreSQL connection
   string. `DATABASE_URL` phải bắt đầu bằng `postgresql://` (hoặc `postgres://`),
   không phải URL HTTPS của project. Nếu mạng máy tính không dùng được IPv6, chọn
   **Session pooler** và sao chép đúng host/username/port Dashboard đưa ra. Đảm bảo
   chuỗi có `sslmode=require`; mã hóa ký tự đặc biệt trong password theo hướng dẫn
   của Supabase.
2. Trong **Storage**, tạo bucket mới và chọn **Private**, ví dụ `plant-care-private`.
   `S3_BUCKET` chính là tên bucket này, không phải endpoint, project URL hay access
   key. Tên bucket là giá trị bạn đặt khi tạo.
3. Trong cài đặt S3 của Storage, bật S3 protocol nếu Dashboard yêu cầu; sao chép
   chính xác endpoint, region, S3 Access Key ID và S3 Secret Access Key vào
   `S3_ENDPOINT`, `S3_REGION`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`. S3 keys khác với
   `SUPABASE_SECRET_KEY` và database password. S3 keys có quyền rộng, chỉ để ở
   backend `.env`; không đưa vào frontend.
4. Đặt `STORAGE_BACKEND=s3`. Khi thiếu PostgreSQL DSN, bucket, quyền truy cập hoặc
   endpoint sai, backend dừng với lỗi cấu hình cụ thể; không tự chuyển sang SQLite
   hay local upload.

`DATABASE_PATH` và `LOCAL_STORAGE_ROOT` không còn được dùng cho dữ liệu ứng dụng.
Ảnh cây/chẩn đoán được lưu trong bucket riêng tư; PostgreSQL chỉ giữ storage key.
Backend kiểm tra quyền sở hữu trước khi cấp signed URL có thời hạn. Log không ghi
password, token, S3 keys hay nội dung ảnh.

Tài liệu: [Supabase database connection strings](https://supabase.com/docs/guides/database/connecting-to-postgres),
[Storage S3 authentication](https://supabase.com/docs/guides/storage/s3/authentication),
[private buckets](https://supabase.com/docs/guides/storage/buckets/fundamentals).

## Dataset, train, validate, test và thay model cho API

### 1. Mở PowerShell và dùng đúng Python trong `.venv`

Các lệnh bên dưới chạy từ thư mục gốc `E:\Verdia`. Luôn gọi
`\.venv\Scripts\python.exe`; nếu chỉ gõ `python`, có thể vô tình train bằng
một phiên bản Torch khác với phiên bản backend đang dùng.

```powershell
cd E:\Verdia
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import torch, torchvision; print('torch', torch.__version__, 'torchvision', torchvision.__version__, 'cuda', torch.cuda.is_available())"
```

Nếu tạo môi trường mới, cài Git và Python trước, rồi chạy:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`requirements.txt` ghim PyTorch/torchvision cho CPU. Máy hiện tại báo CUDA
`False`, vì vậy train EfficientNet có thể mất hàng giờ. Nếu máy có NVIDIA GPU,
chọn bản Windows/Pip/CUDA phù hợp trên [PyTorch Get Started](https://pytorch.org/get-started/locally/),
cài torch và torchvision khớp nhau trong `.venv`, rồi kiểm tra lại CUDA.

### 2. Tải dữ liệu nguồn

PlantVillage Color là dữ liệu train chính và PlantDoc dùng để đánh giá ngoài miền.
Lệnh tải bỏ qua dataset đã đủ ảnh để tránh force-checkout ghi đè file hiện có.

```powershell
.\.venv\Scripts\python.exe scripts\download_datasets.py
```

Kiểm tra phải có ảnh trong `data\plantvillage\raw\color`,
`data\plantdoc\train` và `data\plantdoc\test`. Nguồn Cassava/Rice hiện chưa
được cấu hình trong script nên các lệnh bên dưới không đánh giá hai bộ OOD đó.

### 3. Audit ảnh và split

```powershell
.\.venv\Scripts\python.exe scripts\audit_datasets.py
.\.venv\Scripts\python.exe scripts\audit_perceptual_hashes.py
.\.venv\Scripts\python.exe scripts\prepare_training_data.py
```

Audit exact hash phát hiện ảnh hỏng và ảnh trùng. pHash chạy lâu hơn, chỉ ghi các
cặp ứng viên để rà soát; script không tự xóa ảnh. Tạo manifest giữ official
PlantVillage test nguyên vẹn, rồi chia các group từ official train thành train
và validation. Hiện tại manifest ghi 38.940 train, 4.338 validation, 10.709
official test; 285 ảnh bị cách ly vì group trùng test và 33 ảnh vì exact
duplicate. Có 12.886 hàng phải dùng fallback image ID do leaf-map thiếu ID, nên
khả năng đảm bảo group độc lập bị hạn chế ở các hàng đó. Kiểm tra
`data\prepared\plantvillage\manifest.csv` trước khi train.

### 4. Train model từ đầu

Dừng backend trước khi thay checkpoint đang được API nạp. Lệnh dưới đây train
EfficientNet-B0 8 epoch, freeze backbone 2 epoch đầu và chọn checkpoint có
validation macro-F1 tốt nhất. Đây là full run; đừng đóng cửa sổ khi train.

```powershell
.\.venv\Scripts\python.exe scripts\train.py `
  --manifest data\prepared\plantvillage\manifest.csv `
  --output models\plant_health.pt `
  --epochs 8 `
  --freeze-epochs 2 `
  --batch-size 32 `
  --image-size 224 `
  --architecture efficientnet_b0
```

Train dùng augmentation chỉ trên train, ImageNet normalization và seed 42.
Kết thúc thành công phải có `complete: true` trong `.training.json` và đủ các file
`plant_health.pt`, `.pth`, `.labels.txt`, `.metadata.json`, `.training.json`.
`training.json` có `completed_epochs`, `requested_epochs` và `complete`; chỉ
chấp nhận là full run khi `complete` là `true`. Nếu muốn kiểm tra pipeline nhanh,
có thể chạy smoke run nhanh với mẫu giới hạn đều theo lớp; kết quả đó chỉ để kiểm
tra pipeline, không thay thế huấn luyện đầy đủ:

```powershell
\.venv\Scripts\python.exe scripts\train.py `
  --manifest data\prepared\plantvillage\manifest.csv `
  --output models\smoke_mobilenet.pt `
  --epochs 2 `
  --freeze-epochs 1 `
  --batch-size 64 `
  --image-size 160 `
  --architecture mobilenet_v3_small `
  --max-per-class 50 `
  --log-interval 10
```

Lệnh smoke lấy tối đa 50 ảnh/class cho train và validation, tối đa 1.900 ảnh mỗi
split. Không dùng kết quả này để kết luận model tốt hoặc thay checkpoint chính.
Giảm image size, epoch hoặc đổi kiến trúc có thể giảm chất lượng. Không chọn cấu
hình bằng test.

Train log ghi batch, split, running loss, elapsed và ETA vào `data\logs\training.log`
và console. Mặc định ghi mỗi 50 batch; thêm `--log-interval 10` để cập nhật thường
xuyên hơn. `.training.json` ghi số epoch hoàn tất để phân biệt run bị dừng giữa
chừng với run hoàn tất.

Theo dõi run đang chạy bằng file trạng thái (nhấn `Ctrl+C` chỉ dừng vòng theo dõi):

```powershell
while ($true) {
  $s = Get-Content models\plant_health.training.json -Raw | ConvertFrom-Json
  $last = @($s.history)[-1]
  "completed={0}/{1} complete={2} val_macro_f1={3:N4}" -f $s.completed_epochs, $s.requested_epochs, $s.complete, $last.validation_macro_f1
  Start-Sleep -Seconds 30
}
```

### 5. Đánh giá validation, rồi test

Validation được dùng để chọn checkpoint; đánh giá validation bổ sung bằng:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py `
  --manifest data\prepared\plantvillage\manifest.csv `
  --split validation `
  --checkpoint models\plant_health.pt
```

Khi đã chốt checkpoint và không còn thay model/hyperparameter, chạy official
test đúng một lần:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py `
  --manifest data\prepared\plantvillage\manifest.csv `
  --split test `
  --checkpoint models\plant_health.pt
```

Hai báo cáo JSON chứa accuracy, macro/weighted precision-recall-F1, top-3,
confusion matrix, per-class metrics và ECE. Không dùng test để chọn lại model,
threshold hoặc augmentation. Đánh giá PlantDoc sau đó bằng:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_plantdoc.py `
  --checkpoint models\plant_health.pt `
  --validation-manifest data\prepared\plantvillage\manifest.csv `
  --plantdoc-root data\plantdoc\test
```

PlantDoc mapping hiện chỉ là crosswalk bảo thủ; xem
`ml\configs\plantdoc_label_mapping.json`. Không diễn giải các nhãn unmapped
thành chẩn đoán đúng/sai closed-set. PlantDoc test cũng có exact duplicate giữa
train/test; báo cáo loại các bản test đó.

### 6. Dùng checkpoint vừa train trong backend

Backend nạp model một lần lúc khởi động. Sau khi train xong, dừng API bằng
`Ctrl+C`, rồi khởi động lại:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Mở `http://127.0.0.1:8000/health` để xác nhận `database=supabase_postgres` và
`storage=supabase_s3`. `http://127.0.0.1:8000/api/v1/model/info` hiển thị model,
checkpoint SHA-256, class order, threshold, trạng thái train và metrics test.
Sau đó mở `http://127.0.0.1:8000/docs`, đăng nhập để lấy token, rồi gửi ảnh JPEG/PNG/WebP
vào `POST /api/v1/diagnoses/predict` ở field `file`. Kiểm tra response `model`,
`status`, `confidence` và `top_predictions`; `uncertain` nghĩa là API đang abstain,
không phải chẩn đoán bệnh. `/health` xác nhận backend và database khởi động được,
nhưng không chứng minh model chính xác.

### Debug log và kiểm tra lỗi

- `data\logs\backend.log`: mỗi HTTP request có request ID, endpoint, status và
  thời gian xử lý; kèm traceback lỗi database/storage.
- `data\logs\diagnosis.log`: checksum ảnh, kết quả validate ảnh, dimensions/mode,
  top-k class/confidence, threshold, trạng thái abstain và thời gian inference.
- `data\logs\training.log`: batch/epoch, loss, ETA, device và phiên bản Torch.
  Log không chứa bytes ảnh, token hay credentials.

Theo dõi trực tiếp:

```powershell
Get-Content data\logs\backend.log -Tail 100 -Wait
Get-Content data\logs\diagnosis.log -Tail 100 -Wait
Get-Content data\logs\training.log -Tail 100 -Wait
```

Response có header `X-Request-ID`; tìm ID đó trong các log để nối các bước xử lý
của một request. `GET /api/v1/admin/diagnostics` yêu cầu tài khoản ADMIN và trả
trạng thái DB, cấu hình Storage cùng model runtime mà không lộ key/password. Nếu
app dừng lúc startup, tìm `startup_configuration_invalid` trong `backend.log`.

### Trạng thái model

Trạng thái run mới nhất nằm trong `models\plant_health.training.json`; không lấy
metrics từ báo cáo cũ nếu checkpoint đã được train lại. Khi tài liệu này được cập
nhật, run `.venv` gần nhất đã hoàn thành 2/8 epoch, validation macro-F1 0,9409 và
`complete=false`; chưa có test result cho checkpoint đang train. Chỉ chạy test và
khởi động lại API sau khi run có `complete=true`. Metrics trước đó trong
[MODEL_EVALUATION.md](MODEL_EVALUATION.md) là lịch sử của checkpoint cũ.

Phân loại ảnh không đo được mức độ bệnh học. Nếu hai ảnh khác nhau cùng cho đúng
một kết quả, xác minh chúng có thực sự là hai file khác nhau, kiểm tra
`top_predictions`, rồi đánh giá lại bằng bộ ảnh test độc lập; không kết luận chỉ
từ log hai request.

### Triển khai production

Frontend, API, Supabase PostgreSQL, Supabase Storage và Docker Compose đã có.
Triển khai Internet vẫn cần domain/HTTPS, PostgreSQL managed, private object
storage, secrets ngẫu nhiên riêng cho môi trường và checkpoint đã được đánh giá.
Không dùng `.env.example` làm secrets production. Xem [DEPLOYMENT.md](DEPLOYMENT.md).

Nếu thiếu checkpoint, endpoint chẩn đoán trả HTTP 503; hệ thống không tạo kết quả giả.

## Khac phuc Supabase DNS va resume training

Neu log bao `getaddrinfo failed` voi host `db.<project>.supabase.co`, day la loi DNS/ket noi mang truoc khi PostgreSQL kiem tra password. Mot so mang Windows/ISP khong co IPv6, trong khi direct database host co the chi tra AAAA. Mo Supabase Dashboard > Connect, copy nguyen URI cua **Session pooler** (hoac pooler ma dashboard khuyen nghi), dat vao `DATABASE_URL`; khong tu ghep host/user/port. URI pooler thuong co username rieng gan voi project ref. Backend da bat `sslmode=require`; restart uvicorn sau khi sua `.env`. Khong gui URI co password len chat hay commit `.env`.

Loi start truoc day xay ra o epoch 3 sau khi epoch 2 da duoc luu. Checkpoint tot nhat hien tai la epoch 2, validation macro-F1 0.9409. De tiep tuc tu checkpoint, tranh tai lai pretrained weights va khong chay lai 2 epoch dau:

```powershell
.\.venv\Scripts\python.exe scripts\train.py `
  --manifest data\prepared\plantvillage\manifest.csv `
  --output models\plant_health.pt `
  --epochs 8 `
  --freeze-epochs 8 `
  --batch-size 32 `
  --image-size 224 `
  --architecture efficientnet_b0 `
  --resume
```

`--resume` nap checkpoint tot nhat hien co, bao gom weight tu epoch 2 va metrics lich su, roi chay cac epoch con lai. `--freeze-epochs 8` giu EfficientNet backbone dong bang va cap nhat chi classifier-head; day la lua chon nhanh hon tren CPU nhung khong tuong duong voi fine-tune toan backbone. Neu muon fine-tune tiep nhu ke hoach ban dau, dung `--freeze-epochs 2`; se chay cham hon nhieu tren CPU. Ket qua cuoi cung van phai danh gia tren test split rieng, khong dung validation F1 de tuyen bo test performance.

May dang dung PyTorch ban CPU (`torch.cuda.is_available() == False`); 2 epoch dau mat khoang 23 phut. Tang batch size khong dam bao nhanh hon tren CPU. Hieu qua nhat la train tren may co NVIDIA CUDA, hoac dung head-only lenh tren. De xem GPU:

```powershell
nvidia-smi
.\.venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

Neu backend bat dau ghi log qua chi tiet cua boto3, phien ban moi gioi han log botocore de tranh ghi Authorization/signature vao file. Dung `.env` local co quyen truy cap han che va rotate credentials da tung duoc chia se cong khai.
