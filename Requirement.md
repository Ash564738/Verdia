https://github.com/pkparthk/Plant-Disease-Detection.git
https://github.com/zawrabh/Plant-Disease-Detection.git
https://github.com/manthan89-py/Plant-Disease-Detection.git
https://github.com/pratikkayal/PlantDoc-Dataset.git
https://github.com/spMohanty/PlantVillage-Dataset.git
ĐẶC TẢ ĐỒ ÁN CHUYÊN NGÀNH 2
Hệ thống AI nhận diện bệnh và phân tích tình trạng sức khỏe cây trồng từ hình ảnh
Tôi đề xuất phát triển đề tài theo hướng một nền tảng Smart Plant Care – AI Plant Disease Detection, thay vì chỉ làm một website tải ảnh lên rồi trả về tên bệnh.

Sản phẩm cuối cùng sẽ là một hệ thống web đa nền tảng, sử dụng trí tuệ nhân tạo để nhận diện cây trồng, phân loại bệnh qua hình ảnh lá, đánh giá mức độ rủi ro, đưa ra hướng dẫn chăm sóc, quản lý lịch sử kiểm tra và theo dõi tình trạng cây trồng theo thời gian.

Điểm quan trọng là phải kết hợp được ba phần:
1. AI / Computer Vision: Huấn luyện và triển khai mô hình học sâu nhận diện bệnh.
2. Web Application: Xây dựng nền tảng hoàn chỉnh, có tài khoản, quản lý cây, lịch sử, báo cáo và trang quản trị.
3. Plant Health Analytics: Phân tích kết quả, theo dõi diễn biến và đề xuất phương án chăm sóc dựa trên dữ liệu.
Mục tiêu là tạo ra một sản phẩm có thể trình diễn được trong buổi bảo vệ đồ án, có mô hình AI thực sự, có quy trình đánh giá khoa học và có giao diện sử dụng được trên cả laptop lẫn điện thoại.

1. Phân tích các repository và dataset được cung cấp
Các nguồn bạn đưa ra có thể được chia thành hai nhóm: dự án tham khảo kiến trúc và dự án cung cấp dữ liệu huấn luyện.
1.1. Các dự án tham khảo
1. pkparthk/Plant-Disease-Detection
Nên tham khảo kiến trúc chính
FastAPI + React + TypeScript

Đây là nguồn tham khảo phù hợp nhất cho kiến trúc hệ thống hiện đại. Dự án có frontend React, backend FastAPI, mô hình AI, notebook huấn luyện và hỗ trợ nhiều bộ thực thi mô hình như TensorFlow, PyTorch, ONNX. README cũng mô tả chức năng tải ảnh, dự đoán bệnh, trả về confidence score và triển khai cloud. 

GitHub

Link: GitHub Repository

2. manthan89-py/Plant-Disease-Detection
Nên tham khảo mô hình AI
PyTorch + CNN + Flask

Dự án phân loại 39 lớp bệnh và cây trồng bằng CNN, sử dụng PlantVillage. Có mã huấn luyện, model đã lưu và ứng dụng Flask để nhận ảnh và trả kết quả. Phù hợp để tìm hiểu cách triển khai mô hình đã huấn luyện vào ứng dụng thực tế. 

GitHub

Link: GitHub Repository

3. zawrabh/Plant-Disease-Detection
Tham khảo triển khai đơn giản
CNN + TensorFlow/Keras + Streamlit

Dự án sử dụng CNN để phân loại bệnh, lưu trọng số ở định dạng .h5 và cung cấp giao diện Streamlit để người dùng tải ảnh. Thích hợp để nghiên cứu quy trình inference, nhưng không nên lấy nguyên kiến trúc Streamlit làm nền tảng chính nếu mục tiêu là web đa nền tảng nhiều chức năng. 

GitHub

Link: GitHub Repository

1.2. Các bộ dữ liệu
PlantVillage Dataset








mdpi.com


Dataset chính để huấn luyện ban đầu
- Khoảng 54.306 hình ảnh.
- 14 loại cây trồng.
- 26 bệnh.
- Có ảnh RGB, ảnh grayscale và ảnh đã tách nền.
- Bộ dữ liệu Hugging Face có cấu hình chia train/test và thông tin nhóm lá nhằm hạn chế rò rỉ dữ liệu giữa các tập. 
  
  GitHub+1
Link: PlantVillage Dataset

PlantDoc Dataset








frontiersin.org


Dataset bổ sung để kiểm tra thực tế
- Bộ dữ liệu phục vụ bài toán nhận diện bệnh cây trồng từ hình ảnh thực tế.
- Có cấu trúc train/test.
- Ảnh có bối cảnh tự nhiên hơn, giúp nghiên cứu khả năng tổng quát hóa của mô hình.
- Repository công bố theo giấy phép CC BY 4.0. 
  
  GitHub
Link: PlantDoc Dataset

1.3. Chiến lược sử dụng các nguồn
Không nên gộp tất cả code từ năm repository thành một dự án. Nên tự xây dựng một hệ thống thống nhất, tận dụng từng nguồn theo mục đích:
Nguồn	Cách sử dụng
pkparthk	Tham khảo kiến trúc React + FastAPI
manthan89-py	Tham khảo CNN/PyTorch và quy trình inference
zawrabh	Tham khảo ứng dụng nhận diện cơ bản
PlantVillage	Huấn luyện mô hình phân loại ban đầu
PlantDoc	Kiểm tra khả năng hoạt động với ảnh thực tế

Lưu ý khoa học: PlantVillage có nhiều ảnh được chụp trong điều kiện tương đối kiểm soát. Mô hình đạt Accuracy cao trên bộ dữ liệu này không đồng nghĩa có thể đạt kết quả tương tự khi người dùng chụp lá ngoài vườn. Vì vậy, cần đánh giá riêng trên PlantDoc hoặc bộ ảnh thực địa độc lập. Không được trộn ảnh test vào train hoặc dùng các ảnh gần như trùng nhau ở hai tập. 

GitHub+1

2. Định hướng sản phẩm cần xây dựng
2.1. Tên đề tài đề xuất
Tiếng Việt:

Xây dựng hệ thống ứng dụng trí tuệ nhân tạo hỗ trợ nhận diện bệnh và phân tích tình trạng sức khỏe cây trồng thông qua hình ảnh lá cây.

Tiếng Anh:

AI-Based Plant Disease Detection and Plant Health Analysis System.

Tên sản phẩm: Smart Plant Care AI.
2.2. Mục tiêu của hệ thống
Hệ thống phục vụ ba nhóm người dùng chính:
Đối tượng	Mục đích
Người trồng cây	Kiểm tra bệnh, theo dõi cây và nhận hướng dẫn chăm sóc
Người làm nông nghiệp	Quản lý nhiều cây, nhiều khu vực trồng và theo dõi tình trạng
Quản trị viên / chuyên gia	Quản lý dữ liệu bệnh, người dùng, mô hình AI và kiểm duyệt phản hồi

Hệ thống không chỉ dự đoán nhãn bệnh mà phải cung cấp được thông tin có ích sau khi dự đoán.

Ví dụ, người dùng chụp một chiếc lá cà chua. Hệ thống trả về:
Kết quả phân tích AI
Có dấu hiệu bệnh









gardenuk.co.uk


Tomato – Early Blight
Bệnh đốm vòng sớm trên lá cà chua · Ví dụ minh họa kết quả
Độ tin cậy mô hình
94.8%


Mức độ biểu hiện
Trung bình



Thông tin bệnh
- Tác nhân thường gặp: nấm Alternaria solani.
- Biểu hiện: đốm nâu, thường có vòng đồng tâm.
- Vị trí thường gặp: lá già và lá phía dưới.
Hướng dẫn chăm sóc đề xuất
1. Theo dõi các lá xuất hiện đốm mới.
2. Loại bỏ lá bị bệnh nặng bằng dụng cụ sạch.
3. Hạn chế để lá bị ẩm kéo dài.
4. Theo dõi khả năng lan rộng và tham khảo cán bộ chuyên môn khi bệnh diễn biến nghiêm trọng.
Đây là dữ liệu minh họa giao diện, không phải kết quả inference từ mô hình đang chạy.

2.3. Phạm vi nhận diện ban đầu
Tôi khuyên không nên cố gắng nhận diện tất cả cây trồng trên thế giới ngay từ đầu.

Giai đoạn đầu nên sử dụng các lớp có sẵn từ PlantVillage, đặc biệt tập trung vào:
- Cà chua (Tomato).
- Khoai tây (Potato).
- Ngô (Corn).
- Táo (Apple).
- Nho (Grape).
Sau đó mở rộng các loại cây khác khi đã chuẩn hóa được dữ liệu và nhãn bệnh.

Có thể triển khai mô hình khoảng 39 lớp phân loại theo cách tiếp cận của repository manthan89-py, nhưng cần kiểm tra lại danh sách class và dữ liệu thực tế trước khi huấn luyện. 

GitHub+1


3. Kiến trúc tổng thể của hệ thống
Đề xuất sử dụng kiến trúc Frontend – Backend – AI Model – Database.
3.1. Công nghệ sử dụng
Đây là bộ công nghệ tôi khuyên dùng cho đồ án:
Thành phần	Công nghệ	Vai trò
Frontend	React + TypeScript	Giao diện web
Build tool	Vite	Phát triển và build frontend
UI	Tailwind CSS + shadcn/ui	Thiết kế giao diện
Routing	React Router	Điều hướng trang
Data fetching	TanStack Query	Quản lý dữ liệu API
Responsive/PWA	CSS responsive + PWA	Laptop và điện thoại
Backend	Python + FastAPI	Xử lý nghiệp vụ và API
AI	PyTorch + torchvision	Huấn luyện và inference
Image processing	OpenCV + Pillow	Tiền xử lý ảnh
Database	PostgreSQL	Lưu trữ dữ liệu
ORM	SQLAlchemy + Alembic	Truy vấn và quản lý schema
Image storage	Local storage khi phát triển, S3-compatible khi triển khai	Lưu ảnh
Charts	Recharts	Biểu đồ thống kê
Deployment	Docker	Đóng gói và triển khai

Kiến trúc React + TypeScript và FastAPI cũng là hướng được repository pkparthk sử dụng. Repository này còn mô tả notebook huấn luyện, API dự đoán, kiểm thử và xử lý nhiều định dạng mô hình. 

GitHub+1

Tại sao chọn kiến trúc này?
- React giúp xây dựng giao diện chuyên nghiệp và thích ứng nhiều màn hình.
- FastAPI tương thích tốt với Python và các thư viện học sâu.
- PyTorch thuận tiện cho quá trình huấn luyện, đánh giá và xuất mô hình.
- PostgreSQL giúp quản lý tài khoản, cây trồng, lịch sử chẩn đoán và dữ liệu bệnh.
- PWA cho phép người dùng cài website lên màn hình điện thoại như một ứng dụng.
Không cần xây dựng hai ứng dụng riêng biệt cho Android và laptop. Một frontend responsive có thể phục vụ cả hai. Trong phạm vi đồ án, PWA là lựa chọn phù hợp hơn việc phát triển ứng dụng native Android/iOS.
3.2. Sơ đồ kiến trúc
#chatgpt-mermaid-_r_bk_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_bk_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_bk_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_bk_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_bk_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_bk_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_bk_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_bk_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_bk_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_bk_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_bk_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bk_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bk_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_bk_ p{margin:0;}#chatgpt-mermaid-_r_bk_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_bk_ .label text,#chatgpt-mermaid-_r_bk_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ .node rect,#chatgpt-mermaid-_r_bk_ .node circle,#chatgpt-mermaid-_r_bk_ .node ellipse,#chatgpt-mermaid-_r_bk_ .node polygon,#chatgpt-mermaid-_r_bk_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-_r_bk_ .rough-node .label text,#chatgpt-mermaid-_r_bk_ .node .label text,#chatgpt-mermaid-_r_bk_ .image-shape .label,#chatgpt-mermaid-_r_bk_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_bk_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_bk_ .rough-node .label,#chatgpt-mermaid-_r_bk_ .node .label,#chatgpt-mermaid-_r_bk_ .image-shape .label,#chatgpt-mermaid-_r_bk_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_bk_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_bk_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bk_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bk_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_bk_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_bk_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_bk_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_bk_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_bk_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_bk_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_bk_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_bk_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bk_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_bk_ .icon-shape,#chatgpt-mermaid-_r_bk_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_bk_ .icon-shape p,#chatgpt-mermaid-_r_bk_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_bk_ .icon-shape .label rect,#chatgpt-mermaid-_r_bk_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_bk_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_bk_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_bk_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-_r_bk_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_bk_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_bk_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_bk_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bk_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_bk_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_bk_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_bk_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bk_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-_r_bk_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_bk_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bk_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_bk_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_bk_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bk_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_bk_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bk_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_bk_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_bk_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_bk_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_bk_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-_r_bk_ .node rect,#chatgpt-mermaid-_r_bk_ .node circle,#chatgpt-mermaid-_r_bk_ .node ellipse,#chatgpt-mermaid-_r_bk_ .node polygon,#chatgpt-mermaid-_r_bk_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_bk_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_bk_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_bk_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_bk_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bk_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Người dùngResponsive Web / PWAReact + TypeScriptFastAPI BackendAuthentication & AuthorizationPlant ManagementDiagnosis ServiceHealth AnalyticsPostgreSQLImage StorageImage Validation &PreprocessingPyTorch AI ModelGrad-CAM ExplainabilityDisease Knowledge BaseAdmin Management





3.3. Nguyên tắc hoạt động
Frontend không trực tiếp thực hiện huấn luyện hoặc chạy các thuật toán AI nặng.

Frontend chịu trách nhiệm:
- Nhận ảnh từ người dùng.
- Gửi ảnh đến backend.
- Hiển thị kết quả.
- Quản lý trạng thái và lịch sử.
- Hiển thị biểu đồ và thông tin.
Backend chịu trách nhiệm:
- Xác thực người dùng.
- Kiểm tra ảnh.
- Gọi mô hình AI.
- Truy xuất thông tin bệnh.
- Tính toán chỉ số phân tích.
- Lưu dữ liệu và trả kết quả về frontend.
AI Service chịu trách nhiệm:
- Tiền xử lý ảnh.
- Phân loại cây trồng và bệnh.
- Tính độ tin cậy.
- Tạo giải thích trực quan.
- Trả về kết quả có cấu trúc.
Database quản lý toàn bộ thông tin cần thiết để hệ thống vận hành.

4. Các chức năng cần xây dựng
Tôi chia chức năng thành 3 khu vực: người dùng, hệ thống AI và quản trị viên.
4.1. Khu vực công khai








farm-fresh-connect-81.lovable.app


Trang chủ cần có:
- Giới thiệu Smart Plant Care AI.
- Giới thiệu khả năng nhận diện bệnh.
- Thống kê số loại cây, số bệnh được hỗ trợ.
- Hướng dẫn sử dụng hệ thống.
- Minh họa quy trình phân tích hình ảnh.
- Danh sách một số bệnh phổ biến.
- Nút bắt đầu kiểm tra cây trồng.
- Đăng nhập và đăng ký tài khoản.
Cần thiết kế trang chủ hiện đại, có hình ảnh cây xanh, biểu đồ và các thành phần trực quan. Không nên làm trang chủ chỉ có một ô tải ảnh.
4.2. Đăng ký và đăng nhập
Các chức năng:
- Đăng ký tài khoản bằng email.
- Đăng nhập.
- Đăng xuất.
- Quên mật khẩu.
- Đổi mật khẩu.
- Cập nhật hồ sơ cá nhân.
- Phân quyền USER và ADMIN.
- Bảo vệ các trang yêu cầu đăng nhập.
Có thể bổ sung xác minh email và đăng nhập Google ở giai đoạn mở rộng.
4.3. Dashboard người dùng








behance.net


Sau khi đăng nhập, người dùng vào Dashboard.

Thông tin cần hiển thị:
Thành phần	Nội dung
Tổng số cây	Số cây đã thêm vào hệ thống
Tổng lượt kiểm tra	Tổng số lần chẩn đoán
Cây khỏe mạnh	Số cây có kết quả khỏe mạnh
Cây có dấu hiệu bệnh	Số cây có kết quả bất thường
Lần kiểm tra gần nhất	Thời gian và kết quả
Hoạt động gần đây	Danh sách các lần kiểm tra

Biểu đồ:
- Số lần kiểm tra theo thời gian.
- Tỷ lệ cây khỏe và cây có dấu hiệu bệnh.
- Các loại bệnh xuất hiện thường xuyên.
- Tỷ lệ bệnh theo từng loại cây.
Có khu vực thông báo:
- Cây cần kiểm tra lại.
- Kết quả mới có nguy cơ cao.
- Cây lâu chưa được theo dõi.
- Lịch chăm sóc sắp đến hạn.
4.4. Chức năng AI – Kiểm tra bệnh qua hình ảnh








devpost.com


Đây là chức năng quan trọng nhất của đồ án.

Người dùng có thể:
1. Chọn ảnh từ thiết bị.
2. Chụp ảnh trực tiếp bằng camera điện thoại.
3. Kéo thả ảnh vào giao diện trên máy tính.
4. Xem trước ảnh.
5. Cắt ảnh hoặc chọn lại ảnh.
6. Nhập loại cây nếu đã biết.
7. Chọn cây đã có trong danh sách quản lý.
8. Nhấn nút Phân tích bằng AI.
Kiểm tra chất lượng ảnh trước khi phân tích

Backend cần xác thực:
- Định dạng JPG, JPEG, PNG hoặc WEBP.
- Dung lượng file trong giới hạn.
- Kích thước ảnh hợp lệ.
- File thực sự là hình ảnh.
- Ảnh không bị lỗi hoặc giải mã thất bại.
- Ảnh không quá mờ hoặc quá tối.
- Lá cây có đủ diện tích hiển thị.
Nếu ảnh không đạt yêu cầu, hệ thống phải thông báo và đề nghị chụp lại. Không nên cố dự đoán mọi loại ảnh mà người dùng gửi lên.

Kết quả dự đoán

Hệ thống trả về:
- Tên cây.
- Tên bệnh.
- Trạng thái khỏe mạnh hoặc có dấu hiệu bệnh.
- Confidence score.
- Top 3 dự đoán.
- Mô tả triệu chứng.
- Nguyên nhân thường gặp.
- Điều kiện phát triển bệnh.
- Hướng dẫn xử lý.
- Phương pháp phòng ngừa.
- Khuyến nghị kiểm tra lại.
Ví dụ JSON kết quả:
{
  "plant": {
    "name": "Tomato",
    "name_vi": "Cà chua"
  },
  "disease": {
    "code": "tomato_early_blight",
    "name": "Early Blight",
    "name_vi": "Bệnh đốm vòng sớm"
  },
  "prediction": {
    "status": "disease_detected",
    "confidence": 0.948,
    "top_predictions": [
      {
        "class": "Tomato___Early_blight",
        "confidence": 0.948
      },
      {
        "class": "Tomato___Late_blight",
        "confidence": 0.032
      },
      {
        "class": "Tomato___healthy",
        "confidence": 0.020
      }
    ]
  },
  "model": {
    "name": "efficientnet_b0",
    "version": "1.0.0"
  }
}


Đây là cấu trúc dữ liệu đề xuất, không phải kết quả mô hình thực tế.

Xử lý trường hợp AI không chắc chắn

Rất quan trọng: Không được buộc AI đưa ra tên bệnh khi confidence thấp.

Ví dụ:
- Confidence từ 85% trở lên: kết quả có độ tin cậy cao theo ngưỡng cấu hình.
- Confidence từ 60% đến dưới 85%: kết quả cần kiểm tra thêm.
- Confidence dưới 60%: chưa thể đưa ra kết luận.
Các ngưỡng này chỉ là giá trị khởi tạo minh họa. Phải điều chỉnh theo kết quả validation, calibration và đánh giá thực tế. Confidence score không đồng nghĩa với xác suất bệnh thực sự của cây.

Nếu ảnh không thuộc các lớp đã huấn luyện hoặc không phải ảnh lá phù hợp, cần có trạng thái unknown hoặc unsupported, thay vì gán nhầm một bệnh quen thuộc.
4.5. Phân tích tình trạng sức khỏe cây trồng








dribbble.com


Đây là chức năng giúp đồ án khác biệt với ứng dụng phân loại bệnh thông thường.

Hệ thống cần có trang Plant Health Analysis.

Các nội dung phân tích:

A. Tình trạng hiện tại
- Tình trạng lá được đánh giá.
- Bệnh được nhận diện.
- Độ tin cậy của kết quả.
- Mức độ biểu hiện triệu chứng trên ảnh (nếu có module đánh giá).
- Nguy cơ cần theo dõi.
- Khuyến nghị xử lý.
B. Theo dõi sức khỏe theo thời gian

Hệ thống lưu kết quả nhiều lần của cùng một cây.

Ví dụ:
Thời gian	Kết quả	Tình trạng biểu hiện
01/11	Không phát hiện bệnh	Bình thường
05/11	Có dấu hiệu đốm lá	Nhẹ
10/11	Đốm lá tiếp tục xuất hiện	Trung bình

Từ đó hệ thống tạo biểu đồ diễn biến và cảnh báo khả năng tình trạng đang xấu đi.

Chỉ được so sánh tiến triển bệnh khi các ảnh thực sự thuộc cùng cây hoặc cùng đối tượng theo dõi. Không nên so sánh hai hình ảnh bất kỳ rồi kết luận bệnh đã tiến triển.

C. Đánh giá mức độ biểu hiện

Có thể xây dựng thêm thuật toán phân tích vùng lá:
- Xác định vùng lá.
- Xác định những vùng có dấu hiệu tổn thương.
- Ước tính tỷ lệ diện tích bất thường trên vùng lá.
- Phân loại mức độ biểu hiện: nhẹ, trung bình, nặng.
Ví dụ:
Tỷ lệ diện tích bất thường	Mức biểu hiện
0–5%	Nhẹ
Trên 5–20%	Trung bình
Trên 20%	Nặng

Các mốc này chỉ là ví dụ để thiết kế giao diện và cần được hiệu chỉnh bằng dữ liệu được gán nhãn. Không được sử dụng trực tiếp làm tiêu chuẩn bệnh học.

Lưu ý rất quan trọng về mặt chuyên môn: Một mô hình phân loại ảnh lá không thể tự xác định toàn bộ sức khỏe của cây, dinh dưỡng đất, tình trạng rễ hay mức độ bệnh trên cả cây. Muốn xây dựng đánh giá sức khỏe đáng tin cậy, cần bổ sung phân đoạn vùng lá/vùng bệnh, hình ảnh nhiều lá, dữ liệu quan sát và lịch sử theo dõi. Vì vậy, trong báo cáo nên gọi đây là chỉ số đánh giá tình trạng dựa trên dữ liệu quan sát, không tuyên bố là phép đo sức khỏe sinh học chính xác.
4.6. Quản lý cây trồng của người dùng
Người dùng có thể thêm cây vào hệ thống.

Thông tin mỗi cây:
- Tên cây do người dùng đặt.
- Loại cây.
- Giống cây (tùy chọn).
- Ngày bắt đầu theo dõi.
- Khu vực trồng.
- Ghi chú.
- Ảnh đại diện.
- Trạng thái theo dõi.
Ví dụ, một người dùng có thể quản lý ba cây cà chua khác nhau và theo dõi từng cây độc lập.

Các thao tác:
- Thêm cây.
- Chỉnh sửa thông tin.
- Xóa cây.
- Xem chi tiết.
- Xem lịch sử chẩn đoán.
- So sánh kết quả qua các lần kiểm tra.
4.7. Nhật ký và lịch sử chẩn đoán
Mỗi lần AI phân tích phải được lưu thành một bản ghi.

Thông tin bao gồm:
- Ảnh gốc.
- Thời gian phân tích.
- Người thực hiện.
- Loại cây.
- Kết quả dự đoán.
- Top 3 kết quả.
- Confidence score.
- Model version.
- Khuyến nghị tương ứng.
- Ghi chú của người dùng.
Chức năng:
- Xem lại kết quả cũ.
- Tìm kiếm theo tên cây.
- Lọc theo tình trạng bệnh.
- Lọc theo thời gian.
- Xem chi tiết lần kiểm tra.
- Xóa lịch sử của chính người dùng.
- Xuất báo cáo PDF.
4.8. Thư viện bệnh cây trồng








rahulvikram.com


Đây là một phân hệ độc lập, không nên chỉ hiển thị thông tin bệnh sau khi AI dự đoán.

Người dùng có thể tìm kiếm bệnh theo:
- Tên bệnh.
- Loại cây.
- Nhóm tác nhân.
- Mức độ phổ biến.
Mỗi trang bệnh gồm:
1. Tên bệnh tiếng Việt và tiếng Anh.
2. Hình ảnh minh họa.
3. Loại cây bị ảnh hưởng.
4. Tác nhân gây bệnh.
5. Dấu hiệu nhận biết.
6. Nguyên nhân và điều kiện phát triển.
7. Cách phòng bệnh.
8. Hướng dẫn xử lý.
9. Các lưu ý khi chăm sóc.
Nội dung kiến thức cần được biên soạn và kiểm duyệt. AI không nên tự tạo phác đồ sử dụng thuốc bảo vệ thực vật hoặc liều lượng hóa chất khi không có nguồn chuyên môn đáng tin cậy.
4.9. Hướng dẫn chăm sóc và nhắc nhở
Người dùng có thể tạo lịch:
- Kiểm tra lá.
- Tưới nước.
- Bón phân.
- Theo dõi tình trạng bệnh.
- Chụp ảnh kiểm tra lại.
Có thể xây dựng chức năng nhắc nhở theo ngày và hiển thị thông báo trong ứng dụng.

Giai đoạn mở rộng mới cần tích hợp email, push notification hoặc thời tiết.
4.10. Báo cáo và xuất PDF
Báo cáo cây trồng cần có:
- Thông tin cây.
- Tổng số lần kiểm tra.
- Lịch sử phát hiện bệnh.
- Biểu đồ diễn biến.
- Những bệnh đã gặp.
- Các lần chăm sóc.
- Đề xuất theo dõi tiếp theo.
Báo cáo toàn hệ thống có thể bao gồm:
- Tổng lượt phân tích.
- Số lượng ảnh đã xử lý.
- Tỷ lệ dự đoán theo class.
- Phân bố loại bệnh.
- Thời gian xử lý trung bình.
4.11. Quản trị viên








behance.net


Trang Admin phải có:
Phân hệ	Chức năng
Dashboard	Thống kê hoạt động toàn hệ thống
User Management	Xem, tìm kiếm, khóa và quản lý tài khoản
Plant Management	Quản lý danh mục cây
Disease Management	Thêm, sửa, xóa thông tin bệnh
Class Management	Quản lý các lớp AI hỗ trợ
Image Management	Kiểm tra và quản lý ảnh dữ liệu
Prediction History	Theo dõi các lần dự đoán
Feedback Management	Xem phản hồi và kết quả dự đoán sai
Model Management	Quản lý model version và trạng thái triển khai
Model Evaluation	Hiển thị các chỉ số đánh giá mô hình
System Settings	Cấu hình hệ thống

Đặc biệt, trang Model Evaluation nên hiển thị Accuracy, Precision, Recall, F1-score, confusion matrix và kết quả theo từng lớp. Đây là một chức năng có giá trị lớn đối với đồ án thiên về AI.

5. Quy trình hoạt động của AI
Đây là phần quan trọng nhất về chuyên môn, cần được triển khai thực sự chứ không chỉ tạo giao diện mô phỏng.
5.1. Pipeline nhận diện bệnh
#chatgpt-mermaid-_r_bq_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_bq_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_bq_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_bq_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_bq_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_bq_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_bq_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_bq_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_bq_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_bq_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_bq_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bq_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bq_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_bq_ p{margin:0;}#chatgpt-mermaid-_r_bq_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_bq_ .label text,#chatgpt-mermaid-_r_bq_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ .node rect,#chatgpt-mermaid-_r_bq_ .node circle,#chatgpt-mermaid-_r_bq_ .node ellipse,#chatgpt-mermaid-_r_bq_ .node polygon,#chatgpt-mermaid-_r_bq_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-_r_bq_ .rough-node .label text,#chatgpt-mermaid-_r_bq_ .node .label text,#chatgpt-mermaid-_r_bq_ .image-shape .label,#chatgpt-mermaid-_r_bq_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_bq_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_bq_ .rough-node .label,#chatgpt-mermaid-_r_bq_ .node .label,#chatgpt-mermaid-_r_bq_ .image-shape .label,#chatgpt-mermaid-_r_bq_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_bq_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_bq_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bq_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bq_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_bq_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_bq_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_bq_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_bq_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_bq_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_bq_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_bq_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_bq_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_bq_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_bq_ .icon-shape,#chatgpt-mermaid-_r_bq_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_bq_ .icon-shape p,#chatgpt-mermaid-_r_bq_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_bq_ .icon-shape .label rect,#chatgpt-mermaid-_r_bq_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_bq_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_bq_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_bq_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-_r_bq_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_bq_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_bq_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_bq_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bq_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_bq_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_bq_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_bq_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bq_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-_r_bq_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_bq_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bq_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_bq_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_bq_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bq_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_bq_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_bq_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_bq_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_bq_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_bq_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_bq_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-_r_bq_ .node rect,#chatgpt-mermaid-_r_bq_ .node circle,#chatgpt-mermaid-_r_bq_ .node ellipse,#chatgpt-mermaid-_r_bq_ .node polygon,#chatgpt-mermaid-_r_bq_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_bq_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_bq_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_bq_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_bq_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_bq_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Người dùng tải ảnh hoặc chụpảnhBackend nhận ảnhKiểm tra định dạng, kích thước,chất lượngẢnh có hợp lệ?Thông báo chụp lạiResize và NormalizeAI Classification ModelTính xác suất các lớpĐạt ngưỡng tin cậy?Kết quả chưa xác địnhXác định cây và bệnhLấy thông tin bệnh từKnowledge BaseGrad-CAM giải thích dự đoánLưu kết quả vào DatabaseHiển thị báo cáo cho ngườidùngKhôngCóKhôngCó





5.2. Các bước xử lý
Bước 1: Tiếp nhận hình ảnh

Ảnh được tải lên từ camera hoặc thư viện.

Bước 2: Tiền xử lý
- Đọc ảnh.
- Kiểm tra RGB.
- Resize theo kích thước mô hình, ví dụ 224 × 224.
- Normalize theo thông số đã sử dụng khi huấn luyện.
- Chuyển thành tensor.
Phải đảm bảo preprocessing khi inference giống với preprocessing khi huấn luyện.

Bước 3: Dự đoán

Mô hình AI nhận tensor và xuất ra vector xác suất ứng với từng lớp bệnh.

Ví dụ:
{    "Tomato___Early_blight": 0.948,    "Tomato___Late_blight": 0.032,    "Tomato___healthy": 0.020}



Bước 4: Xử lý kết quả

Backend:
- Sắp xếp các lớp theo xác suất.
- Lấy Top 3.
- Kiểm tra ngưỡng tin cậy.
- Ánh xạ class sang tên cây và bệnh.
- Lấy thông tin tương ứng trong cơ sở dữ liệu.
Bước 5: Giải thích

Có thể dùng Grad-CAM để tạo heatmap cho biết vùng ảnh nào đóng góp nhiều vào dự đoán của mạng.

Lưu ý: Grad-CAM là cách trực quan hóa sự chú ý của mô hình, không phải bằng chứng xác nhận vùng đó chính là tổn thương bệnh.
5.3. Mô hình AI nên sử dụng
Tôi đề xuất sử dụng Transfer Learning.
Mô hình	Ưu điểm	Vai trò
CNN tự xây dựng	Dễ giải thích kiến trúc và làm baseline	Mô hình cơ sở
ResNet50	Kiến trúc phổ biến, dễ nghiên cứu	Mô hình so sánh
MobileNetV3	Nhẹ, phù hợp thiết bị có tài nguyên hạn chế	Hướng tối ưu mobile
EfficientNet-B0	Cân bằng hiệu năng và kích thước	Mô hình chính đề xuất

Chiến lược: Huấn luyện CNN cơ sở, sau đó huấn luyện EfficientNet-B0 sử dụng pretrained weights và so sánh kết quả. Có thể bổ sung MobileNetV3 nếu còn thời gian.

Như vậy, trong báo cáo đồ án có phần thực nghiệm so sánh mô hình thay vì chỉ sử dụng một mô hình tải sẵn.

6. Xây dựng bộ dữ liệu và huấn luyện mô hình
6.1. Tổ chức dữ liệu
Không nên lưu tất cả hình ảnh vào một thư mục duy nhất.

Cấu trúc dữ liệu huấn luyện đề xuất:
ml/
├── datasets/
│   ├── raw/
│   │   ├── plantvillage/
│   │   └── plantdoc/
│   │
│   ├── processed/
│   │   ├── train/
│   │   │   ├── Apple___healthy/
│   │   │   ├── Apple___Black_rot/
│   │   │   ├── Tomato___healthy/
│   │   │   └── Tomato___Early_blight/
│   │   │
│   │   ├── val/
│   │   └── test/
│   │
│   └── metadata/
│       ├── classes.json
│       ├── dataset_info.json
│       └── class_distribution.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_cnn_baseline.ipynb
│   ├── 04_efficientnet_training.ipynb
│   └── 05_model_evaluation.ipynb
│
├── src/
│   ├── dataset.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── explainability.py
│
├── weights/
│   ├── best_model.pth
│   ├── class_mapping.json
│   └── model_metadata.json
│
└── reports/
    ├── training_history.png
    ├── confusion_matrix.png
    ├── classification_report.csv
    └── model_comparison.csv


6.2. Thu thập dữ liệu
Sử dụng PlantVillage làm nguồn huấn luyện chính ban đầu.

PlantVillage có 54.306 ảnh và ba cấu hình color, grayscale, segmented trên nguồn Hugging Face. Nguồn này cũng cung cấp cách chia tập 80/20 có xét nhóm lá. 

GitHub+1

Sau đó sử dụng PlantDoc để kiểm tra khả năng tổng quát hóa trên ảnh có bối cảnh tự nhiên hơn. Repository PlantDoc có hai thư mục train và test, và công bố giấy phép CC BY 4.0. 

GitHub+1

Các công việc cần thực hiện:
- Tải dữ liệu.
- Đọc và thống kê số lượng ảnh.
- Kiểm tra định dạng.
- Kiểm tra ảnh lỗi.
- Loại bỏ dữ liệu trùng lặp.
- Chuẩn hóa tên class.
- Phát hiện các class thiếu dữ liệu.
- Phân tích mất cân bằng lớp.
- Trực quan hóa hình ảnh mẫu.
6.3. Phân tích dữ liệu EDA
Notebook EDA cần tạo ra:
1. Tổng số ảnh.
2. Tổng số loại cây.
3. Tổng số lớp phân loại.
4. Số lượng ảnh từng lớp.
5. Biểu đồ phân bố class.
6. Hình ảnh đại diện từng class.
7. Kích thước ảnh.
8. Tỷ lệ ảnh RGB và grayscale.
9. Phát hiện ảnh lỗi.
10. Kiểm tra ảnh trùng lặp.








mdpi.com


Kết quả EDA cần được lưu thành biểu đồ để có thể đưa vào báo cáo đồ án.
6.4. Tiền xử lý và tăng cường dữ liệu
Các kỹ thuật đề xuất:
Kỹ thuật	Mục đích
Resize	Đồng nhất kích thước
Normalize	Chuẩn hóa pixel
Random Horizontal Flip	Tăng khả năng tổng quát
Random Rotation	Mô phỏng thay đổi góc chụp
Color Jitter	Thay đổi ánh sáng, màu sắc
Random Crop	Tăng biến thiên bố cục
Random Affine	Mô phỏng biến đổi hình học

Không áp dụng augmentation quá mạnh khiến biểu hiện bệnh bị biến dạng hoặc làm thay đổi đặc trưng quan trọng.
6.5. Chia tập dữ liệu
Đề xuất:
- Train: 70%.
- Validation: 15%.
- Test: 15%.
Hoặc giữ nguyên official test split của PlantVillage rồi tách validation từ train.

Điểm quan trọng: phải chia dữ liệu theo nhóm lá/ảnh gốc khi có metadata phù hợp, tránh ảnh của cùng một chiếc lá xuất hiện ở cả train và test. Không dùng test để điều chỉnh mô hình.

Đối với PlantDoc, nên giữ tập test đã công bố khi có thể, sau đó chỉ tách validation từ tập train. Khi so sánh PlantVillage và PlantDoc, cần đối chiếu lớp tương ứng, không mặc định tất cả class có mặt ở cả hai bộ dữ liệu.
6.6. Huấn luyện mô hình
Quy trình:
1. Load dataset.
2. Load pretrained weights.
3. Thay đổi lớp phân loại cuối theo số class.
4. Freeze backbone trong giai đoạn đầu.
5. Huấn luyện classifier head.
6. Unfreeze một phần hoặc toàn bộ backbone.
7. Fine-tune với learning rate thấp.
8. Theo dõi train loss và validation loss.
9. Lưu best checkpoint.
10. Đánh giá trên test.
Các tham số thử nghiệm ban đầu:
Tham số	Giá trị đề xuất
Input size	224 × 224
Batch size	32
Epoch	20–40
Optimizer	AdamW
Initial learning rate	0.0001
Loss	Cross Entropy
Scheduler	ReduceLROnPlateau hoặc Cosine Annealing
Early stopping	5–7 epoch không cải thiện

Đây là cấu hình khởi đầu để thử nghiệm, không phải cấu hình tối ưu đã được xác nhận.
6.7. Đánh giá mô hình
Phải có đầy đủ:

Accuracy

Tỷ lệ dự đoán đúng trên tổng số mẫu.

Precision

Khả năng những mẫu được dự đoán là một lớp thực sự thuộc lớp đó.

Recall

Khả năng tìm ra các mẫu thực sự thuộc một lớp.

F1-score

Trung bình điều hòa giữa Precision và Recall.

Đối với bài toán nhiều lớp và dữ liệu mất cân bằng, cần báo cáo cả macro-F1 và weighted-F1, không chỉ Accuracy.

Các biểu đồ cần có:










Training Curves

Loss và Accuracy theo epoch











Confusion Matrix

Phân tích nhầm lẫn giữa các bệnh











Metrics Comparison

So sánh các chỉ số mô hình











Grad-CAM

Trực quan hóa vùng ảnh ảnh hưởng đến dự đoán


Nên có thêm:
- Precision, Recall, F1-score từng lớp.
- Top-1 và Top-3 Accuracy.
- Inference time.
- Kích thước model.
- Calibration.
- Kiểm tra khả năng từ chối dự đoán khi gặp ảnh ngoài phân phối.
Bảng so sánh mô hình trong báo cáo:
Model	Accuracy	Macro-F1	Inference time
CNN baseline	Thực nghiệm	Thực nghiệm	Thực nghiệm
ResNet50	Thực nghiệm	Thực nghiệm	Thực nghiệm
EfficientNet-B0	Thực nghiệm	Thực nghiệm	Thực nghiệm

Không điền số liệu dự đoán trước khi chạy thử nghiệm.
6.8. Phân biệt ba bài toán AI
Đây là một điểm nên làm rõ trong báo cáo để tránh nhầm lẫn thuật ngữ:
Bài toán	Chức năng	Độ ưu tiên
Image Classification	Phân loại loại cây và bệnh	Bắt buộc
Explainable AI	Trực quan hóa vùng ảnh ảnh hưởng đến dự đoán	Nên có
Image Segmentation	Xác định vùng lá và vùng tổn thương	Mở rộng

Mô hình EfficientNet-B0 chỉ làm nhiệm vụ phân loại ảnh. Nó không tự tạo bounding box hay pixel mask cho vị trí bệnh. Muốn có bản đồ tổn thương và đo diện tích vùng bệnh, phải bổ sung mô hình segmentation và dữ liệu gán nhãn phù hợp.

Phạm vi AI nên chốt cho Đồ án chuyên ngành 2:
- Có mô hình phân loại bệnh thực sự.
- Có so sánh tối thiểu hai kiến trúc.
- Có Top 3 prediction và confidence.
- Có xử lý dự đoán không chắc chắn.
- Có Grad-CAM.
- Có báo cáo đầy đủ các metrics.
- Có chức năng lưu kết quả inference vào web.
Segmentation là phần nâng cao, không nên để nó làm chậm tiến độ hoàn thành sản phẩm chính.

7. Cơ sở dữ liệu
Sử dụng PostgreSQL.

Đề xuất các bảng như sau:
Bảng	Mục đích
users	Tài khoản người dùng
roles	Phân quyền
plants	Danh mục cây trồng
user_plants	Cây do người dùng quản lý
diseases	Danh mục bệnh
plant_disease_mapping	Quan hệ cây và bệnh
disease_symptoms	Triệu chứng bệnh
disease_treatments	Hướng dẫn xử lý
scans	Lịch sử phân tích ảnh
scan_predictions	Kết quả dự đoán
scan_feedback	Phản hồi về kết quả
care_logs	Nhật ký chăm sóc
reminders	Lịch nhắc nhở
notifications	Thông báo
model_versions	Thông tin phiên bản mô hình
model_evaluations	Chỉ số đánh giá mô hình
audit_logs	Nhật ký hoạt động quản trị

7.1. Quan hệ dữ liệu chính
#chatgpt-mermaid-_r_98_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_98_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_98_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_98_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_98_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_98_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_98_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_98_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_98_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_98_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_98_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_98_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_98_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_98_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_98_ p{margin:0;}#chatgpt-mermaid-_r_98_ .entityBox{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);}#chatgpt-mermaid-_r_98_ .relationshipLabelBox{fill:rgb(48, 48, 48);opacity:0.7;background-color:rgb(48, 48, 48);}#chatgpt-mermaid-_r_98_ .relationshipLabelBox rect{opacity:0.5;}#chatgpt-mermaid-_r_98_ .labelBkg{background-color:rgba(48, 48, 48, 0.5);}#chatgpt-mermaid-_r_98_ .edgeLabel{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_98_ .edgeLabel .label rect{fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_98_ .edgeLabel .label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_98_ .edgeLabel .label{fill:rgb(31, 78, 148);font-size:14px;}#chatgpt-mermaid-_r_98_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_98_ .edge-pattern-dashed{stroke-dasharray:8,8;}#chatgpt-mermaid-_r_98_ .node rect,#chatgpt-mermaid-_r_98_ .node circle,#chatgpt-mermaid-_r_98_ .node ellipse,#chatgpt-mermaid-_r_98_ .node polygon{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-_r_98_ .relationshipLine{stroke:rgb(175, 175, 175);stroke-width:1px;fill:none;}#chatgpt-mermaid-_r_98_ .marker{fill:none!important;stroke:rgb(175, 175, 175)!important;stroke-width:1;}#chatgpt-mermaid-_r_98_ [data-look=neo].labelBkg{background-color:rgba(48, 48, 48, 0.5);}#chatgpt-mermaid-_r_98_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-_r_98_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_98_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_98_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_98_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_98_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_98_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_98_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_98_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_98_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-_r_98_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_98_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_98_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_98_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_98_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_98_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_98_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_98_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}USERSUSER_PLANTSPLANTSSCANSSCAN_PREDICTIONSDISEASESPLANT_DISEASE_MAPPINGSCAN_FEEDBACKCARE_LOGSREMINDERSMODEL_VERSIONSMODEL_EVALUATIONSmanagesdescribesinspected_increatescontainsidentified_assupportsaffectsreceivesrecordsschedulespredicts_withevaluated_by





Nguyên tắc thiết kế:
- Người dùng chỉ được xem và sửa dữ liệu của mình.
- Admin mới được quản lý dữ liệu toàn hệ thống.
- Kết quả chẩn đoán phải lưu lại model version.
- Không lưu ảnh dưới dạng binary trực tiếp trong các bảng PostgreSQL. Chỉ lưu đường dẫn hoặc storage key.
- Nên có cơ chế xóa ảnh và dữ liệu cá nhân theo quyền của người dùng.

8. Thiết kế API Backend
Đề xuất REST API với tiền tố /api/v1.
Authentication
Method	Endpoint	Chức năng
POST	/auth/register	Đăng ký
POST	/auth/login	Đăng nhập
POST	/auth/logout	Đăng xuất
POST	/auth/refresh	Làm mới token
GET	/auth/me	Thông tin tài khoản
PUT	/auth/me	Cập nhật hồ sơ

Plant Management
Method	Endpoint	Chức năng
GET	/plants	Danh sách cây
GET	/plants/{id}	Chi tiết cây
POST	/my-plants	Thêm cây vào danh sách cá nhân
GET	/my-plants	Cây đang theo dõi
PUT	/my-plants/{id}	Sửa thông tin
DELETE	/my-plants/{id}	Xóa cây

AI Diagnosis
Method	Endpoint	Chức năng
POST	/diagnoses/predict	Phân tích ảnh
GET	/diagnoses	Danh sách kết quả
GET	/diagnoses/{id}	Chi tiết kết quả
DELETE	/diagnoses/{id}	Xóa kết quả
POST	/diagnoses/{id}/feedback	Phản hồi kết quả

Disease Library
Method	Endpoint	Chức năng
GET	/diseases	Danh sách bệnh
GET	/diseases/{id}	Chi tiết bệnh
GET	/diseases/search	Tìm kiếm bệnh
GET	/diseases/by-plant/{id}	Bệnh của từng loại cây

Plant Health Analytics
Method	Endpoint	Chức năng
GET	/analytics/dashboard	Thống kê Dashboard
GET	/analytics/plant/{id}	Phân tích tình trạng cây
GET	/analytics/history/{id}	Diễn biến theo thời gian
GET	/analytics/disease-distribution	Phân bố bệnh

Care & Reminders
Method	Endpoint	Chức năng
GET	/care-logs	Nhật ký chăm sóc
POST	/care-logs	Thêm nhật ký
POST	/reminders	Tạo nhắc nhở
GET	/reminders	Danh sách nhắc nhở
PUT	/reminders/{id}	Cập nhật
DELETE	/reminders/{id}	Xóa

Admin
Method	Endpoint	Chức năng
GET	/admin/users	Quản lý người dùng
GET	/admin/scans	Quản lý kết quả phân tích
POST	/admin/diseases	Thêm bệnh
PUT	/admin/diseases/{id}	Cập nhật bệnh
GET	/admin/models	Danh sách model
POST	/admin/models	Đăng ký model version
GET	/admin/model-evaluations	Xem kết quả đánh giá

API có tài liệu Swagger tự động từ FastAPI, phục vụ kiểm thử và tích hợp frontend.

9. Thiết kế giao diện đa nền tảng
9.1. Các trang cần có
Mã	Trang
P01	Trang chủ
P02	Đăng nhập
P03	Đăng ký
P04	Quên mật khẩu
P05	Dashboard
P06	AI Disease Detection
P07	Kết quả phân tích
P08	Plant Health Analysis
P09	My Plants
P10	Plant Detail
P11	Diagnosis History
P12	Disease Library
P13	Disease Detail
P14	Care Schedule
P15	Notifications
P16	Profile
A01	Admin Dashboard
A02	User Management
A03	Plant Management
A04	Disease Management
A05	Dataset/Class Management
A06	Model Management
A07	Model Evaluation
A08	Prediction Management
A09	System Settings

9.2. Quy tắc Responsive










Laptop / Desktop

Sidebar, dashboard nhiều cột, bảng và biểu đồ lớn.











Điện thoại

Menu thu gọn, camera, nút thao tác lớn, nội dung một cột.


Các yêu cầu:
- Desktop: sidebar cố định hoặc thu gọn.
- Tablet: sidebar dạng drawer.
- Mobile: navigation dưới hoặc menu drawer.
- Các biểu đồ tự co giãn.
- Form không bị tràn màn hình.
- Bảng có cơ chế chuyển thành card hoặc cuộn ngang hợp lý.
- Nút chụp ảnh phải hoạt động trên trình duyệt di động.
- Có loading skeleton, empty state và error state.
- Có chế độ cài PWA.
- Có giao diện tiếng Việt; có thể bổ sung tiếng Anh.
Không chỉ kiểm tra giao diện ở độ rộng desktop. Phải kiểm thử thực tế ở nhiều kích thước viewport.
9.3. Hệ thống thiết kế giao diện
Phong cách đề xuất:
- Màu chủ đạo: xanh lá đậm.
- Màu phụ: xanh nhạt, trắng, xám.
- Nền sáng.
- Thẻ bo góc vừa phải.
- Font dễ đọc.
- Biểu đồ trực quan.
- Icon nhất quán.
- Hình ảnh thực tế của cây và bệnh.
Ưu tiên trải nghiệm người dùng hơn hiệu ứng trang trí.

10. Bảo mật và độ ổn định
Các yêu cầu tối thiểu:

Bảo mật
- Hash mật khẩu bằng Argon2 hoặc bcrypt.
- Xác thực và phân quyền backend.
- Không lưu secret trong mã nguồn.
- Sử dụng .env.
- Kiểm tra file upload bằng MIME và nội dung thực tế.
- Giới hạn dung lượng và kích thước ảnh.
- Không cho phép người dùng truy cập dữ liệu người khác bằng cách thay ID trên URL.
- CORS giới hạn theo domain.
- Rate limiting cho các API đăng nhập và dự đoán.
- Xử lý lỗi không tiết lộ thông tin nhạy cảm.
Ổn định
- Xử lý lỗi model chưa được load.
- Kiểm tra Database kết nối.
- Logging.
- Kiểm tra API health.
- Không lưu kết quả giả khi AI bị lỗi.
- Không cho phép ứng dụng báo thành công khi việc lưu dữ liệu thất bại.
- Xây dựng test cho cả backend và frontend.
Quyền riêng tư
- Không tự động công khai ảnh của người dùng.
- Có chính sách lưu trữ và xóa ảnh.
- Thông báo rõ khi ảnh được gửi lên máy chủ để phân tích.

11. Cấu trúc thư mục toàn bộ project
Tôi đề xuất tổ chức source code như sau để dễ phát triển, bảo trì và chia công việc cho AI lập trình.
smart-plant-care/
│
├── frontend/
│   ├── public/
│   │   ├── images/
│   │   ├── icons/
│   │   └── manifest.json
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   ├── charts/
│   │   │   └── forms/
│   │   │
│   │   ├── pages/
│   │   │   ├── public/
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── diagnosis/
│   │   │   ├── plants/
│   │   │   ├── analytics/
│   │   │   ├── diseases/
│   │   │   ├── history/
│   │   │   ├── care/
│   │   │   └── admin/
│   │   │
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── routes/
│   │   └── App.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── plants.py
│   │   │       ├── diagnoses.py
│   │   │       ├── diseases.py
│   │   │       ├── analytics.py
│   │   │       ├── reminders.py
│   │   │       └── admin.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── permissions.py
│   │   │
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── base.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   │
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── image_service.py
│   │   │   ├── diagnosis_service.py
│   │   │   ├── plant_service.py
│   │   │   ├── analytics_service.py
│   │   │   └── report_service.py
│   │   │
│   │   ├── ml/
│   │   │   ├── predictor.py
│   │   │   ├── preprocessing.py
│   │   │   ├── model_loader.py
│   │   │   ├── class_mapping.py
│   │   │   └── gradcam.py
│   │   │
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── ml/
│   ├── datasets/
│   ├── notebooks/
│   ├── src/
│   ├── weights/
│   ├── reports/
│   └── requirements.txt
│
├── docs/
│   ├── requirements.md
│   ├── architecture.md
│   ├── api-documentation.md
│   ├── database-design.md
│   ├── ai-model.md
│   └── testing.md
│
├── infra/
│   ├── docker/
│   └── docker-compose.yml
│
├── .gitignore
├── README.md
└── LICENSE


Lưu ý: Thư mục ml/datasets và ml/weights có thể chứa dung lượng lớn. Không nên commit toàn bộ dataset vào GitHub. Cần sử dụng .gitignore, lưu trữ riêng và ghi rõ cách tải dữ liệu, model.

12. Kiểm thử toàn bộ hệ thống
Đồ án phải có kiểm thử cả AI và website.
Nhóm	Các nội dung kiểm thử
AI	Phân loại đúng, sai, confidence thấp
AI	Ảnh lá khỏe mạnh
AI	Ảnh lá có bệnh
AI	Ảnh không phải lá cây
AI	Ảnh quá tối, mờ, sai định dạng
Authentication	Đăng ký, đăng nhập, đăng xuất
Authorization	USER không truy cập chức năng ADMIN
Diagnosis	Upload ảnh, dự đoán, lưu kết quả
Plant	Thêm, sửa, xóa cây
History	Lưu và truy vấn lịch sử
Analytics	Tính toán và hiển thị biểu đồ
Admin	Quản lý người dùng, bệnh và model
Responsive	Laptop, tablet, điện thoại
Integration	Frontend kết nối Backend và Database

Tiêu chí nghiệm thu
Tôi đề xuất đặt ra những điều kiện sau:
1. Người dùng đăng ký, đăng nhập được.
2. Người dùng có thể quản lý nhiều cây trồng.
3. Người dùng chụp ảnh hoặc tải ảnh lên từ điện thoại và laptop.
4. Backend thực sự gọi mô hình PyTorch đã huấn luyện.
5. Hệ thống trả kết quả bệnh và confidence score.
6. Có cơ chế xử lý ảnh không phù hợp hoặc không chắc chắn.
7. Có Grad-CAM.
8. Kết quả được lưu vào Database.
9. Có lịch sử phân tích.
10. Có trang phân tích tình trạng cây.
11. Có thư viện bệnh.
12. Có trang quản trị.
13. Có báo cáo đánh giá mô hình.
14. Giao diện responsive.
15. Không có chức năng quan trọng nào chỉ là giao diện giả hoặc dữ liệu tĩnh.

13. Lộ trình triển khai đồ án
Không nên bắt AI xây dựng tất cả các chức năng cùng một lúc. Dự án có nhiều module, nếu làm đồng thời rất dễ sinh lỗi kết nối, sai schema và giao diện có chức năng nhưng backend không hoạt động.

Nên chia thành 7 giai đoạn.
Roadmap phát triển
1. Giai đoạn 1 – Phân tích và thiết kế
   Nền tảng bắt buộc
   - Chốt yêu cầu.
   - Phân tích database.
   - Thiết kế kiến trúc.
   - Tạo cấu trúc project.
   - Thiết kế giao diện cơ bản.
2. Giai đoạn 2 – Xây dựng AI
   - Tải và phân tích PlantVillage.
   - Tiền xử lý dữ liệu.
   - Huấn luyện CNN baseline.
   - Huấn luyện EfficientNet-B0.
   - Đánh giá và so sánh.
   - Lưu model và class mapping.
3. Giai đoạn 3 – Backend
   - Kết nối PostgreSQL.
   - Xây dựng Authentication.
   - Xây dựng API quản lý cây.
   - Tích hợp AI inference.
   - Xây dựng API chẩn đoán.
4. Giai đoạn 4 – Frontend
   - Trang chủ.
   - Login/Register.
   - Dashboard.
   - AI Detection.
   - Kết quả phân tích.
   - Responsive.
5. Giai đoạn 5 – Các tính năng mở rộng
   - Quản lý cây.
   - Lịch sử.
   - Health Analytics.
   - Disease Library.
   - Nhật ký chăm sóc.
   - Nhắc nhở.
   - Báo cáo PDF.
6. Giai đoạn 6 – Admin
   - Quản lý tài khoản.
   - Quản lý bệnh.
   - Quản lý class.
   - Quản lý model.
   - Model Evaluation.
   - Dashboard quản trị.
7. Giai đoạn 7 – Kiểm thử và triển khai
   - Integration testing.
   - Kiểm thử trên điện thoại.
   - Kiểm thử AI.
   - Sửa lỗi.
   - Docker.
   - Deploy frontend và backend.
   - Hoàn thiện báo cáo và slide bảo vệ.

Ưu tiên thực hiện
Mức độ	Chức năng
P0	AI nhận diện bệnh, Backend, Database, Upload ảnh
P0	Login, Dashboard, Lịch sử, Responsive
P1	Plant Management, Health Analytics, Disease Library
P1	Admin, Grad-CAM, PDF Report
P2	PWA, Reminder, Feedback
P2	Segmentation, Weather Integration, AI Chatbot

Đối với thời gian của Đồ án chuyên ngành 2, nên hoàn thành toàn bộ P0 và phần lớn P1 trước. Những tính năng P2 là phần mở rộng khi đã hoàn thiện hệ thống chính.

14. MASTER PROMPT – Đưa cho AI lập trình xây dựng toàn bộ dự án
Phần dưới đây là bản đặc tả có thể đưa trực tiếp cho Cursor, Claude Code, Codex hoặc AI lập trình khác.

Tôi viết theo hướng yêu cầu AI hiểu cả nghiệp vụ, kiến trúc, công nghệ, chức năng và nguyên tắc triển khai, không chỉ đơn giản yêu cầu nó tạo giao diện.
MASTER PROJECT SPECIFICATION
Ready to use

Copy toàn bộ nội dung bên dưới để làm tài liệu định hướng cho AI coding agent.
 Copy Master Prompt

15. Cách sử dụng AI để triển khai đúng hướng
Đừng chỉ gửi Master Prompt rồi yêu cầu AI tạo toàn bộ dự án. Hãy sử dụng nó làm tài liệu gốc, sau đó yêu cầu từng giai đoạn.

Tôi khuyên quy trình làm việc như sau:

Lần 1 – Thiết kế và khởi tạo

Đưa Master Prompt cho AI, yêu cầu đọc yêu cầu, lập kiến trúc, database schema và tạo cấu trúc thư mục. Chưa cần viết mọi chức năng.

Lần 2 – Hoàn thành AI

Yêu cầu AI xử lý PlantVillage, EDA, training, evaluation và xuất model. Đặc biệt phải giữ lại notebook và các báo cáo để đưa vào đồ án.

Lần 3 – Hoàn thành Backend

Tạo database, authentication, CRUD, AI inference và API.

Lần 4 – Hoàn thành Frontend

Tạo giao diện và kết nối từng API đã hoàn thành. Không để AI tự ý thay đổi response format backend.

Lần 5 – Kiểm thử tích hợp

Yêu cầu AI chạy toàn bộ luồng từ đăng nhập, thêm cây, tải ảnh, phân tích bằng model thật đến lưu và xem lịch sử.

Lần 6 – Hoàn thiện

Responsive, Admin, Analytics, PDF, Docker và triển khai.

Một yêu cầu rất quan trọng: bắt AI duy trì PROJECT_PLAN.md, TASKS.md, API_CONTRACT.md và README.md trong quá trình phát triển. Điều này giúp AI không mất định hướng khi làm dự án dài.

16. Định hướng trình bày khi bảo vệ đồ án
Tôi đề xuất bố cục báo cáo theo 5 chương:
Chương	Nội dung
Chương 1	Tổng quan đề tài, lý do chọn đề tài, mục tiêu và phạm vi
Chương 2	Cơ sở lý thuyết, Computer Vision, CNN, Transfer Learning, các mô hình
Chương 3	Phân tích thiết kế hệ thống, kiến trúc, database, API, UI/UX
Chương 4	Xây dựng dataset, tiền xử lý, huấn luyện, đánh giá và tích hợp AI
Chương 5	Kết quả thử nghiệm, kiểm thử hệ thống, hạn chế và hướng phát triển

Khi bảo vệ, nên có một quy trình demo xuyên suốt:
1. Đăng nhập vào hệ thống.
2. Thêm một cây cà chua.
3. Chụp ảnh lá bệnh bằng điện thoại.
4. Upload ảnh và chạy AI.
5. Xem kết quả phân loại, Top 3 và Grad-CAM.
6. Xem thông tin bệnh và hướng dẫn chăm sóc.
7. Lưu kết quả vào hồ sơ cây.
8. Thực hiện lần kiểm tra thứ hai.
9. Xem lịch sử và biểu đồ theo dõi.
10. Đăng nhập Admin để xem thống kê và kết quả đánh giá mô hình.
Đây sẽ là một luồng demo thể hiện đầy đủ sự liên kết giữa AI, backend, database và giao diện.

17. Kết luận và phạm vi nên chốt
Theo tôi, cấu hình phù hợp nhất cho Đồ án chuyên ngành 2 là:
Smart Plant Care AI
AI-Based Plant Disease Detection and Health Monitoring Platform

React
Responsive Web / PWA

FastAPI
Backend REST API

PyTorch
Deep Learning

PostgreSQL
Database



Sản phẩm phải hoàn thành
- [x] AI nhận diện cây và bệnh.
- [x] Transfer Learning và đánh giá mô hình.
- [x] Grad-CAM.
- [x] Quản lý người dùng.
- [x] Quản lý cây trồng.
- [x] Health Analytics.
- [x] Lịch sử chẩn đoán.
- [x] Disease Library.
- [x] Admin Dashboard.
- [x] Báo cáo PDF.
- [x] Responsive laptop và điện thoại.
- [x] Docker và hướng dẫn triển khai.

Một điểm tôi muốn nhấn mạnh: Đừng biến đồ án thành một website đẹp nhưng AI chỉ trả về kết quả được lập trình sẵn. Giá trị học thuật nằm ở quá trình xử lý dữ liệu, thử nghiệm mô hình, đánh giá khả năng tổng quát hóa và tích hợp mô hình vào một sản phẩm thực tế.

Tôi khuyên bắt đầu theo thứ tự: AI Dataset và Model → Backend → Frontend → Analytics → Admin → Deployment. Nhưng ngay từ đầu hãy thiết kế kiến trúc tổng thể để các module có thể kết nối với nhau mà không phải viết lại khi mở rộng.

Đây là hướng triển khai đủ rộng để trở thành một sản phẩm hoàn chỉnh, nhưng vẫn có thể chia nhỏ để kiểm soát tiến độ và chất lượng trong khuôn khổ đồ án chuyên ngành 2.

Đúng. Tôi nghĩ cần dừng phần thiết kế giao diện ở đây và chuyển sang xây dựng một đặc tả kỹ thuật riêng cho AI Backend và Dataset Pipeline. Đây phải là nền móng của toàn bộ đồ án.

Có một vấn đề rất quan trọng trong câu hỏi của bạn: PlantVillage và PlantDoc không phải hai bộ dữ liệu có cùng cấu trúc, cùng điều kiện chụp ảnh hay cùng tập nhãn. Không thể cứ tải cả hai về, gộp thư mục rồi chia ngẫu nhiên 80/20 để huấn luyện và kiểm thử.

Tôi sẽ chốt một phương án có thể đưa vào báo cáo khoa học và triển khai thực tế, gồm ba kiểu đánh giá riêng:
1. In-domain evaluation: Mô hình học và kiểm tra trên cùng nguồn PlantVillage, nhưng ảnh train/validation/test hoàn toàn khác nhau.
2. Cross-domain evaluation: Huấn luyện bằng PlantVillage, kiểm tra trên PlantDoc để đánh giá khả năng nhận diện ảnh ngoài môi trường kiểm soát.
3. Open-set evaluation: Đưa vào ảnh cây chưa từng được huấn luyện, ảnh bệnh chưa hỗ trợ hoặc ảnh không phải lá cây để kiểm tra xem mô hình có biết từ chối kết luận hay không.
Ba bài đánh giá này trả lời ba câu hỏi khác nhau. Không được gộp kết quả thành một Accuracy duy nhất.
PHẦN A. CHỐT CHIẾN LƯỢC DATASET
1. Chính xác thì từng dataset dùng để làm gì?
Dataset 1: PlantVillage
Nguồn huấn luyện chính









researchgate.net


Đặc điểm:
- 54.306 ảnh theo công bố của bộ dữ liệu.
- 14 loại cây trồng.
- 38 lớp phân loại kết hợp loại cây và tình trạng bệnh.
- Ảnh RGB, grayscale và segmented.
- Ảnh chủ yếu được chụp trong điều kiện kiểm soát, nền tương đối đơn giản.
Phân công sử dụng:
- Train: Có.
- Validation: Có, tách từ phần train.
- Test nội bộ: Có, giữ tập test độc lập.
- Cross-domain test: Không phải nguồn chính.
Nguồn: PlantVillage Dataset. 

GitHub+1


Dataset 2: PlantDoc
Nguồn kiểm thử thực tế









mdpi.com


Đặc điểm:
- Công bố ban đầu có 2.598 ảnh.
- 13 loại cây.
- Ảnh được thu thập từ Internet, có bối cảnh tự nhiên phức tạp hơn.
- Có ảnh lá với ánh sáng, góc chụp, kích thước và nền khác nhau.
Phân công sử dụng:
- Train: Không sử dụng trong thí nghiệm đánh giá khả năng tổng quát hóa ban đầu.
- Validation: Không dùng cho việc điều chỉnh mô hình PlantVillage trong thí nghiệm cross-domain thuần túy.
- Test: Có, trên các lớp tương ứng với PlantVillage.
- Fine-tuning: Chỉ trong một thí nghiệm riêng, không trộn với bài test độc lập.
Nguồn: PlantDoc Dataset. 

GitHub+1


Tại sao tôi chọn PlantVillage làm train chính và PlantDoc làm test độc lập?

Vì đây là một bài toán nghiên cứu có ý nghĩa:
Một mô hình được huấn luyện từ các hình ảnh lá cây có nền tương đối đơn giản có thể nhận diện chính xác bệnh khi người dùng chụp ảnh bằng điện thoại trong môi trường thực tế hay không?

Đây là vấn đề domain shift (sự khác biệt phân phối dữ liệu giữa môi trường huấn luyện và môi trường kiểm thử).

Việc sử dụng PlantDoc làm tập đánh giá độc lập giúp chúng ta biết mô hình có thực sự tổng quát hóa hay chỉ học được đặc điểm của những bức ảnh trong PlantVillage.

2. Train, Validation, Test khác nhau chính xác như thế nào?
Ba tập này có nhiệm vụ riêng, tuyệt đối không sử dụng thay thế tùy tiện.
TRAIN – Dữ liệu huấn luyện
Được phép học
AI sử dụng các ảnh trong tập này để cập nhật trọng số mạng neural.

Ví dụ: ảnh cà chua bị Early Blight, ảnh khoai tây khỏe mạnh, ảnh táo bị Black Rot.

VALIDATION – Dữ liệu kiểm định
Được phép dùng để lựa chọn mô hình
AI không học trực tiếp từ tập này. Ta sử dụng nó để:
- So sánh các mô hình.
- Chọn learning rate.
- Điều chỉnh hyperparameters.
- Theo dõi overfitting.
- Chọn checkpoint tốt nhất.
- Điều chỉnh ngưỡng confidence và calibration.
TEST – Dữ liệu kiểm thử cuối cùng
Không được dùng để điều chỉnh mô hình
Chỉ mở tập này sau khi đã chốt mô hình và các ngưỡng.

Dùng để tính Accuracy, Precision, Recall, F1-score và các chỉ số cuối cùng. Không xem kết quả rồi quay lại tinh chỉnh cho đến khi đạt con số mong muốn.

Ví dụ với PlantVillage, ta dùng một cách chia:
Tập	Tỷ lệ	Mục đích
Train	70%	Huấn luyện
Validation	15%	Lựa chọn và tối ưu mô hình
Test	15%	Báo cáo kết quả cuối cùng

Đây là tỷ lệ đề xuất nếu tự tổ chức lại dữ liệu. Tuy nhiên, PlantVillage hiện có sẵn official split 80/20 theo nhóm lá với 43.596 ảnh train và 10.709 ảnh test ở cấu hình color. Vì vậy, phương án tôi ưu tiên hơn là:
- Giữ nguyên official test 10.709 ảnh.
- Chia official train 43.596 ảnh thành train và validation.
- Không động vào test trong quá trình huấn luyện. 
  
  GitHub+1
Cách này vừa tận dụng được cách chia dữ liệu của nguồn công bố, vừa có validation độc lập.
3. Hai bộ dữ liệu khác loại cây, khác nhãn thì xử lý thế nào?
Đây là chỗ phải làm cẩn thận nhất.
3.1. Phân biệt loại cây và lớp bệnh
Một lớp phân loại của mô hình không chỉ là tên bệnh, mà phải là tổ hợp:
\[
\text{Class} = \text{Plant Species} + \text{Disease State}
\]

Ví dụ:
Tomato___Early_blight
Tomato___Late_blight
Tomato___healthy

Potato___Early_blight
Potato___Late_blight
Potato___healthy


Không được gộp tất cả Early Blight của cà chua và khoai tây thành một lớp chung, vì hệ thống cần xác định cả loại cây.

PlantVillage có 38 lớp tổ hợp cây-bệnh. PlantDoc có cách đặt tên lớp khác, trong đó có các lớp healthy và disease riêng biệt. Bản đóng gói PlantDoc có 28 lớp tổng hợp từ các thư mục ảnh; con số 17 trong bài báo gốc là số nhóm bệnh được công bố, không phải số thư mục phân loại tổng cộng. 

GitHub+3

3.2. Bảng đối chiếu nhãn
Ta cần xây dựng một bộ quy tắc chuẩn hóa nhãn (Label Harmonization).

Ví dụ:
PlantVillage	PlantDoc	Đánh giá
Apple Scab	Apple Scab Leaf	Có thể đối chiếu
Grape Black Rot	Grape leaf black rot	Có thể đối chiếu
Potato Early Blight	Potato leaf early blight	Có thể đối chiếu
Potato Late Blight	Potato leaf late blight	Có thể đối chiếu
Tomato Early Blight	Tomato Early blight leaf	Có thể đối chiếu
Tomato Septoria	Tomato Septoria leaf spot	Có thể đối chiếu
Tomato Bacterial Spot	Tomato leaf bacterial spot	Có thể đối chiếu
Tomato Late Blight	Tomato leaf late blight	Có thể đối chiếu
Tomato Mosaic Virus	Tomato leaf mosaic virus	Có thể đối chiếu
Tomato Leaf Mold	Tomato mold leaf	Cần xác minh nhãn
Tomato Yellow Leaf Curl Virus	Tomato leaf yellow virus	Cần xác minh nhãn
Corn Common Rust	Corn rust leaf	Cần xác minh nhãn
Corn Northern Leaf Blight	Corn leaf blight	Không tự động đồng nhất
Pepper Bacterial Spot	Bell pepper leaf spot	Không tự động đồng nhất

Bảng trên là các cặp nhãn ứng viên, không phải bảng đã được xác nhận chuyên môn. Phải đối chiếu mô tả và hình ảnh gốc, đặc biệt với các tên bệnh viết chung chung như Corn leaf blight hoặc Bell pepper leaf spot.

Ví dụ, chỉ vì hai nhãn có chữ Blight không có nghĩa chúng là cùng một bệnh.
3.3. Xây dựng hệ thống nhãn chuẩn hóa
Không dùng trực tiếp tên thư mục của dataset làm class index.

Ta tạo một danh mục nhãn thống nhất:
ml/
└── configs/
    ├── plant_classes.yaml
    ├── disease_classes.yaml
    └── label_mapping.yaml


Ví dụ label_mapping.yaml:
classes:

  - id: tomato_early_blight
    plant: tomato
    disease: early_blight
    healthy: false

  - id: tomato_late_blight
    plant: tomato
    disease: late_blight
    healthy: false

  - id: tomato_healthy
    plant: tomato
    disease: healthy
    healthy: true

  - id: potato_early_blight
    plant: potato
    disease: early_blight
    healthy: false

  - id: potato_late_blight
    plant: potato
    disease: late_blight
    healthy: false

  - id: potato_healthy
    plant: potato
    disease: healthy
    healthy: true


Sau đó lưu quan hệ với nhãn gốc:
dataset_mappings:

  - dataset: plantvillage
    raw_label: Tomato___Early_blight
    canonical_id: tomato_early_blight
    mapping_status: exact

  - dataset: plantdoc
    raw_label: Tomato Early blight leaf
    canonical_id: tomato_early_blight
    mapping_status: verified

  - dataset: plantdoc
    raw_label: Corn leaf blight
    canonical_id: null
    mapping_status: ambiguous
    reason: "Disease name is not sufficiently specific"


Các trạng thái mapping:
Trạng thái	Ý nghĩa	Có dùng trong đánh giá chung?
exact	Nhãn trùng khớp	Có
verified	Đã xác minh tương đương	Có
ambiguous	Chưa đủ căn cứ	Không
unmapped	Không có nhãn tương ứng	Không

Mục đích là tránh tạo ra một bài đánh giá có kết quả Accuracy cao nhưng bản chất hai tập dữ liệu đang dùng hai cách gọi bệnh khác nhau.
3.4. Vậy các lớp không có ở cả hai dataset xử lý thế nào?
Ta chia thành ba trường hợp.
Trường hợp 1: Cùng cây, cùng bệnh

Ví dụ: Tomato Early Blight xuất hiện trong cả hai dataset.
Known class
Được dùng để đánh giá Cross-domain.

Trường hợp 2: Cùng cây, bệnh khác hoặc chưa có nhãn tương ứng

Ví dụ: mô hình được huấn luyện với một số bệnh cà chua nhưng nhận hình ảnh một bệnh cà chua không nằm trong 38 lớp.
Unknown disease
Không được tự động gán vào một bệnh đã biết. Đưa vào bài kiểm tra khả năng từ chối dự đoán.

Trường hợp 3: Loại cây chưa từng được huấn luyện

Ví dụ: mô hình học Apple, Tomato, Potato nhưng người dùng tải ảnh lá sắn (Cassava).
Unsupported crop / OOD
Phải nhận diện đây là trường hợp ngoài phạm vi hỗ trợ và từ chối đưa ra kết luận bệnh.

Đặc biệt, PlantVillage có 14 loài cây, còn PlantDoc có 13 loài. Danh sách cây của PlantDoc phần lớn nằm trong danh mục loài của PlantVillage; Orange là một ví dụ về cây có trong PlantVillage nhưng không có trong danh mục PlantDoc được sử dụng ở đây. Vì thế PlantDoc rất hữu ích để kiểm tra domain shift, nhưng không đủ để kiểm chứng khả năng nhận biết một cây hoàn toàn mới. 

GitHub+2


4. Nếu người dùng đưa vào một loại cây chưa từng Train thì AI làm gì?
Bạn đặt đúng vấn đề: CNN classification thông thường không tự hiểu khái niệm cây mới.

Giả sử mô hình có 38 output classes.

Người dùng tải hình ảnh một chiếc lá sắn lên. Mô hình vẫn phải xuất ra một trong 38 lớp nếu chỉ sử dụng Softmax thông thường.

Nó có thể trả về:
Tomato___Early_blight: 0.81
Potato___Early_blight: 0.11
Apple___Black_rot: 0.05
...


Điều đó không có nghĩa chiếc lá sắn bị bệnh đốm vòng cà chua. Đây là một dự đoán sai rất nguy hiểm.
4.1. Giải pháp: Open-set Recognition và OOD Detection
Tôi đề xuất xây dựng thêm một tầng kiểm tra trước khi chấp nhận kết quả phân loại.
#chatgpt-mermaid-_r_ma_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_ma_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_ma_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_ma_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_ma_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_ma_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_ma_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_ma_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_ma_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_ma_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_ma_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_ma_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_ma_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_ma_ p{margin:0;}#chatgpt-mermaid-_r_ma_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_ma_ .label text,#chatgpt-mermaid-_r_ma_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ .node rect,#chatgpt-mermaid-_r_ma_ .node circle,#chatgpt-mermaid-_r_ma_ .node ellipse,#chatgpt-mermaid-_r_ma_ .node polygon,#chatgpt-mermaid-_r_ma_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-_r_ma_ .rough-node .label text,#chatgpt-mermaid-_r_ma_ .node .label text,#chatgpt-mermaid-_r_ma_ .image-shape .label,#chatgpt-mermaid-_r_ma_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_ma_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_ma_ .rough-node .label,#chatgpt-mermaid-_r_ma_ .node .label,#chatgpt-mermaid-_r_ma_ .image-shape .label,#chatgpt-mermaid-_r_ma_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_ma_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_ma_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_ma_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_ma_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_ma_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_ma_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_ma_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_ma_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_ma_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_ma_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_ma_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_ma_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_ma_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_ma_ .icon-shape,#chatgpt-mermaid-_r_ma_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_ma_ .icon-shape p,#chatgpt-mermaid-_r_ma_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_ma_ .icon-shape .label rect,#chatgpt-mermaid-_r_ma_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_ma_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_ma_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_ma_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-_r_ma_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_ma_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_ma_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_ma_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_ma_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_ma_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_ma_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_ma_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_ma_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-_r_ma_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_ma_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_ma_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_ma_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_ma_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_ma_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_ma_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_ma_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_ma_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_ma_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_ma_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_ma_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-_r_ma_ .node rect,#chatgpt-mermaid-_r_ma_ .node circle,#chatgpt-mermaid-_r_ma_ .node ellipse,#chatgpt-mermaid-_r_ma_ .node polygon,#chatgpt-mermaid-_r_ma_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_ma_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_ma_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_ma_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_ma_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_ma_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Ảnh được tải lênImage Quality CheckẢnh hợp lệ?Yêu cầu chụp lạiLeaf / Plant Image ValidationCó phải ảnh phù hợp?Từ chối ảnhPlant Disease ClassifierOOD DetectorẢnh thuộc phạm vi model?Unsupported / UnknownKiểm tra confidence vàcalibrationĐạt ngưỡng?Chưa đủ độ tin cậyTrả tên cây và bệnhNoYesNoYesNoYesNoYes





Các module:

Module 1 – Image Quality Check

Kiểm tra ảnh bị mờ, quá tối, quá nhỏ hoặc không đủ thông tin.

Module 2 – Plant/Leaf Validation

Kiểm tra ảnh có thuộc phạm vi hình ảnh thực vật và lá cây hay không.

Module 3 – Disease Classifier

Phân loại theo 38 lớp hỗ trợ.

Module 4 – OOD Detector

Kiểm tra ảnh có khả năng thuộc ngoài phân phối dữ liệu huấn luyện hay không.

Module 5 – Confidence Calibration

Đánh giá độ tin cậy và quyết định có chấp nhận dự đoán hay không.
4.2. Cần bổ sung dataset nào cho OOD?
Trong danh sách ban đầu của bạn, tôi đề xuất bổ sung bộ Cassava Leaf Disease.










Cassava Leaf Disease Dataset
- 21.397 ảnh.
- Cây sắn, không có trong danh mục 14 cây của PlantVillage.
- Gồm lá khỏe mạnh và các tình trạng bệnh thường gặp.
- Ảnh được thu thập từ khoảng 200 nông hộ ở Uganda bằng điện thoại.
Nguồn: Open Plant Image Archive và Cassava Disease Classification.


Cách sử dụng:
- Không đưa Cassava vào 38 lớp bệnh của mô hình PlantVillage.
- Sử dụng một phần ảnh Cassava trong bộ OOD development/calibration.
- Giữ riêng các ảnh Cassava khác để kiểm thử OOD.
- Đánh giá xem mô hình có từ chối kết luận thay vì dự đoán nhầm một lớp Tomato, Potato hoặc Apple hay không.
Có thể bổ sung thêm ảnh lá lúa từ bộ Rice Leaf Disease Image Samples gồm 5.932 ảnh và bốn nhóm bệnh để mở rộng đánh giá cây chưa được hỗ trợ. 

Mendeley Data+1

Tuy nhiên, một bộ Cassava riêng lẻ không đủ chứng minh hệ thống có thể nhận biết tất cả các cây lạ. Open-set detection là bài toán đánh giá khả năng từ chối trên những mẫu OOD cụ thể, không phải bảo đảm rằng mọi loại cây chưa từng gặp đều được nhận diện chính xác.

PHẦN B. PROTOCOL HUẤN LUYỆN VÀ KIỂM THỬ CHÍNH THỨC
5. Tôi chốt ba thí nghiệm riêng cho đồ án
Đây là phần quan trọng nhất. Chúng ta sẽ không chỉ có một mô hình và một lần kiểm tra.
Experiment 01 – PlantVillage Baseline
Bắt buộc
Đánh giá mô hình trong cùng domain
PlantVillage

54.306 ảnh theo công bố

Train – 90% của official train

Dữ liệu cập nhật trọng số

Validation – 10% của official train

Lựa chọn mô hình và hyperparameters

Official Test – 10.709 ảnh

Chỉ đánh giá cuối cùng


Mục tiêu: Xác định mô hình có học đúng 38 lớp hay không, có bị overfitting không và hiệu năng nội bộ đạt mức nào.

Experiment 02 – Cross-Domain Generalization
Bắt buộc
Đánh giá khả năng hoạt động trên ảnh thực tế hơn
PlantVillage Train

Model đã được huấn luyện và đóng băng.


PlantDoc Official Test

Chỉ giữ ảnh có nhãn đối chiếu được với model.


Mục tiêu: Kiểm tra ảnh thực tế có gây giảm độ chính xác hay không, những class nào thường bị nhầm và mức domain shift lớn đến đâu.

Experiment 03 – Open-set Evaluation
Bắt buộc nếu muốn xử lý cây chưa hỗ trợ
Known classes

38 lớp đã học từ PlantVillage.

Unknown disease

Các tình trạng không có lớp tương ứng.

Unknown crop

Cassava, Rice hoặc cây ngoài phạm vi.

Non-leaf / Non-plant

Ảnh không phù hợp.


Mục tiêu: Xác định tỷ lệ mô hình phát hiện và từ chối chính xác các trường hợp không được hỗ trợ.

Điểm quan trọng: Trong Experiment 02, không lấy PlantDoc train để tinh chỉnh mô hình. Trong Experiment 03, không lấy những ảnh OOD test để chọn threshold. Các biến thể mô hình phải được chốt bằng validation trước khi chạy tập test cuối cùng.
6. Protocol chi tiết cho Experiment 01
Bước 1: Sử dụng dữ liệu RGB
Chỉ sử dụng cấu hình color của PlantVillage làm dataset chính.

Không gộp:
- color
- grayscale
- segmented
thành ba nguồn ảnh độc lập, vì chúng có thể là các phiên bản biến đổi của cùng hình ảnh lá. Nếu bị chia vào các tập khác nhau, mô hình có thể nhìn thấy một phiên bản trong train và một phiên bản khác trong test.

Nếu muốn nghiên cứu tác động của ảnh grayscale hoặc segmented, thực hiện thành thí nghiệm riêng, có cùng protocol chia nhóm lá.
Bước 2: Chia Train và Validation
PlantVillage đã có 43.596 ảnh train. Chia tiếp:
Phần	Tỷ lệ trong official train	Số lượng xấp xỉ
Train	90%	39.236
Validation	10%	4.360

Không chia đơn thuần theo ảnh. Phải đảm bảo các ảnh của cùng một chiếc lá không bị nằm ở cả hai tập.

Nguồn PlantVillage có leaf_id và official split được thiết kế để giữ các ảnh cùng lá trong một nhóm. 

GitHub+1

Bước 3: Huấn luyện mô hình
Thực hiện tối thiểu hai mô hình:
Mô hình	Mục đích
CNN baseline	Làm mô hình đối chứng
EfficientNet-B0	Mô hình chính sử dụng Transfer Learning

Có thể bổ sung ResNet50 nếu đủ thời gian.

Cần sử dụng cùng một dataset split, quy tắc preprocessing và phương pháp đánh giá để phép so sánh có ý nghĩa.
Bước 4: Validation
Mỗi epoch lưu:
- Train Loss.
- Validation Loss.
- Train Accuracy.
- Validation Accuracy.
- Validation Macro-F1.
- Learning rate.
Ưu tiên chọn model theo Validation Macro-F1 hoặc một tiêu chí đã định trước, không chọn chỉ vì Accuracy cao.

Nếu train accuracy tiếp tục tăng nhưng validation loss tăng và validation F1 giảm, đó là dấu hiệu overfitting.
Bước 5: Test nội bộ
Sau khi lựa chọn xong mô hình, chạy official test 10.709 ảnh.

Tính:
- Accuracy.
- Precision.
- Recall.
- Macro-F1.
- Weighted-F1.
- Top-3 Accuracy.
- Confusion Matrix.
- Classification Report theo từng class.
Không tiếp tục điều chỉnh mô hình bằng kết quả test này.
7. Protocol chi tiết cho Experiment 02
PlantDoc là dữ liệu thử thách hơn vì ảnh có nhiều loại nền, ánh sáng và góc chụp. Bộ dữ liệu này ban đầu được công bố với train/test chứ không có validation chính thức; một bản đóng gói lại ghi nhận 2.342 ảnh train và 236 ảnh test. 

arXiv+1

Quy trình:

Bước 1: Giữ nguyên mô hình đã được huấn luyện từ PlantVillage.

Bước 2: Lấy PlantDoc/test.

Bước 3: Dùng label_mapping.yaml để xác định những class có thể đối chiếu chính xác.

Bước 4: Không đưa các class không tương ứng vào phép tính Accuracy closed-set.

Bước 5: Chạy inference toàn bộ ảnh thuộc các class đã mapping.

Bước 6: Đánh giá bằng Macro-F1, Accuracy, per-class Recall, confusion matrix và confidence intervals.

Các class không đối chiếu được chuyển sang nhóm unknown để kiểm tra khả năng từ chối dự đoán, không được xóa bỏ khỏi toàn bộ nghiên cứu.
Điều đặc biệt cần lưu ý về số lượng ảnh
Có sự khác nhau giữa số lượng ảnh ở bài báo gốc, repository và các bản đóng gói lại của PlantDoc. Ví dụ, một bản mirror kiểm kê 2.578 ảnh với 28 lớp, trong khi bài báo gốc công bố 2.598 ảnh. Bản mirror còn ghi nhận nguy cơ mất sáu ảnh do tên file chỉ khác nhau về chữ hoa/chữ thường trên hệ thống filesystem không phân biệt hoa thường. 

arXiv+1

Vì vậy, trước khi huấn luyện phải có một báo cáo kiểm kê dữ liệu thực tế. Với môi trường Windows, nên clone và kiểm tra PlantDoc trong WSL2/Linux filesystem hoặc Colab, sau đó đối chiếu số lượng bằng manifest. Không mặc định rằng git clone trên NTFS đã giữ nguyên toàn bộ ảnh.
8. Experiment 03 – Có nên cho PlantDoc vào Train không?
Có, nhưng chỉ trong một thí nghiệm riêng.

Sau khi có mô hình baseline, ta có thể xây dựng một mô hình thứ hai:

Model A: PlantVillage-only.

Model B: PlantVillage + PlantDoc train.

Mục tiêu là so sánh việc bổ sung ảnh tự nhiên có cải thiện khả năng nhận diện thực địa hay không.

Protocol cho Model B:
Tập	Nguồn
Train	PlantVillage train + PlantDoc train
Validation	Tách riêng từ dữ liệu train, bảo đảm không trùng ảnh/nhóm
Test nội bộ	PlantVillage official test
Test thực tế	PlantDoc official test

PlantDoc official test phải luôn được giữ ngoài quá trình huấn luyện và lựa chọn mô hình.

Khi so sánh hai model, phải:
- Dùng cùng tập class đã harmonize.
- Cố định official test.
- Không dùng điểm test để điều chỉnh lại hyperparameters.
- So sánh macro-F1 và per-class recall, không chỉ Accuracy.
Điều cần chứng minh: Việc bổ sung dữ liệu ngoài thực địa có giúp mô hình tổng quát hóa tốt hơn hay không.

Đây là một phần thực nghiệm rất có giá trị cho đồ án vì bạn có thể so sánh ba kết quả:
Mô hình	Dữ liệu huấn luyện
Model A	PlantVillage
Model B	PlantVillage + PlantDoc train
Model C	PlantVillage + PlantDoc train + augmentation có kiểm soát

Sau đó đánh giá trên cùng một tập PlantDoc test đã giữ kín.

Lưu ý, model B và C là các thử nghiệm cải thiện. Chúng không được phép sử dụng PlantDoc test để lựa chọn cấu hình.

PHẦN C. TRAINING PIPELINE VÀ CẤU TRÚC BACKEND
9. Cấu trúc thư mục Machine Learning
Tôi muốn tách hẳn quá trình huấn luyện AI thành một module độc lập. Không để code xử lý dataset nằm lẫn trong API FastAPI.

Cấu trúc đề xuất:
smart-plant-care/
│
├── ml/
│   │
│   ├── configs/
│   │   ├── dataset.yaml
│   │   ├── training.yaml
│   │   ├── evaluation.yaml
│   │   ├── ood.yaml
│   │   └── label_mapping.yaml
│   │
│   ├── data/
│   │   ├── raw/
│   │   │   ├── plantvillage/
│   │   │   │   └── color/
│   │   │   ├── plantdoc/
│   │   │   │   ├── train/
│   │   │   │   └── test/
│   │   │   └── ood/
│   │   │       ├── cassava/
│   │   │       ├── rice/
│   │   │       └── non_leaf/
│   │   │
│   │   ├── interim/
│   │   │   ├── verified/
│   │   │   ├── corrupted/
│   │   │   └── duplicates/
│   │   │
│   │   ├── processed/
│   │   │   ├── pv38/
│   │   │   ├── plantdoc_aligned/
│   │   │   └── ood/
│   │   │
│   │   └── manifests/
│   │       ├── plantvillage_manifest.csv
│   │       ├── plantdoc_manifest.csv
│   │       ├── ood_manifest.csv
│   │       ├── train.csv
│   │       ├── validation.csv
│   │       └── test.csv
│   │
│   ├── notebooks/
│   │   ├── 01_dataset_inspection.ipynb
│   │   ├── 02_eda.ipynb
│   │   ├── 03_label_mapping.ipynb
│   │   ├── 04_preprocessing.ipynb
│   │   ├── 05_cnn_baseline.ipynb
│   │   ├── 06_efficientnet_training.ipynb
│   │   ├── 07_cross_domain_evaluation.ipynb
│   │   └── 08_ood_evaluation.ipynb
│   │
│   ├── src/
│   │   ├── data/
│   │   │   ├── download.py
│   │   │   ├── inventory.py
│   │   │   ├── validate_images.py
│   │   │   ├── deduplicate.py
│   │   │   ├── normalize_labels.py
│   │   │   ├── create_splits.py
│   │   │   └── dataset.py
│   │   │
│   │   ├── models/
│   │   │   ├── cnn.py
│   │   │   ├── resnet.py
│   │   │   └── efficientnet.py
│   │   │
│   │   ├── training/
│   │   │   ├── trainer.py
│   │   │   ├── loss.py
│   │   │   ├── optimizer.py
│   │   │   └── callbacks.py
│   │   │
│   │   ├── evaluation/
│   │   │   ├── classification.py
│   │   │   ├── cross_domain.py
│   │   │   ├── calibration.py
│   │   │   ├── ood.py
│   │   │   └── explainability.py
│   │   │
│   │   └── inference/
│   │       ├── predictor.py
│   │       ├── preprocessing.py
│   │       └── model_loader.py
│   │
│   ├── artifacts/
│   │   ├── experiments/
│   │   ├── models/
│   │   └── reports/
│   │
│   ├── requirements.txt
│   └── README.md
│
├── backend/
│   └── app/
│       ├── api/
│       ├── database/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       └── ml/
│           ├── model_loader.py
│           ├── predictor.py
│           ├── image_validator.py
│           ├── ood_detector.py
│           └── inference_service.py
│
└── docs/
    ├── dataset_card.md
    ├── dataset_audit.md
    ├── label_mapping.md
    ├── training_protocol.md
    ├── evaluation_report.md
    └── model_card.md


ml/ chịu trách nhiệm nghiên cứu và huấn luyện.

backend/app/ml/ chỉ nhận model đã huấn luyện, thực hiện inference và trả kết quả cho API.

Không chạy training model trong lúc người dùng upload ảnh.
10. Quy trình xử lý dữ liệu trước khi Train
Đây là pipeline bắt buộc. AI coding agent phải làm đúng trình tự.
#chatgpt-mermaid-_r_nn_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_nn_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_nn_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_nn_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-_r_nn_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_nn_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_nn_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_nn_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_nn_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_nn_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_nn_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_nn_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_nn_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_nn_ p{margin:0;}#chatgpt-mermaid-_r_nn_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_nn_ .label text,#chatgpt-mermaid-_r_nn_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ .node rect,#chatgpt-mermaid-_r_nn_ .node circle,#chatgpt-mermaid-_r_nn_ .node ellipse,#chatgpt-mermaid-_r_nn_ .node polygon,#chatgpt-mermaid-_r_nn_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-_r_nn_ .rough-node .label text,#chatgpt-mermaid-_r_nn_ .node .label text,#chatgpt-mermaid-_r_nn_ .image-shape .label,#chatgpt-mermaid-_r_nn_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_nn_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_nn_ .rough-node .label,#chatgpt-mermaid-_r_nn_ .node .label,#chatgpt-mermaid-_r_nn_ .image-shape .label,#chatgpt-mermaid-_r_nn_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_nn_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_nn_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_nn_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-_r_nn_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-_r_nn_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-_r_nn_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_nn_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-_r_nn_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_nn_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-_r_nn_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-_r_nn_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_nn_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-_r_nn_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_nn_ .icon-shape,#chatgpt-mermaid-_r_nn_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-_r_nn_ .icon-shape p,#chatgpt-mermaid-_r_nn_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-_r_nn_ .icon-shape .label rect,#chatgpt-mermaid-_r_nn_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-_r_nn_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_nn_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_nn_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-_r_nn_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_nn_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_nn_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_nn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_nn_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_nn_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_nn_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_nn_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_nn_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-_r_nn_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_nn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_nn_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_nn_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_nn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_nn_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_nn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_nn_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_nn_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-_r_nn_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_nn_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_nn_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-_r_nn_ .node rect,#chatgpt-mermaid-_r_nn_ .node circle,#chatgpt-mermaid-_r_nn_ .node ellipse,#chatgpt-mermaid-_r_nn_ .node polygon,#chatgpt-mermaid-_r_nn_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_nn_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_nn_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_nn_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_nn_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-_r_nn_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Download datasetsDataset InventoryImage ValidationDuplicate DetectionLabel NormalizationLabel Mapping ReviewData Quality ReportGroup-aware Data SplittingPreprocessingAugmentation - Train onlyPyTorch DataLoaderTraining





10.1. Dataset Inventory
Tự động thống kê:
- Tổng số ảnh.
- Tổng số cây.
- Tổng số class.
- Số ảnh theo từng class.
- Số ảnh train/test của từng class.
- Số ảnh theo nguồn.
- Kích thước ảnh.
- Định dạng ảnh.
Kết quả cần xuất:
dataset_statistics.json
class_distribution.csv
dataset_inventory.csv


10.2. Image Validation
Kiểm tra:
- Ảnh đọc được.
- File không bị hỏng.
- Kích thước hợp lệ.
- Có thể chuyển sang RGB.
- Không bị trùng lặp bất thường.
- Không phải file rác hoặc ảnh không liên quan.
Các ảnh bị loại phải lưu lại lý do.
10.3. Duplicate Detection
Phải sử dụng ít nhất hai cách:
- SHA256: phát hiện các file giống nhau hoàn toàn.
- Perceptual Hash (pHash): phát hiện ảnh giống hoặc gần giống dù đã thay đổi kích thước hoặc nén.
Đặc biệt phải kiểm tra trùng lặp giữa PlantVillage và PlantDoc. Nếu hai dataset chứa cùng một hình ảnh, không được để một bản tham gia train và bản kia tham gia cross-domain test.
10.4. Data Manifest
Tôi muốn bắt AI tạo một file CSV quản lý toàn bộ ảnh thay vì để việc chia tập phụ thuộc vào thứ tự thư mục.

Ví dụ:
image_id	dataset	plant	disease	class_id	split
pv_0001	PV	tomato	early_blight	28	train
pv_0002	PV	tomato	healthy	37	train
pd_0001	PD	tomato	early_blight	28	external_test
pd_0002	PD	potato	late_blight	21	external_test

Các cột đầy đủ cần có:
image_id
image_path
dataset_source
dataset_version
original_label
canonical_label
plant_species
disease_name
class_index
sha256
perceptual_hash
group_id
split
license
quality_status
exclude_reason


Cách này giúp theo dõi chính xác một hình ảnh thuộc dataset nào, nhãn gốc là gì và được đưa vào tập nào.
11. Training configuration đề xuất
Không nên để AI tự đặt tham số tùy tiện cho mỗi lần chạy.

Tạo một cấu hình cố định để có thể tái lập thực nghiệm:
dataset:
  primary: plantvillage
  config: color
  num_classes: 38

  validation_ratio: 0.10
  use_official_test: true
  group_aware_split: true

image:
  size: 224
  channels: 3

training:
  model: efficientnet_b0
  pretrained: true

  epochs: 40
  batch_size: 32

  optimizer: AdamW
  learning_rate: 0.0001
  weight_decay: 0.0001

  loss: cross_entropy
  early_stopping_patience: 7

  seed: 42

evaluation:
  primary_metric: macro_f1
  metrics:
    - accuracy
    - precision
    - recall
    - macro_f1
    - weighted_f1
    - top_3_accuracy

  confusion_matrix: true
  classification_report: true


Các tham số này là điểm bắt đầu, cần điều chỉnh theo GPU và kết quả validation.

Phần data augmentation ban đầu:
train_transforms = [    "Resize",    "RandomHorizontalFlip",    "RandomRotation",    "ColorJitter",    "Normalize"]validation_transforms = [    "Resize",    "Normalize"]test_transforms = [    "Resize",    "Normalize"]



Chỉ sử dụng augmentation trong train. Validation và test không được thay đổi ngẫu nhiên.

Nếu dữ liệu mất cân bằng, thử:
- Class-weighted Cross Entropy.
- Weighted Random Sampler.
- Focal Loss khi cần.
Phải báo cáo rõ phương pháp nào được sử dụng. Không nên áp dụng tất cả cùng lúc mà không có thực nghiệm so sánh.

PHẦN D. ĐÁNH GIÁ MÔ HÌNH VÀ TIÊU CHÍ ĐẠT
12. Những chỉ số phải có
Đối với đồ án này, tôi không chấp nhận chỉ có một con số Accuracy.

Phải có bảng đánh giá đầy đủ.
Chỉ số	Ý nghĩa
Accuracy	Tỷ lệ dự đoán chính xác chung
Precision	Mức độ chính xác khi dự đoán một lớp
Recall	Khả năng tìm được mẫu thật sự thuộc lớp
Macro-F1	Đánh giá công bằng giữa các lớp
Weighted-F1	F1 có tính đến số lượng mẫu từng lớp
Top-3 Accuracy	Nhãn thật có nằm trong ba dự đoán cao nhất
Confusion Matrix	Phân tích các lớp bị nhầm lẫn
ECE	Đo độ lệch hiệu chỉnh confidence
Brier Score	Đánh giá chất lượng xác suất dự đoán
Inference Time	Thời gian phân tích mỗi ảnh

Trong đồ án này, tôi đặc biệt chú trọng Macro-F1 và Recall theo từng lớp.

Ví dụ:

Giả sử mô hình có 100 ảnh cà chua, 100 ảnh khoai tây nhưng chỉ có 10 ảnh táo.

Nếu mô hình đoán rất tốt cà chua, khoai tây nhưng đoán sai gần hết ảnh táo, Accuracy chung vẫn có thể cao. Macro-F1 sẽ phản ánh rõ hơn sự yếu kém ở các lớp ít dữ liệu.
12.1. Confusion Matrix
Ví dụ mô hình thường nhầm:
- Tomato Early Blight với Tomato Septoria.
- Potato Early Blight với Potato Late Blight.
- Tomato Healthy với Tomato Leaf Mold.
Phải tìm hiểu nguyên nhân:
- Hai bệnh có triệu chứng trực quan tương tự.
- Vùng bệnh quá nhỏ.
- Chất lượng ảnh kém.
- Nhãn dữ liệu chưa chính xác.
- Mất cân bằng dữ liệu.
- Mô hình học đặc điểm nền thay vì bệnh.
Sau đó đề xuất cải tiến tương ứng.
12.2. Đánh giá độ tin cậy
Confidence không đồng nghĩa với độ chính xác.

Ví dụ model dự đoán 95% nhưng thực tế kết quả đúng chỉ 70% trên một nhóm ảnh. Điều này thể hiện mô hình chưa được calibration tốt.

Cần nghiên cứu:
- Temperature Scaling.
- Expected Calibration Error.
- Reliability Diagram.
- Brier Score.
Chọn calibration trên validation, không được dùng test để đặt ngưỡng.
13. Accuracy bao nhiêu mới được xem là đạt?
Không tồn tại một ngưỡng Accuracy chung được quy định cho mọi đề tài AI nhận diện bệnh thực vật.

Tôi đề xuất những mốc nghiệm thu nội bộ sau. Đây là mục tiêu của đồ án, không phải tiêu chuẩn quốc tế hoặc kết quả đã đạt được.
Mốc 1 – In-domain PlantVillage
Mục tiêu đề xuất
≥95%
Accuracy

≥0.93
Macro-F1


Yêu cầu thêm: kiểm tra Recall theo lớp, confusion matrix, không có data leakage và không có chênh lệch quá lớn giữa train và validation.

Mốc 2 – Cross-domain PlantDoc
Mục tiêu nghiên cứu
≥50%
Macro-F1 mục tiêu ban đầu

≥60%
Mục tiêu cải thiện


Không coi đây là ngưỡng chuẩn bắt buộc. Cần xem xét số mẫu mỗi lớp, khoảng tin cậy và chất lượng mapping.

Mốc 3 – OOD Detection
≥0.85
OOD AUROC mục tiêu

≤10%
False acceptance mục tiêu ở operating point đã chọn


Cần báo cáo thêm tỷ lệ từ chối nhầm ảnh thuộc lớp đã hỗ trợ. Không được tối ưu false acceptance bằng cách từ chối gần như mọi ảnh.

Có một kết quả nghiên cứu cần đặc biệt lưu ý: bài báo PlantVillage năm 2016 báo cáo Accuracy 99,35% trên tập kiểm thử cùng nguồn, nhưng khi kiểm tra 121 ảnh bên ngoài được thu thập trong điều kiện khác, Accuracy chỉ còn 31,4%. Đây là minh chứng rất rõ cho việc đạt 99% trên dataset không có nghĩa ứng dụng sẽ đạt 99% ngoài thực tế. 

Frontiers+1

Vì vậy, đừng cố chạy model đến khi có 99% rồi dừng. Mục tiêu của chúng ta là biết chính xác mô hình tốt ở đâu, yếu ở đâu và có đáng tin cậy khi người dùng chụp ảnh bằng điện thoại hay không.
14. Những báo cáo bắt buộc phải xuất ra
Sau khi hoàn thành training và evaluation, cần có các file:
artifacts/
│
├── models/
│   ├── cnn_baseline.pth
│   ├── efficientnet_best.pth
│   ├── class_mapping.json
│   ├── preprocessing.json
│   ├── thresholds.json
│   └── model_metadata.json
│
├── reports/
│   ├── dataset_inventory.csv
│   ├── class_distribution.csv
│   ├── data_quality_report.pdf
│   ├── leakage_audit.json
│   ├── training_history.csv
│   ├── classification_report.csv
│   ├── confusion_matrix.png
│   ├── accuracy_loss_curves.png
│   ├── model_comparison.csv
│   ├── plantdoc_cross_domain.csv
│   ├── ood_evaluation.csv
│   └── final_evaluation_report.pdf
│
└── experiments/
    ├── experiment_01/
    ├── experiment_02/
    └── experiment_03/


Cần có:
- Thời gian huấn luyện.
- Cấu hình máy.
- Phiên bản thư viện.
- Seed.
- Phiên bản dataset.
- Số ảnh đã sử dụng.
- Số ảnh bị loại.
- Checkpoint tốt nhất.
- Các kết quả đánh giá.
Đây là bằng chứng quan trọng để đưa vào báo cáo và giải trình với giảng viên.

PHẦN E. BACKEND SAU KHI MODEL ĐẠT YÊU CẦU
15. Thiết kế AI Inference Service
Sau khi đã khóa được model tốt nhất, mới tích hợp vào FastAPI.

Backend cần có module:
backend/app/ml/
│
├── model_loader.py
├── model_registry.py
├── image_validator.py
├── preprocessing.py
├── plant_classifier.py
├── disease_classifier.py
├── ood_detector.py
├── confidence_calibrator.py
├── gradcam_service.py
└── inference_service.py


Ở phiên bản đầu, plant_classifier và disease_classifier có thể dùng chung một mô hình 38 lớp crop-disease, sau đó phân tích class ID để tách tên cây và bệnh.
Quy trình một request
1. Nhận ảnh từ frontend.
2. Kiểm tra MIME, kích thước và chất lượng.
3. Đọc ảnh, chuyển RGB.
4. Resize và normalize.
5. Chạy model inference.
6. Lấy Top 3.
7. Chạy OOD evaluation.
8. Calibration confidence.
9. Xác định trạng thái dự đoán.
10. Lưu kết quả.
11. Trả JSON.
Response API phải phân biệt các trạng thái
{
  "status": "diagnosed",
  "plant": {
    "id": "tomato",
    "name": "Cà chua"
  },
  "disease": {
    "id": "tomato_early_blight",
    "name": "Early Blight"
  },
  "prediction": {
    "confidence": 0.948,
    "top_k": []
  },
  "model_version": "1.0.0"
}


Các trạng thái khác:
diagnosed
healthy
uncertain
unsupported_crop
unknown_disease
invalid_image
poor_image_quality


Ví dụ người dùng gửi ảnh lá sắn:
{
  "status": "unsupported_crop",
  "message": "Loại cây này chưa nằm trong phạm vi hỗ trợ của mô hình.",
  "prediction": null
}


Backend không được trả về một bệnh cà chua chỉ vì mô hình Softmax chọn Tomato là lớp có xác suất cao nhất.
Database cần lưu thông tin đánh giá
Bảng model_versions:
id
model_name
model_version
architecture
dataset_version
class_count
weights_path
preprocessing_config
threshold_config
accuracy
macro_precision
macro_recall
macro_f1
cross_domain_macro_f1
ood_auroc
created_at
status


Mỗi lần dự đoán phải lưu phiên bản model đã sử dụng để sau này có thể so sánh kết quả giữa những phiên bản AI khác nhau.

PHẦN F. CÓ NÊN SỬ DỤNG BA REPOSITORY CODE ĐÃ GỬI KHÔNG?
Tôi đã kiểm tra README của ba dự án. Đánh giá vai trò của từng repository như sau:
Repository	Sử dụng cho
pkparthk	Tham khảo kiến trúc FastAPI, React, API, model integration
manthan89-py	Tham khảo CNN PyTorch và quá trình huấn luyện PlantVillage
zawrabh	Tham khảo CNN, TensorFlow/Keras và inference

Có một điểm cần chú ý: manthan89-py mô tả mô hình 39 categories, trong khi PlantVillage được công bố với 38 lớp. Phải kiểm tra class mapping của repository này trước khi dùng lại trọng số. 

GitHub+1

Repository pkparthk còn liệt kê Mango Anthracnose, Citrus Canker và Rice Blast trong các bệnh hỗ trợ, nghĩa là không thể mặc định toàn bộ các lớp của nó xuất phát từ PlantVillage. Cần kiểm tra nguồn dữ liệu và pipeline mở rộng trước khi sử dụng. 

GitHub

Kết luận: Không nên dùng model đã train của ba repository làm kết quả cuối cùng của đồ án. Hãy dùng chúng làm tài liệu tham khảo, tự xây dựng dataset manifest, pipeline train, đánh giá và lưu model của riêng mình.

PHẦN G. THỨ TỰ TRIỂN KHAI CHÍNH THỨC
Tôi đồng ý với hướng bạn vừa đưa ra: chưa cần làm frontend và deploy bây giờ.

Tôi đề xuất khóa tiến độ theo từng cổng nghiệm thu.
AI-first development roadmap
1. MILESTONE 1 – Dataset Audit
   Ưu tiên số 1
   - Download PlantVillage.
   - Download PlantDoc.
   - Download nguồn OOD.
   - Kiểm kê dữ liệu.
   - Kiểm tra class.
   - Kiểm tra trùng ảnh.
   - Chuẩn hóa label.
   - Tạo manifest.
   - Tạo báo cáo EDA.
   Đầu ra: Dataset được xác minh và có protocol sử dụng.
2. MILESTONE 2 – Data Preprocessing
   - Xây dựng image pipeline.
   - RGB conversion.
   - Resize và normalization.
   - Augmentation.
   - Group-aware splitting.
   - Leakage audit.
   Đầu ra: Train/validation/test được khóa.
3. MILESTONE 3 – Model Training
   - CNN baseline.
   - EfficientNet-B0.
   - Model checkpoint.
   - Training curves.
   - Hyperparameter tuning.
   Đầu ra: Các mô hình đã huấn luyện.
4. MILESTONE 4 – Model Evaluation
   - In-domain test.
   - Cross-domain test.
   - Open-set test.
   - Calibration.
   - Confusion matrix.
   - Model comparison.
   Đầu ra: Báo cáo đánh giá khoa học.
5. MILESTONE 5 – AI Model Finalization
   - Chọn model.
   - Khóa class mapping.
   - Khóa preprocessing.
   - Khóa threshold.
   - Grad-CAM.
   - Xuất model metadata.
   Đầu ra: Model có thể chạy inference độc lập.
6. MILESTONE 6 – Backend Development
   - FastAPI.
   - PostgreSQL.
   - Authentication.
   - AI inference API.
   - Plant management API.
   - Diagnosis history.
   - Analytics API.
   Đầu ra: Backend chạy độc lập và kiểm thử được qua Swagger.
7. MILESTONE 7 – Frontend Development
   - React + TypeScript.
   - Responsive UI.
   - AI Detection.
   - Dashboard.
   - Plant Management.
   - Analytics.
   - Admin.
   Đầu ra: Hoàn chỉnh giao diện người dùng.
8. MILESTONE 8 – Web & Mobile Deployment
   - Docker.
   - Deploy backend.
   - Deploy database.
   - Deploy frontend.
   - PWA.
   - Kiểm thử Android/iOS và laptop.
   Đầu ra: Sản phẩm có thể sử dụng trên nhiều thiết bị.

16. Tiêu chí bắt buộc trước khi được phép làm Frontend
Tôi đề xuất không chuyển sang frontend trước khi các ô sau được hoàn thành:
AI readiness checklist
0/14



[ ] Đã kiểm kê và xác minh PlantVillage, PlantDoc.
[ ] Đã tạo label mapping và xác nhận các class tương ứng.
[ ] Đã phát hiện và xử lý ảnh trùng lặp, ảnh lỗi.
[ ] Đã tạo train/validation/test manifest cố định.
[ ] Đã hoàn thành EDA và báo cáo mất cân bằng lớp.
[ ] Đã huấn luyện CNN baseline.
[ ] Đã huấn luyện và so sánh EfficientNet-B0.
[ ] Đã đánh giá trên PlantVillage official test.
[ ] Đã đánh giá cross-domain bằng PlantDoc test.
[ ] Đã đánh giá khả năng từ chối ảnh OOD.
[ ] Đã có confusion matrix, Macro-F1 và classification report.
[ ] Đã chốt model, preprocessing và class mapping.
[ ] Đã có inference script chạy độc lập.
[ ] Đã có model card và báo cáo thực nghiệm.
Tích vào từng mục khi có bằng chứng kiểm thử.
Reset


17. MASTER PROMPT MỚI – CHỈ TẬP TRUNG DATASET, TRAINING VÀ BACKEND AI
Đây là prompt tôi muốn bạn sử dụng trước tiên với AI coding agent. Nó thay thế yêu cầu xây dựng toàn bộ website ngay lập tức.
AI & DATASET ENGINEERING SPECIFICATION
Phase 1–5

Copy toàn bộ yêu cầu để bắt đầu xây dựng nền tảng AI.
 Copy AI & Dataset Master Prompt

18. Quyết định cuối cùng về Dataset
Tôi chốt phương án cho phiên bản đồ án đầu tiên như sau:
Dataset	Training	Validation	Testing	Mục tiêu
PlantVillage Color	Có	Có	Có	Benchmark nội bộ 38 lớp
PlantDoc	Không ở thí nghiệm đầu	Không ở thí nghiệm đầu	Có	Cross-domain
PlantDoc Train	Thí nghiệm riêng	Tách riêng	Không	Domain adaptation
Cassava	Không đưa vào 38 lớp	OOD calibration riêng	OOD test riêng	Cây chưa hỗ trợ
Rice	Không đưa vào 38 lớp	Có thể dùng tùy protocol	OOD test riêng	Cây chưa hỗ trợ

Kết luận quan trọng nhất:

Chúng ta không xây dựng một mô hình tuyên bố nhận diện tất cả cây trồng. Chúng ta xây dựng một mô hình có phạm vi hỗ trợ xác định, nhận diện được 38 lớp của PlantVillage, kiểm chứng khả năng tổng quát hóa qua PlantDoc, có khả năng từ chối dự đoán ngoài phạm vi đã huấn luyện và có báo cáo thực nghiệm chứng minh từng khả năng đó.

Đây là cách làm vừa có tính học thuật, vừa có tính ứng dụng, tránh tình trạng website chạy được nhưng mô hình AI không đáng tin cậy.

Bước đầu tiên nên làm ngay: tải và kiểm kê PlantVillage Color và PlantDoc, kiểm tra số lượng ảnh, 38 class và danh mục nhãn thực tế, tạo bảng label_mapping.csv và dataset_manifest.csv. Chưa train model cho đến khi hoàn thành bước này.

# **ĐẶC TẢ FRONTEND – BACKEND INTEGRATION**

## **Smart Plant Care AI – Hệ thống nhận diện bệnh và phân tích sức khỏe cây trồng**

Ở giai đoạn này, chúng ta cần thiết kế Frontend không phải như một website độc lập, mà là **một ứng dụng giao tiếp trực tiếp với Backend thông qua REST API**.

Nguyên tắc quan trọng:

- Frontend chịu trách nhiệm giao diện, trải nghiệm người dùng, nhập dữ liệu và hiển thị kết quả.
- Backend chịu trách nhiệm xử lý nghiệp vụ, xác thực, phân quyền, truy vấn Database và gọi AI Model.
- AI Service chịu trách nhiệm xử lý ảnh và dự đoán bệnh.
- Database là nguồn dữ liệu chính thức của hệ thống.
- Frontend không tự tính toán kết quả bệnh, không tự tạo confidence score, không tự giả lập dữ liệu thống kê.

Tôi đề xuất giữ kiến trúc React + TypeScript + FastAPI + PyTorch + PostgreSQL đã thống nhất.

## **1. Kiến trúc kết nối tổng thể**

\#chatgpt-mermaid-\_r_sd\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_sd\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_sd\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_sd\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_sd\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_sd\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_sd\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_sd\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_sd\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_sd\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_sd\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_sd\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_sd\_ p{margin:0;}#chatgpt-mermaid-\_r_sd\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_sd\_ .label text,#chatgpt-mermaid-\_r_sd\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ .node rect,#chatgpt-mermaid-\_r_sd\_ .node circle,#chatgpt-mermaid-\_r_sd\_ .node ellipse,#chatgpt-mermaid-\_r_sd\_ .node polygon,#chatgpt-mermaid-\_r_sd\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ .rough-node .label text,#chatgpt-mermaid-\_r_sd\_ .node .label text,#chatgpt-mermaid-\_r_sd\_ .image-shape .label,#chatgpt-mermaid-\_r_sd\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_sd\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ .rough-node .label,#chatgpt-mermaid-\_r_sd\_ .node .label,#chatgpt-mermaid-\_r_sd\_ .image-shape .label,#chatgpt-mermaid-\_r_sd\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_sd\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_sd\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_sd\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_sd\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_sd\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_sd\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_sd\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_sd\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_sd\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_sd\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_sd\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_sd\_ .icon-shape,#chatgpt-mermaid-\_r_sd\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_sd\_ .icon-shape p,#chatgpt-mermaid-\_r_sd\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_sd\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_sd\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_sd\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_sd\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_sd\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_sd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_sd\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_sd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_sd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_sd\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_sd\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_sd\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_sd\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_sd\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_sd\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_sd\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ .node rect,#chatgpt-mermaid-\_r_sd\_ .node circle,#chatgpt-mermaid-\_r_sd\_ .node ellipse,#chatgpt-mermaid-\_r_sd\_ .node polygon,#chatgpt-mermaid-\_r_sd\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_sd\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_sd\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_sd\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_sd\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_sd\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Backend - FastAPIFrontend - React + TypeScriptMiddlewareAuthentication APIPlant APIDiagnosis APIAnalytics APIAdmin APIBusiness ServicesAI Inference ServiceResponsive UI / PWAReact RouterAuth StateAPI ClientTanStack QueryNgười dùngPostgreSQLPrivate Image StoragePyTorch ModelHTTPS / JSON / Multipart

### **1.1. Luồng xử lý cơ bản**

Ví dụ người dùng muốn kiểm tra bệnh trên lá cà chua:

1. Người dùng mở trang AI Detection trên điện thoại.
2. Frontend cho phép chụp ảnh bằng camera hoặc chọn ảnh trong thư viện.
3. Frontend hiển thị ảnh xem trước và kiểm tra sơ bộ định dạng, dung lượng.
4. Người dùng nhấn Phân tích.
5. Frontend gửi hình ảnh lên API Backend bằng `multipart/form-data`.
6. Backend xác thực người dùng và kiểm tra file.
7. Backend lưu ảnh, gọi AI Inference Service.
8. AI Model trả về kết quả dự đoán và các thông tin đánh giá.
9. Backend kiểm tra trạng thái kết quả, lấy thông tin bệnh tương ứng từ Database.
10. Backend lưu lần chẩn đoán vào Database.
11. Backend trả JSON cho Frontend.
12. Frontend hiển thị tên cây, bệnh, confidence, Top 3, Grad-CAM và hướng dẫn chăm sóc.

**Phân chia trách nhiệm**

Frontend

Chụp ảnh, gửi request, hiển thị kết quả.

Backend

Xác thực, xử lý nghiệp vụ, lưu trữ và quản lý dữ liệu.

AI Service

Tiền xử lý ảnh, phân loại, OOD detection, Grad-CAM.

Database

Tài khoản, cây trồng, lịch sử, bệnh và phiên bản mô hình.

## **2. Công nghệ Frontend và vai trò từng thư viện**

| Công nghệ        | Nhiệm vụ                               |
| ---------------- | -------------------------------------- |
| React            | Xây dựng giao diện theo component      |
| TypeScript       | Kiểm soát kiểu dữ liệu giữa các module |
| Vite             | Build và chạy frontend                 |
| Tailwind CSS     | Thiết kế responsive                    |
| shadcn/ui        | Component giao diện                    |
| React Router     | Quản lý trang và điều hướng            |
| TanStack Query   | Gọi API, caching, loading, refetch     |
| React Hook Form  | Quản lý form                           |
| Zod              | Validate dữ liệu nhập                  |
| Recharts         | Hiển thị biểu đồ                       |
| Axios hoặc Fetch | Giao tiếp Backend                      |
| PWA              | Cài đặt website trên điện thoại        |

Tôi đề xuất dùng TanStack Query để quản lý dữ liệu từ Backend. Không cần lưu tất cả dữ liệu API vào Zustand hoặc Context vì sẽ làm hệ thống khó đồng bộ.

Phân chia state:

- Server state: TanStack Query.
- Authentication state: Auth Context hoặc một auth store nhỏ.
- Form state: React Hook Form.
- UI state: React useState.
- Bộ lọc và phân trang: URL query parameters khi phù hợp.

# **3. Thiết kế toàn bộ Frontend và API tương ứng**

Frontend có ba khu vực: Public, User và Admin.

## **3.1. Public Website**

[AgriAssist – AI Farming Assistant Web Platform — built with](https://images.openai.com/static-rsc-4/MeVKL_TFbawerR4IJ0p4FfKP98hZ1inkPRF7VWhHWdIWcm5l7Y-ucCscqtokFzWcrC9fxWICxdVWtWlnF6yPs5TLOoGGtqYbPWcA5GzkxSXahOBvNh0BVdRZjWzQwUlJGPMmck2fOTcJ48BuMKrWLGLVpjtCQtaMMBygO3bagcw?purpose=inline)

[blink.new](https://blink.new/p/agriassist-ai-farming-platform-1njug2o8?utm_source=chatgpt.com)

| Trang           | Chức năng                | API Backend                         |
| --------------- | ------------------------ | ----------------------------------- |
| Home            | Trang giới thiệu         | `GET /api/v1/public/statistics`     |
| Disease Library | Danh sách bệnh công khai | `GET /api/v1/diseases`              |
| Disease Detail  | Nội dung bệnh            | `GET /api/v1/diseases/{id}`         |
| Login           | Đăng nhập                | `POST /api/v1/auth/login`           |
| Register        | Đăng ký                  | `POST /api/v1/auth/register`        |
| Forgot Password | Quên mật khẩu            | `POST /api/v1/auth/forgot-password` |

Trang chủ có thể lấy dữ liệu thống kê công khai từ Backend, chẳng hạn số cây và số bệnh đang hỗ trợ.

Không được tự đặt số lượng loại cây, số bệnh, Accuracy của mô hình rồi hiển thị như dữ liệu thật.

## **3.2. Authentication – Đăng nhập và quản lý tài khoản**

Luồng đăng nhập:

\#chatgpt-mermaid-\_r_ss\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_ss\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_ss\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_ss\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_ss\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_ss\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_ss\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_ss\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_ss\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_ss\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ss\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ss\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_ss\_ p{margin:0;}#chatgpt-mermaid-\_r_ss\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_ss\_ .label text,#chatgpt-mermaid-\_r_ss\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ .node rect,#chatgpt-mermaid-\_r_ss\_ .node circle,#chatgpt-mermaid-\_r_ss\_ .node ellipse,#chatgpt-mermaid-\_r_ss\_ .node polygon,#chatgpt-mermaid-\_r_ss\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ .rough-node .label text,#chatgpt-mermaid-\_r_ss\_ .node .label text,#chatgpt-mermaid-\_r_ss\_ .image-shape .label,#chatgpt-mermaid-\_r_ss\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_ss\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ .rough-node .label,#chatgpt-mermaid-\_r_ss\_ .node .label,#chatgpt-mermaid-\_r_ss\_ .image-shape .label,#chatgpt-mermaid-\_r_ss\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_ss\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_ss\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ss\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ss\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_ss\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_ss\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_ss\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_ss\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_ss\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_ss\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_ss\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_ss\_ .icon-shape,#chatgpt-mermaid-\_r_ss\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_ss\_ .icon-shape p,#chatgpt-mermaid-\_r_ss\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_ss\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_ss\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_ss\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_ss\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_ss\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_ss\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_ss\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_ss\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_ss\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ss\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_ss\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_ss\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_ss\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_ss\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_ss\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_ss\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ .node rect,#chatgpt-mermaid-\_r_ss\_ .node circle,#chatgpt-mermaid-\_r_ss\_ .node ellipse,#chatgpt-mermaid-\_r_ss\_ .node polygon,#chatgpt-mermaid-\_r_ss\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_ss\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_ss\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_ss\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_ss\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_ss\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Mở LoginNhập Email và PasswordFrontend validatePOST /auth/loginBackend xác thực?Hiển thị lỗiNhận thông tin user và sessionGET /auth/meKiểm tra roleUser DashboardAdmin DashboardKhôngCóUSERADMIN

Các API:

| API                          | Nhiệm vụ               |
| ---------------------------- | ---------------------- |
| `POST /auth/register`        | Đăng ký                |
| `POST /auth/login`           | Đăng nhập              |
| `POST /auth/logout`          | Đăng xuất              |
| `GET /auth/me`               | Lấy tài khoản hiện tại |
| `POST /auth/refresh`         | Làm mới session/token  |
| `PUT /auth/me`               | Sửa hồ sơ              |
| `POST /auth/change-password` | Đổi mật khẩu           |

**Yêu cầu bảo mật:**

Nên sử dụng cookie bảo mật `HttpOnly`, `Secure` khi chạy HTTPS và thiết lập `SameSite` phù hợp để quản lý session. Nếu sử dụng cookie authentication, phải xử lý CSRF phù hợp. Không lưu refresh token vào `localStorage`.

Cả Frontend và Backend đều kiểm tra quyền, nhưng Backend mới là nơi quyết định cuối cùng. Việc ẩn trang Admin trên giao diện không thay thế được phân quyền API.

## **3.3. User Dashboard**

[Agrova - Smart Farming Dashboard by Emura on Dribbble](https://images.openai.com/static-rsc-4/1Cuu8KYGzD0T-how_mBQYy0tAjwNKJuCpoguo_zMKcquzJPnt_BPNfXy8p_JAJ01dd4UPL6bWwhuIjezSpaZ9DIly5v1fptYklJyI0uVCT58Jbv6LiOmrEgNGLDj0mqIpslpC2qB0jtA8ZVH2poxMUtTo-oqAC5L3ivxT8hkIG8?purpose=inline)

[dribbble.com](https://dribbble.com/shots/27189397-Agrova-Smart-Farming-Dashboard?utm_source=chatgpt.com)

Khi đăng nhập thành công, Frontend gọi:

`GET /api/v1/analytics/dashboard`

Backend tổng hợp dữ liệu của tài khoản đang đăng nhập và trả về:

```
{
  "total_plants": 12,
  "total_scans": 86,
  "healthy_scans": 54,
  "disease_detected_scans": 27,
  "uncertain_scans": 5,
  "recent_scans": [],
  "disease_distribution": [],
  "scan_trend": []
}
```

Đây là ví dụ cấu trúc response, chưa phải dữ liệu thực tế.

Frontend hiển thị:

- Tổng số cây đang theo dõi.
- Tổng lượt kiểm tra.
- Số lượt nhận diện khỏe mạnh.
- Số lượt phát hiện dấu hiệu bệnh.
- Số lượt chưa đủ độ tin cậy.
- Biểu đồ lịch sử kiểm tra.
- Biểu đồ phân bố bệnh.
- Hoạt động gần đây.
- Nút chuyển nhanh sang AI Detection.

Khi mở Dashboard, không nên gọi từng API riêng lẻ cho mỗi thẻ thống kê nếu Backend có thể tổng hợp trong một endpoint phù hợp.

Quan trọng: Thống kê phải là dữ liệu lấy từ Database, không phải các con số viết cứng trong React.

# **4. Tích hợp quan trọng nhất: Frontend AI Detection với Backend AI**

Đây là luồng phải được thiết kế và kiểm thử kỹ nhất.

## **4.1. Giao diện AI Detection**

["KrishiMitra AI," an AI-powered personal assistant to farmer | Devpost](https://images.openai.com/static-rsc-4/k6QPj6iTE6KXqhEo0F01ymXygA4SQMdBICVW1sU0EOH2IDF8QzQqbspKTLo42kSha9FjHwVPZiBH_T3SSLVT30EhLFLlL3YRkgf-Z74TKRShTczQRa05v81sicGA-Z69xHsRkCLv7LSKA-YVuFvFkOPho10aIj06i1kaC0q7hLY?purpose=inline)

[devpost.com](https://devpost.com/software/krishimitra-ai-an-ai-powered-personal-assistant-to-farmer?utm_source=chatgpt.com)

Frontend cần có:

- Khu vực kéo thả ảnh trên máy tính.
- Nút chọn ảnh từ thiết bị.
- Nút chụp ảnh bằng camera trên điện thoại.
- Xem trước hình ảnh.
- Xóa hoặc thay ảnh.
- Chọn loại cây, nếu người dùng biết.
- Chọn cây đang được quản lý.
- Nhập ghi chú.
- Nút Phân tích bằng AI.

Ví dụ input:

```
POST /api/v1/diagnoses/predict

Content-Type: multipart/form-data

image: tomato_leaf.jpg
expected_plant: tomato
user_plant_id: 125
notes: Lá xuất hiện nhiều đốm nâu
```

`expected_plant` là thông tin người dùng cung cấp để hỗ trợ kiểm tra sự phù hợp, không phải nhãn mà Backend được phép tin tưởng tuyệt đối.

Nếu người dùng chọn Tomato nhưng mô hình nhận diện một cây khác hoặc không đủ tin cậy, Backend phải xử lý tình huống đó thay vì ép kết quả thành Tomato.

## **4.2. Frontend gửi ảnh lên Backend thế nào?**

Ví dụ code TypeScript:

```
export interface PredictRequest {
  image: File;
  expectedPlant?: string;
  userPlantId?: number;
  notes?: string;
}

export async function predictPlantDisease(
  payload: PredictRequest
) {
  const formData = new FormData();

  formData.append("image", payload.image);

  if (payload.expectedPlant) {
    formData.append(
      "expected_plant",
      payload.expectedPlant
    );
  }

  if (payload.userPlantId) {
    formData.append(
      "user_plant_id",
      String(payload.userPlantId)
    );
  }

  if (payload.notes) {
    formData.append("notes", payload.notes);
  }

  const response = await fetch(
    `${import.meta.env.VITE_API_BASE_URL}/api/v1/diagnoses/predict`,
    {
      method: "POST",
      credentials: "include",
      body: formData
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.detail ?? "Không thể phân tích hình ảnh."
    );
  }

  return response.json();
}
```

Không tự thiết lập header `Content-Type: multipart/form-data` khi gửi `FormData` bằng Fetch; trình duyệt phải tự tạo boundary.

Phần code trên là mẫu giao tiếp. Cần bổ sung kiểu response, xử lý lỗi thống nhất, timeout và cấu hình CSRF theo phương thức xác thực thực tế.

## **4.3. Backend nhận và xử lý như thế nào?**

```
POST /api/v1/diagnoses/predict
            |
            v
Validate user authentication
            |
            v
Validate image file
            |
            v
Check file size and image content
            |
            v
Image quality validation
            |
            v
Save private image
            |
            v
Load image and preprocessing
            |
            v
Run PyTorch model inference
            |
            v
Run OOD and confidence checks
            |
            v
Map class_id to plant and disease
            |
            v
Generate Grad-CAM if applicable
            |
            v
Save diagnosis and predictions
            |
            v
Return response JSON
```

AI không trả lời bằng cách tự tạo đoạn văn tùy ý. Model trả về kết quả có cấu trúc, Backend ánh xạ kết quả sang thông tin bệnh đã được quản lý trong Database.

## **4.4. Thiết kế response chuẩn**

Backend phải có response contract thống nhất để Frontend không phải đoán cấu trúc dữ liệu.

Ví dụ kết quả phát hiện bệnh:

```
{
  "diagnosis_id": 1058,
  "status": "diagnosed",
  "plant": {
    "id": "tomato",
    "name": "Cà chua"
  },
  "disease": {
    "id": "tomato_early_blight",
    "name": "Early Blight",
    "name_vi": "Bệnh đốm vòng sớm"
  },
  "prediction": {
    "confidence": 0.948,
    "top_k": [
      {
        "class_id": "tomato_early_blight",
        "confidence": 0.948
      },
      {
        "class_id": "tomato_late_blight",
        "confidence": 0.032
      },
      {
        "class_id": "tomato_healthy",
        "confidence": 0.020
      }
    ]
  },
  "image": {
    "original_url": "/api/v1/images/1058/original",
    "explanation_url": "/api/v1/diagnoses/1058/explanation"
  },
  "model": {
    "name": "efficientnet_b0",
    "version": "1.0.0"
  },
  "created_at": "2026-11-24T09:00:00Z"
}
```

Confidence ở đây phải là giá trị thật do AI Service trả về và đã được xử lý theo calibration đã chọn. Không được Frontend tự đặt 94,8%.

### **Frontend phải xử lý tất cả các trạng thái**

| Backend status       | Frontend hiển thị                              |
| -------------------- | ---------------------------------------------- |
| `diagnosed`          | Có dấu hiệu bệnh, hiển thị bệnh được dự đoán   |
| `healthy`            | Mô hình nhận diện mẫu thuộc lớp khỏe mạnh      |
| `uncertain`          | Chưa đủ độ tin cậy để kết luận                 |
| `unsupported_crop`   | Loại cây ngoài phạm vi hỗ trợ                  |
| `unknown_disease`    | Không nhận diện được bệnh thuộc các lớp hỗ trợ |
| `poor_image_quality` | Ảnh không đạt chất lượng                       |
| `invalid_image`      | File không hợp lệ                              |

Không phải tất cả các tình trạng đều trả HTTP 200. Ví dụ file hỏng hoặc định dạng không được hỗ trợ có thể trả HTTP 400/415; file vượt giới hạn trả HTTP 413. Những trạng thái dự đoán hợp lệ như uncertain có thể trả HTTP 200.

Đối với `unsupported_crop` hoặc `unknown_disease`, không hiển thị tên bệnh như một kết luận đã xác nhận.

## **4.5. Các trạng thái giao diện trong quá trình dự đoán**

**State 1 – Chưa chọn ảnh**

**Tải ảnh lá cây lên**

PNG, JPG, WEBP – theo giới hạn hệ thống

Choose image

**State 2 – Ảnh đã chọn**

[Why Do Tomato Leaves Have Spots and Turn Brown? Causes & Fixes  – trailingpetunia.com](https://images.openai.com/static-rsc-4/icFqVdSiag3S7ZYiCz-6YS4eM3JU_9A45Y51b0Z3bS3PPr7CxpVBB82mxZndgMWghvuMj2DfdXZzOMiVw8NmqaJXNJ8jYekqM-Ba4hwgjbLXDMR7Ayl5z4sTofxDBtpKQoq2Y22ukVhWCvVwITdSXgcPYS1DFfAs_m2Tm_jeQzk?purpose=inline)

**tomato_leaf.jpg**

Ảnh đã chọn – chờ phân tích

Ready

**State 3 – Đang phân tích**

**AI đang phân tích hình ảnh**

Đang xử lý dữ liệu và kiểm tra kết quả...

Processing

**State 4 – Có kết quả**

**Kết quả**

Disease detected

**Tomato – Early Blight**

# **94.8%**

Confidence – giá trị minh họa

Tiếp tục xem triệu chứng, thông tin bệnh và hướng dẫn chăm sóc.

Minh họa các trạng thái UI, không phải kết quả inference của model thật.

Frontend cần có ít nhất bốn trạng thái: idle, selected, uploading/processing và completed; ngoài ra phải có error state.

Đối với phiên bản đầu, nếu inference xử lý đủ nhanh có thể sử dụng API đồng bộ. Nếu cần xử lý ảnh lâu, Grad-CAM nặng hoặc dùng hàng đợi, nên chuyển sang:

1. `POST /diagnoses/predict` trả `202 Accepted` và `job_id`.
2. Frontend gọi `GET /diagnoses/jobs/{job_id}`.
3. Backend trả `queued`, `processing`, `completed` hoặc `failed`.
4. Frontend cập nhật UI cho đến khi có kết quả.

Không nên giả lập phần trăm tiến độ AI nếu Backend không thực sự cung cấp tiến độ.

## **4.6. Trang kết quả AI**

[Deep Learning-Based Cucumber Leaf Disease Detection | Devpost](https://images.openai.com/static-rsc-4/RTQy9ejlsuLFP09rH_fVM5LmJ5P03fO23cWq-pB_yAkZz7xSLt9xsJhw43rcXA2_XezLukf0u_uuJU5uWBP0myzfCWLLwWR5AvLGVAAD2hAS1mbI3A5hpLr9jBhQV-GjkII0CuGstaf8dKUn_PX69D5LGwotAWde9nyrNJlAGx8?purpose=inline)

[devpost.com](https://devpost.com/software/deep-learning-based-cucumber-leaf-disease-detection?utm_source=chatgpt.com)

Khi nhận kết quả, Frontend cần hiển thị thành các khu vực:

| Khu vực         | Dữ liệu lấy từ        |
| --------------- | --------------------- |
| Ảnh người dùng  | Image Storage API     |
| Tên cây         | Prediction response   |
| Tên bệnh        | Prediction response   |
| Confidence      | AI prediction         |
| Top 3           | `top_k`               |
| Grad-CAM        | Explanation API       |
| Triệu chứng     | Disease Knowledge API |
| Nguyên nhân     | Disease Knowledge API |
| Hướng dẫn xử lý | Disease Knowledge API |
| Lịch sử         | Diagnosis API         |

Cần có các nút:

- Lưu vào cây đang theo dõi.
- Xem chi tiết bệnh.
- Tải báo cáo.
- Gửi phản hồi kết quả.
- Kiểm tra lại bằng ảnh mới.

Nếu model không đưa ra kết luận chắc chắn thì không được hiển thị khu vực khuyến nghị điều trị theo một bệnh cụ thể. Thay vào đó cần hướng dẫn chụp lại, kiểm tra thêm hoặc tham khảo chuyên gia.

# **5. Tích hợp chức năng quản lý cây trồng**

Đây là phân hệ kết nối trực tiếp giữa thông tin cây của người dùng và lịch sử AI.

## **5.1. Trang My Plants**

[Plants App UI by Monil Soni on Dribbble](https://images.openai.com/static-rsc-4/ApCVPXJSQ2YtVhwd_S1xnVUVIywSodAtzWL4RSM7Qw4RFUMZDbJWaYvky2e6eBhv-zhpj6WTjSmOSvb8at_DRJ_eXjEZ_HMB-gDKiPGafdtjtg8fz-XiuC0cU-J65AnpnYYcpJITwuUv507oWfN-7QC-l2pxXKZ2fhJWxRO9bRw?purpose=inline)

[dribbble.com](https://dribbble.com/shots/27148140-Plants-App-UI?utm_source=chatgpt.com)

Frontend hiển thị danh sách cây mà người dùng đã đăng ký theo dõi.

Mỗi cây có:

- Ảnh đại diện.
- Tên do người dùng đặt.
- Loại cây.
- Ngày bắt đầu theo dõi.
- Khu vực trồng.
- Tổng số lần kiểm tra.
- Lần kiểm tra gần nhất.
- Tình trạng theo dõi gần nhất.

Các API:

| Method | Endpoint                    | Chức năng                 |
| ------ | --------------------------- | ------------------------- |
| GET    | `/my-plants`                | Lấy danh sách cây         |
| POST   | `/my-plants`                | Thêm cây                  |
| GET    | `/my-plants/{id}`           | Chi tiết cây              |
| PUT    | `/my-plants/{id}`           | Cập nhật cây              |
| DELETE | `/my-plants/{id}`           | Xóa cây                   |
| GET    | `/my-plants/{id}/diagnoses` | Lịch sử chẩn đoán của cây |

Ví dụ dữ liệu thêm cây:

```
{
  "name": "Cà chua khu vườn số 1",
  "plant_species": "tomato",
  "variety": "Cherry Tomato",
  "location": "Khu vườn phía sau",
  "planted_at": "2026-10-15",
  "notes": "Trồng trong chậu"
}
```

Sau khi Frontend gọi `POST /my-plants`, Backend:

1. Xác thực user.
2. Kiểm tra `plant_species` có trong danh mục cây được quản lý không.
3. Tạo bản ghi `user_plants`.
4. Trả thông tin cây vừa tạo.
5. Frontend cập nhật danh sách bằng TanStack Query.

Cần phân biệt hai đối tượng:

- `plants`: danh mục loại cây toàn hệ thống, ví dụ Tomato, Potato, Apple.
- `user_plants`: từng cây cụ thể do người dùng theo dõi.

Một người có thể có nhiều cây cà chua. Không được lưu mỗi loại cây thành một đối tượng quản lý duy nhất.

## **5.2. Trang Plant Detail**

Khi người dùng mở chi tiết một cây, Frontend gọi:

```
GET /api/v1/my-plants/{id}
GET /api/v1/my-plants/{id}/diagnoses
GET /api/v1/analytics/plant/{id}
GET /api/v1/care-logs?plant_id={id}
```

Giao diện gồm các tab:

| Tab              | Nội dung                             |
| ---------------- | ------------------------------------ |
| Overview         | Thông tin cây và tình trạng theo dõi |
| Diagnosis        | Các lần nhận diện bệnh               |
| Health Analytics | Biểu đồ tình trạng                   |
| Care Journal     | Nhật ký chăm sóc                     |
| Reminders        | Lịch nhắc nhở                        |

Khi người dùng chọn một cây từ trang này để phân tích, Frontend gửi `user_plant_id` trong request prediction. Backend kiểm tra cây đó có thuộc tài khoản đang đăng nhập trước khi liên kết kết quả chẩn đoán.

# **6. Tích hợp lịch sử chẩn đoán**

[FarmPulse AI - Smart Irrigation and Plant Disease Detection Syste..](https://images.openai.com/static-rsc-4/nVplNAjsqyj3T_L2B8zwRII8wlvksV6eNmAo1Zp7bhc1AEu6fxubGAgK-3e-xdRXw0kbK1b9VSccDub0goeI6CGOCxpKEWX12EFhbygrxaIQjn9nDmEXD2Fcu_DHPPLEZ2Yg0s-chiqPUmsRIn1BeSTjvCwF1mX9VgyUhviify8?purpose=inline)

[electronicwings.com](https://www.electronicwings.com/users/JayanthKS/projects/5957/farmpulse-ai---smart-irrigation-and-plant-disease-detection-system-for-small-farmers?utm_source=chatgpt.com)

Trang Diagnosis History hiển thị tất cả các lần người dùng từng phân tích ảnh.

API:

| Method | Endpoint                      | Chức năng           |
| ------ | ----------------------------- | ------------------- |
| GET    | `/diagnoses`                  | Danh sách chẩn đoán |
| GET    | `/diagnoses/{id}`             | Chi tiết chẩn đoán  |
| DELETE | `/diagnoses/{id}`             | Xóa bản ghi         |
| POST   | `/diagnoses/{id}/feedback`    | Gửi phản hồi        |
| GET    | `/diagnoses/{id}/explanation` | Xem Grad-CAM        |
| GET    | `/diagnoses/{id}/report`      | Xuất báo cáo        |

Frontend cần có bộ lọc:

- Theo thời gian.
- Theo loại cây.
- Theo tên bệnh.
- Theo trạng thái healthy/disease/uncertain.
- Theo cây đang theo dõi.

Sử dụng phân trang từ Backend thay vì tải toàn bộ lịch sử về frontend.

Ví dụ:

```
GET /api/v1/diagnoses?page=1&page_size=20&status=diagnosed
```

Backend trả:

```
{
  "items": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 86,
    "total_pages": 5
  }
}
```

Mỗi bản ghi phải lưu `model_version`. Khi người dùng mở lịch sử cũ, Frontend phải hiển thị đúng phiên bản AI đã phân tích ở thời điểm đó, không lấy phiên bản model hiện tại để gán vào kết quả cũ.

## **6.1. Feedback kết quả AI**

Đây là chức năng rất hữu ích cho việc cải thiện mô hình sau này.

Người dùng có thể phản hồi:

- Kết quả có vẻ đúng.
- Kết quả có vẻ sai.
- Loại cây không chính xác.
- Bệnh không chính xác.
- Ảnh không đủ rõ.
- Có ghi chú bổ sung.

API:

```
POST /api/v1/diagnoses/{id}/feedback
```

Ví dụ:

```
{
  "feedback_type": "incorrect_disease",
  "corrected_plant": "tomato",
  "corrected_disease": "septoria_leaf_spot",
  "comment": "Kết quả dự đoán chưa đúng với quan sát thực tế."
}
```

Phản hồi này không được tự động xem là nhãn chuyên môn đã xác thực. Nếu muốn đưa ảnh vào vòng huấn luyện tiếp theo, phải có quy trình kiểm duyệt và xác nhận nhãn.

# **7. Tích hợp Plant Health Analytics**

Đây là một trong những phần cần thiết kế cẩn thận nhất để tránh Frontend tự tính ra những chỉ số không có cơ sở.

[Karthik. | Web Developer](https://images.openai.com/static-rsc-4/KEW1JFfs_Mop28yUAc5nsuocVtSxHJYL8_Cz-tK4USPgf7zInN4COdIdiJGCssxo6t8VMKXXKX59HqWneGB2y6ImIlHYJpfmwdJI1rOQeCJKuJv4q-dVebFqJE6-ECzUsOtyFZwuT_1IATLZpUlin0yC7E5njZDoj-ekG-CjCLc?purpose=inline)

[karthikn-code.github.io](https://karthikn-code.github.io/?utm_source=chatgpt.com)

Frontend chỉ nhận kết quả phân tích đã được Backend tính toán.

API:

```
GET /api/v1/analytics/dashboard
GET /api/v1/analytics/plant/{plant_id}
GET /api/v1/analytics/plant/{plant_id}/history
GET /api/v1/analytics/disease-distribution
GET /api/v1/analytics/scan-trend
```

Backend tổng hợp từ:

- Các bản ghi chẩn đoán.
- Kết quả AI.
- Thời gian chụp ảnh.
- Cây được gắn với lần kiểm tra.
- Mức độ tổn thương nếu có module đo lường.
- Nhật ký chăm sóc của người dùng.

Frontend hiển thị:

**A. Plant Health Overview**

- Kết quả kiểm tra gần nhất.
- Số lần xuất hiện dấu hiệu bệnh.
- Các loại bệnh đã từng được nhận diện.
- Thời gian kiểm tra gần nhất.

**B. Disease History**

Biểu đồ số lần phát hiện các bệnh theo ngày, tuần hoặc tháng.

**C. Symptom Trend**

Nếu đã có module phân đoạn vùng lá và đo tỷ lệ tổn thương, Backend có thể trả về tỷ lệ diện tích bất thường của từng ảnh để Frontend vẽ biểu đồ.

**D. Care Activity**

Hiển thị các hoạt động chăm sóc đã được người dùng ghi nhận.

Cần ghi nhớ:

- Confidence 95% không có nghĩa cây bệnh nặng 95%.
- Số lần phát hiện bệnh không tương đương tỷ lệ cây bị bệnh trong toàn bộ khu vườn.
- Hai ảnh khác nhau không tự động chứng minh bệnh đang tiến triển.
- Nếu không có dữ liệu segmentation, không được tự tạo phần trăm diện tích lá bị bệnh.

## **7.1. Ví dụ response Analytics**

```
{
  "plant_id": 125,
  "period": {
    "from": "2026-11-01",
    "to": "2026-11-24"
  },
  "summary": {
    "total_scans": 6,
    "healthy_scans": 2,
    "disease_detected_scans": 3,
    "uncertain_scans": 1
  },
  "timeline": [
    {
      "date": "2026-11-05",
      "diagnosis_status": "healthy"
    },
    {
      "date": "2026-11-10",
      "diagnosis_status": "diagnosed",
      "disease_id": "tomato_early_blight"
    }
  ],
  "latest_assessment": {
    "status": "needs_monitoring",
    "based_on": "latest_image_diagnosis"
  }
}
```

Đây là ví dụ response cần thiết kế. Trạng thái `needs_monitoring` được Backend tạo theo một quy tắc nghiệp vụ minh bạch, không phải nhãn trực tiếp từ mô hình 38 lớp.

# **8. Tích hợp Disease Library**

[AI Plant Disease Detection System — Final Year Project with Source Code | CodeAj Marketplace](https://images.openai.com/static-rsc-4/Db2KJeZeM88WhJZpAmtoMtbndWaBwHHB0y4oXUm-IzMeO29yWL1XvAQjWbzG5ji1NwMr0S6tJiGLZMBin_hwFl6cohGaOMvZ2Km3VJjqgDtkqrsXzu83Rb8qfjLi3opMK0F7U6dvzaQzw_52-rwmF7-qNj31YU2cQO1JrbG_Z4M?purpose=inline)

[projects.codeaj.com](https://projects.codeaj.com/projects/ai-plant-disease-detection-cnn-flask-final-year-project/?utm_source=chatgpt.com)

Trang thư viện bệnh phải sử dụng chung dữ liệu với phần kết quả AI.

Backend quản lý nội dung bệnh trong bảng `diseases`, `disease_symptoms`, `disease_treatments`.

API:

| API                           | Công dụng                     |
| ----------------------------- | ----------------------------- |
| `GET /diseases`               | Danh sách bệnh                |
| `GET /diseases/{id}`          | Chi tiết bệnh                 |
| `GET /diseases?plant=tomato`  | Lọc theo cây                  |
| `GET /diseases?search=blight` | Tìm kiếm                      |
| `GET /plants/{id}/diseases`   | Bệnh có thể ảnh hưởng đến cây |

Khi người dùng nhận kết quả Tomato Early Blight, Frontend sử dụng `disease_id` trong response để lấy đúng nội dung kiến thức từ Backend.

Không nên viết riêng mô tả bệnh vào một component React, bởi nội dung cần được quản lý tập trung và có thể cập nhật mà không phải sửa mã nguồn frontend.

# **9. Tích hợp Care Journal và Reminders**

Các chức năng này không cần AI trực tiếp, nhưng liên kết với quá trình theo dõi cây.

| Chức năng Frontend | API Backend                     |
| ------------------ | ------------------------------- |
| Xem nhật ký        | `GET /care-logs`                |
| Thêm hoạt động     | `POST /care-logs`               |
| Sửa hoạt động      | `PUT /care-logs/{id}`           |
| Xóa hoạt động      | `DELETE /care-logs/{id}`        |
| Tạo lịch nhắc      | `POST /reminders`               |
| Xem lịch nhắc      | `GET /reminders`                |
| Cập nhật lịch      | `PUT /reminders/{id}`           |
| Hoàn thành lịch    | `POST /reminders/{id}/complete` |

Các loại hoạt động ban đầu:

- Watering – Tưới nước.
- Fertilizing – Bón phân.
- Pruning – Cắt tỉa.
- Disease Treatment – Xử lý bệnh.
- Inspection – Kiểm tra cây.
- Other – Hoạt động khác.

Nhắc nhở nên được Backend quản lý và lưu trong Database. Frontend chịu trách nhiệm hiển thị lịch và trạng thái. Khi người dùng đóng trình duyệt, hệ thống vẫn phải giữ được lịch nhắc.

# **10. Admin Frontend tích hợp Admin Backend**

[NSquare](https://images.openai.com/static-rsc-4/djrnPZfuuIiaR_QPaIQ3PPR7bVhtzC_M7O7TXYOZEm7JGPwFnp-ydn3JccuxLMdoRZNn0DXPpKkAUQmCBUlUhCFIZBAn54QuajcssAGJM03sOd0zqApfVWMNDGKVHYXllz-_yYfZOLnrUlU_quG9DnGbohmLE4bdqYO8fI4s6xI?purpose=inline)

[nsqur.com](https://www.nsqur.com/Home/MLOpsPlatform?utm_source=chatgpt.com)

Admin là một khu vực riêng của ứng dụng, chỉ những tài khoản có role `ADMIN` mới được sử dụng.

| Trang Admin           | API                        |
| --------------------- | -------------------------- |
| Admin Dashboard       | `GET /admin/dashboard`     |
| User Management       | `/admin/users`             |
| Plant Management      | `/admin/plants`            |
| Disease Management    | `/admin/diseases`          |
| Prediction Management | `/admin/diagnoses`         |
| Feedback Management   | `/admin/feedback`          |
| Model Management      | `/admin/models`            |
| Model Evaluation      | `/admin/model-evaluations` |
| Audit Logs            | `/admin/audit-logs`        |

### **10.1. Admin Dashboard**

Hiển thị:

- Tổng số người dùng.
- Số tài khoản đang hoạt động.
- Tổng số lượt dự đoán.
- Lượt dự đoán theo ngày.
- Các class được nhận diện nhiều nhất.
- Tỷ lệ uncertain.
- Số lượng feedback.
- Trạng thái model đang triển khai.

### **10.2. Model Management**

Đây là phần liên kết trực tiếp với AI Backend đã xây dựng ở giai đoạn trước.

Admin có thể xem:

| Thông tin         | Ví dụ                    |
| ----------------- | ------------------------ |
| Model Name        | EfficientNet-B0          |
| Version           | 1.0.0                    |
| Dataset           | PlantVillage Color       |
| Number of Classes | 38                       |
| Accuracy          | Lấy từ evaluation report |
| Macro-F1          | Lấy từ evaluation report |
| Cross-domain F1   | Lấy từ evaluation report |
| Model Status      | Active / Archived        |

Không được cho Admin chỉnh sửa file trọng số trực tiếp từ trình duyệt.

Nếu muốn bổ sung chức năng kích hoạt model mới, Backend phải xác minh model artifact, metadata, class mapping, preprocessing và evaluation status trước khi cho phép triển khai.

### **10.3. Model Evaluation**

Đây là một trang có giá trị học thuật cao, có thể dùng khi thuyết trình đồ án.

Frontend lấy dữ liệu từ:

```
GET /api/v1/admin/model-evaluations
GET /api/v1/admin/model-evaluations/{id}
GET /api/v1/admin/model-evaluations/{id}/confusion-matrix
```

Hiển thị:

- Accuracy.
- Macro Precision.
- Macro Recall.
- Macro-F1.
- Weighted-F1.
- Confusion Matrix.
- Classification Report.
- PlantDoc Cross-domain Results.
- OOD Metrics.
- Model Comparison.
- Training Curves.

Các biểu đồ phải đọc dữ liệu thực từ báo cáo đánh giá đã lưu. Không nên dùng dữ liệu random để tạo biểu đồ mô hình.

# **11. Thiết kế API Contract thống nhất giữa Frontend và Backend**

Đây là quy định quan trọng nhất về mặt kỹ thuật tích hợp.

Frontend và Backend cần thống nhất trước:

- Endpoint.
- HTTP method.
- Request schema.
- Response schema.
- Validation.
- HTTP status code.
- Error format.
- Authentication.
- Pagination.
- Sorting và filtering.

Tôi đề xuất dùng chuẩn JSON API thống nhất, đồng thời tạo tài liệu OpenAPI từ FastAPI.

## **11.1. Cấu trúc dự án Frontend**

```
frontend/
│
├── public/
│   ├── icons/
│   ├── images/
│   └── manifest.json
│
├── src/
│   ├── app/
│   │   ├── App.tsx
│   │   ├── router.tsx
│   │   └── providers.tsx
│   │
│   ├── components/
│   │   ├── ui/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── feedback/
│   │   └── charts/
│   │
│   ├── features/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── diagnosis/
│   │   ├── plants/
│   │   ├── history/
│   │   ├── analytics/
│   │   ├── diseases/
│   │   ├── care/
│   │   ├── notifications/
│   │   └── admin/
│   │
│   ├── hooks/
│   ├── lib/
│   │   ├── api-client.ts
│   │   ├── query-client.ts
│   │   └── error-handler.ts
│   │
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── diagnosis.service.ts
│   │   ├── plant.service.ts
│   │   ├── analytics.service.ts
│   │   └── disease.service.ts
│   │
│   ├── types/
│   │   ├── api.ts
│   │   ├── diagnosis.ts
│   │   ├── plant.ts
│   │   └── user.ts
│   │
│   ├── utils/
│   ├── styles/
│   └── main.tsx
│
├── .env.example
├── package.json
└── vite.config.ts
```

Mỗi feature tự quản lý component, hook, validation schema và service liên quan. Tránh viết toàn bộ API vào một file `api.ts` hàng nghìn dòng.

## **11.2. Cấu trúc Backend tương ứng**

```
backend/app/
│
├── api/
│   └── v1/
│       ├── auth.py
│       ├── dashboard.py
│       ├── plants.py
│       ├── diagnoses.py
│       ├── diseases.py
│       ├── analytics.py
│       ├── care.py
│       ├── notifications.py
│       └── admin.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── dependencies.py
│   └── permissions.py
│
├── models/
├── schemas/
├── repositories/
│
├── services/
│   ├── auth_service.py
│   ├── plant_service.py
│   ├── diagnosis_service.py
│   ├── disease_service.py
│   ├── analytics_service.py
│   ├── care_service.py
│   └── report_service.py
│
├── ml/
│   ├── model_loader.py
│   ├── predictor.py
│   ├── preprocessing.py
│   ├── ood_detector.py
│   └── gradcam.py
│
├── storage/
│   └── image_storage.py
│
└── main.py
```

# **12. Quy tắc giao tiếp API giữa hai phía**

## **12.1. Base URL và môi trường**

Frontend không được viết cứng URL Backend vào từng component.

Tạo `.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

Các môi trường:

| Môi trường  | Frontend                   | Backend               |
| ----------- | -------------------------- | --------------------- |
| Development | localhost:5173             | localhost:8000        |
| Staging     | staging frontend domain    | staging API domain    |
| Production  | production frontend domain | production API domain |

Toàn bộ endpoint dùng tiền tố:

```
/api/v1/
```

Khi Backend thay đổi version API, chúng ta có thể phát triển `/api/v2/` mà không phá vỡ ngay các client đang sử dụng `/api/v1/`.

## **12.2. Response format thống nhất**

Dữ liệu thành công:

```
{
  "data": {
    "id": 125,
    "name": "Cà chua"
  },
  "meta": {
    "request_id": "req_abc123"
  }
}
```

Dữ liệu phân trang:

```
{
  "data": [],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 86,
    "total_pages": 5
  }
}
```

Lỗi:

```
{
  "error": {
    "code": "IMAGE_TOO_LARGE",
    "message": "Ảnh vượt quá dung lượng cho phép.",
    "details": {
      "maximum_size_mb": 10
    }
  },
  "meta": {
    "request_id": "req_abc123"
  }
}
```

Đây là quy ước đề xuất. FastAPI cần được cấu hình exception handler để mọi endpoint tuân thủ cùng một format.

## **12.3. Bảng HTTP status code**

| Status | Ý nghĩa                             | Frontend xử lý                     |
| ------ | ----------------------------------- | ---------------------------------- |
| 200    | Thành công                          | Hiển thị dữ liệu                   |
| 201    | Tạo mới thành công                  | Cập nhật danh sách                 |
| 202    | Yêu cầu được tiếp nhận, xử lý nền   | Theo dõi job                       |
| 400    | Dữ liệu không hợp lệ                | Hiển thị validation error          |
| 401    | Chưa đăng nhập hoặc session hết hạn | Thử refresh hoặc yêu cầu đăng nhập |
| 403    | Không có quyền                      | Hiển thị trang không được phép     |
| 404    | Không tìm thấy dữ liệu              | Hiển thị not found                 |
| 409    | Xung đột dữ liệu                    | Thông báo và yêu cầu xử lý         |
| 413    | File quá lớn                        | Yêu cầu chọn ảnh khác              |
| 415    | Định dạng không hỗ trợ              | Hiển thị định dạng được phép       |
| 422    | Lỗi validation                      | Hiển thị lỗi trường dữ liệu        |
| 429    | Quá nhiều request                   | Thông báo thử lại sau              |
| 500    | Lỗi hệ thống                        | Hiển thị thông báo chung           |

## **12.4. Một API Client duy nhất**

Mọi feature phải gọi API thông qua lớp dùng chung.

Ví dụ:

```
// src/lib/api-client.ts

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1${endpoint}`,
    {
      ...options,
      credentials: "include",
      headers: {
        Accept: "application/json",
        ...options.headers
      }
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.error?.message ??
      error?.detail ??
      "Đã xảy ra lỗi khi kết nối máy chủ."
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
```

Khi sử dụng API client này, cần xử lý CSRF token nếu authentication dùng cookie, bổ sung refresh session có kiểm soát và tránh nhiều request cùng lúc tự động refresh.

Các component không gọi `fetch()` tùy tiện. Chúng gọi service tương ứng:

```
DiagnosisPage
      |
      v
useDiagnosisMutation
      |
      v
diagnosis.service.ts
      |
      v
api-client.ts
      |
      v
FastAPI
```

Cách này giúp thay đổi Backend URL hoặc response mapping mà không phải sửa hàng chục component.

## **12.5. Định nghĩa TypeScript từ OpenAPI**

Đây là việc rất nên làm ngay từ đầu.

FastAPI tự sinh OpenAPI schema. Có thể sử dụng công cụ sinh TypeScript types từ OpenAPI để Frontend sử dụng đúng kiểu dữ liệu Backend đã công bố.

Ví dụ:

```
export type DiagnosisStatus =
  | "diagnosed"
  | "healthy"
  | "uncertain"
  | "unsupported_crop"
  | "unknown_disease";

export interface PredictionItem {
  class_id: string;
  confidence: number;
}

export interface DiagnosisResult {
  diagnosis_id: number;
  status: DiagnosisStatus;
  plant: {
    id: string;
    name: string;
  } | null;
  disease: {
    id: string;
    name: string;
    name_vi: string;
  } | null;
  prediction: {
    confidence: number | null;
    top_k: PredictionItem[];
  } | null;
  model_version: string;
}
```

Không được để Frontend tự định nghĩa một response khác với Backend. Đây là nguyên nhân thường gặp khiến tích hợp bị lỗi khi phát triển nhiều module song song.

# **13. Responsive Web và Mobile/PWA**

Bạn muốn hệ thống chạy được trên laptop và điện thoại. Có thể sử dụng chung một bộ Frontend React, không cần làm hai website riêng.

[Deep Learning-Based Cucumber Leaf Disease Detection | Devpost](https://images.openai.com/static-rsc-4/JedT30NGtSitzMVec-9ZrGa2rqZxSB2fS1SThSf03UWAexnkXWLFM5IrkgALREyWk_05-WZqIhVmyVI4zoHkZNOASmBUvbMJ8ExJZSKHDbgXSCwW6138YpX2h0qGEvfk8_RD8sAU-Mh5O7sfwUOi_KnKN-wECJjsQUJ2PpD3kEI?purpose=inline)

**Laptop / Desktop**

Sidebar, nhiều cột, biểu đồ, bảng dữ liệu, kéo thả ảnh.

[UI/UX Mobile Design - Plant Disease Detection by Nurevina on Dribbble](https://images.openai.com/static-rsc-4/_lFTP0y5bd4vxapHKYurQcm6Ch5cg71RK-3kWAFShkKmvmzIklYc_SOyAzzZpX2LbuwmMQyy2lvXnsQa-Rj0WjjD7EG0tpNaUzhgwLfsU0rEwKeCIrDHIPCMreQuHIDlJXugCA3a74XKKBArC7626JMRw20v-l8zTgXVmZLBNuM?purpose=inline)

**Mobile**

Camera, upload ảnh, menu thu gọn, thao tác bằng một tay.

## **13.1. Những yêu cầu UI Responsive**

| Thành phần | Laptop                 | Mobile                        |
| ---------- | ---------------------- | ----------------------------- |
| Navigation | Sidebar                | Bottom navigation hoặc drawer |
| Dashboard  | Grid nhiều cột         | Một cột                       |
| Chart      | Biểu đồ lớn            | Biểu đồ co giãn               |
| Table      | Bảng đầy đủ            | Card hoặc cuộn ngang          |
| Upload     | Drag & Drop            | Camera và thư viện ảnh        |
| Form       | Nhiều trường cùng hàng | Một trường mỗi hàng           |
| Dialog     | Modal                  | Full-screen sheet             |
| Menu       | Sidebar                | Drawer                        |

Frontend nên được kiểm thử ít nhất ở các viewport:

- 375 × 812.
- 390 × 844.
- 768 × 1024.
- 1024 × 768.
- 1366 × 768.
- 1920 × 1080.

## **13.2. Chụp ảnh bằng camera điện thoại**

Có thể dùng input:

```
<input
  type="file"
  accept="image/*"
  capture="environment"
/>
```

Một số trình duyệt sẽ mở camera sau, một số cho phép chọn camera hoặc thư viện ảnh. Không nên giả định mọi thiết bị đều mở camera theo cùng cách.

Cần có phương án dự phòng cho người dùng chọn ảnh từ thư viện.

## **13.3. PWA hoạt động như thế nào?**

PWA cho phép người dùng:

- Cài website lên màn hình chính.
- Mở giao diện gần giống ứng dụng.
- Sử dụng một số chức năng giao diện trong điều kiện mạng yếu.
- Nhận thông báo đẩy nếu đã triển khai service và được hệ điều hành/trình duyệt hỗ trợ.

Tuy nhiên, PWA không đồng nghĩa với một ứng dụng native Android/iOS. Các chức năng AI vẫn gọi Backend qua Internet.

Đối với Đồ án chuyên ngành 2, PWA là phương án phù hợp. Nếu sau này cần ứng dụng native từ cùng codebase web, có thể đánh giá thêm Capacitor hoặc React Native.

## **13.4. Khi mất mạng**

Phải phân biệt:

- Các trang đã cache và nội dung công khai có thể mở offline nếu được thiết kế.
- Lịch sử đã cache có thể xem ở chế độ hạn chế.
- Người dùng không thể gọi AI Backend khi không có mạng, trừ khi xây dựng thêm mô hình chạy trực tiếp trên thiết bị.

Không được hiển thị "AI đã phân tích thành công" trong lúc điện thoại chưa kết nối được Backend.

# **14. Kiểm thử tích hợp Frontend – Backend**

Chúng ta không chỉ kiểm thử riêng từng phía. Phải có kiểm thử xuyên suốt toàn bộ hệ thống.

| Mã     | Kịch bản                    | Kết quả mong muốn                        |
| ------ | --------------------------- | ---------------------------------------- |
| INT-01 | Đăng nhập đúng              | Chuyển đến Dashboard                     |
| INT-02 | Đăng nhập sai               | Hiện lỗi                                 |
| INT-03 | Refresh trang sau đăng nhập | Giữ session hợp lệ                       |
| INT-04 | USER mở API ADMIN           | Backend trả 403                          |
| INT-05 | Tải ảnh hợp lệ              | Backend nhận ảnh                         |
| INT-06 | Tải file PDF                | Backend từ chối                          |
| INT-07 | Tải ảnh quá lớn             | Backend trả 413                          |
| INT-08 | Phân tích ảnh lá hợp lệ     | Nhận kết quả AI thật                     |
| INT-09 | Ảnh cây chưa hỗ trợ         | Trả unsupported/unknown phù hợp          |
| INT-10 | Confidence thấp             | Trả uncertain                            |
| INT-11 | Model chưa load             | Không giả kết quả thành công             |
| INT-12 | Database lỗi                | Không thông báo lưu thành công           |
| INT-13 | Lưu chẩn đoán vào cây       | Liên kết đúng user_plant                 |
| INT-14 | Xem lịch sử                 | Có dữ liệu đã lưu                        |
| INT-15 | Xóa dữ liệu                 | User không thể xóa dữ liệu của user khác |
| INT-16 | Dashboard                   | Thống kê đúng dữ liệu Database           |
| INT-17 | Mobile upload               | Gửi ảnh thành công                       |
| INT-18 | Mạng bị ngắt                | Hiển thị lỗi và cho phép thử lại         |

### **14.1. Những công cụ nên sử dụng**

| Công cụ          | Kiểm thử                       |
| ---------------- | ------------------------------ |
| Swagger UI       | Backend API                    |
| Postman          | API request/response           |
| Pytest           | Backend                        |
| Vitest           | Frontend unit/component        |
| Playwright       | End-to-end                     |
| Browser DevTools | Responsive, network, console   |
| Lighthouse       | Hiệu năng và khả năng truy cập |

### **14.2. Luồng End-to-End quan trọng nhất**

\#chatgpt-mermaid-\_r_141\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_141\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_141\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_141\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_141\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_141\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_141\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_141\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_141\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_141\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_141\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_141\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_141\_ p{margin:0;}#chatgpt-mermaid-\_r_141\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_141\_ .label text,#chatgpt-mermaid-\_r_141\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ .node rect,#chatgpt-mermaid-\_r_141\_ .node circle,#chatgpt-mermaid-\_r_141\_ .node ellipse,#chatgpt-mermaid-\_r_141\_ .node polygon,#chatgpt-mermaid-\_r_141\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ .rough-node .label text,#chatgpt-mermaid-\_r_141\_ .node .label text,#chatgpt-mermaid-\_r_141\_ .image-shape .label,#chatgpt-mermaid-\_r_141\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_141\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ .rough-node .label,#chatgpt-mermaid-\_r_141\_ .node .label,#chatgpt-mermaid-\_r_141\_ .image-shape .label,#chatgpt-mermaid-\_r_141\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_141\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_141\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_141\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_141\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_141\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_141\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_141\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_141\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_141\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_141\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_141\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_141\_ .icon-shape,#chatgpt-mermaid-\_r_141\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_141\_ .icon-shape p,#chatgpt-mermaid-\_r_141\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_141\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_141\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_141\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_141\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_141\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_141\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_141\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_141\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_141\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_141\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_141\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_141\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_141\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_141\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_141\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_141\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_141\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_141\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ .node rect,#chatgpt-mermaid-\_r_141\_ .node circle,#chatgpt-mermaid-\_r_141\_ .node ellipse,#chatgpt-mermaid-\_r_141\_ .node polygon,#chatgpt-mermaid-\_r_141\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_141\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_141\_ .mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_141\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_141\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_141\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Open websiteRegister / LoginCreate a plantOpen AI DetectionUpload leaf imageBackend validatesReal AI inferenceSave result in DBDisplay diagnosisOpen Plant DetailView diagnosis historyView health analytics

Chỉ khi luồng này chạy thành công trên cả laptop lẫn điện thoại mới được xem là đã hoàn thành tích hợp chức năng chính.

# **15. Quy trình phát triển Frontend – Backend**

Dù đã thống nhất xây dựng AI trước, Backend và Frontend vẫn phải có một hợp đồng giao tiếp ngay từ đầu.

Không nên đợi Backend viết xong toàn bộ rồi Frontend mới bắt đầu. Có thể thiết kế API contract sớm, nhưng việc triển khai giao diện chính thức sẽ dựa trên các API và model đã được nghiệm thu.

## **Integration Roadmap**

1. **Phase 1 – Chốt Backend Contract**
   - Đặc tả REST API.
   - Định nghĩa request/response.
   - Định nghĩa status và error.
   - Định nghĩa authentication.
   - Xác định database schema.

   Đầu ra: `API_CONTRACT.md`, OpenAPI specification.
2. **Phase 2 – Backend AI hoàn chỉnh**
   - Tích hợp model đã đánh giá.
   - Xây dựng inference API.
   - Kiểm tra ảnh.
   - OOD và confidence.
   - Lưu lịch sử.

   Đầu ra: API dự đoán chạy thật qua Swagger.
3. **Phase 3 – Backend nghiệp vụ**
   - Authentication.
   - Plant Management.
   - Diagnosis History.
   - Disease Library.
   - Analytics.
   - Admin APIs.

   Đầu ra: Backend hoàn chỉnh và có test.
4. **Phase 4 – Frontend Foundation**
   - React project.
   - Routing.
   - Design system.
   - API Client.
   - Authentication.
   - Layout responsive.

   Đầu ra: Frontend kết nối được API thật.
5. **Phase 5 – Frontend Features**
   - Dashboard.
   - AI Detection.
   - Result page.
   - Plant Management.
   - History.
   - Analytics.
   - Disease Library.
   - Admin.

   Đầu ra: Toàn bộ chức năng được tích hợp.
6. **Phase 6 – Integration Testing**
   - Kiểm tra request/response.
   - Kiểm thử quyền truy cập.
   - Kiểm thử AI.
   - Kiểm thử upload.
   - Kiểm thử dữ liệu thống kê.
   - Kiểm thử đa thiết bị.

   Đầu ra: Bản nghiệm thu tích hợp.
7. **Phase 7 – Deployment**
   - Dockerize.
   - Deploy PostgreSQL.
   - Deploy Backend.
   - Deploy Frontend.
   - Cấu hình HTTPS.
   - PWA.
   - Kiểm thử production.

   Đầu ra: Hệ thống hoạt động trên Internet.

# **16. Quy định triển khai và cấu hình giữa hai phía**

Khi chạy trên máy cá nhân, Docker hoặc Internet, Frontend và Backend phải biết địa chỉ của nhau thông qua biến môi trường.

### **Frontend&#x20;**`.env`

```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Smart Plant Care AI
```

### **Backend&#x20;**`.env`

```
APP_ENV=development
APP_PORT=8000

DATABASE_URL=postgresql://user:password@localhost:5432/plantcare

CORS_ORIGINS=http://localhost:5173

MODEL_PATH=artifacts/models/efficientnet_best.pth
MODEL_VERSION=1.0.0

MAX_UPLOAD_SIZE_MB=10
IMAGE_STORAGE_PATH=storage/uploads

SECRET_KEY=change_this_secret
```

Đây chỉ là cấu hình mẫu. Không commit `.env` thật lên GitHub.

### **16.1. Lưu trữ hình ảnh**

Ảnh người dùng không nên lưu trực tiếp trong PostgreSQL.

Quy trình:

```
Frontend
   |
   | Upload image
   v
FastAPI
   |
   v
Image Validation
   |
   v
Private Storage
   |
   v
Save storage_key in PostgreSQL
```

Trong Database chỉ cần lưu:

```
image_id
user_id
diagnosis_id
storage_key
original_filename
mime_type
file_size
created_at
```

Khi Frontend muốn xem ảnh, Backend kiểm tra quyền sở hữu rồi mới trả ảnh hoặc URL truy cập có thời hạn.

Khi triển khai production, có thể chuyển từ local storage sang S3-compatible object storage mà không cần thay đổi logic nghiệp vụ của Frontend.

### **16.2. CORS và kết nối**

Backend phải giới hạn CORS theo domain Frontend được phép truy cập.

Ví dụ môi trường development:

```
http://localhost:5173
```

Production chỉ cho phép domain chính thức.

Không sử dụng `allow_origins=["*"]` cùng credential-based authentication.

### **16.3. Vấn đề hiệu năng**

Cần chú ý những trường hợp:

- Ảnh dung lượng lớn.
- Nhiều người dùng upload đồng thời.
- Model chiếm nhiều RAM/GPU.
- Grad-CAM mất thời gian xử lý.
- Dashboard có nhiều dữ liệu.
- Người dùng xem lịch sử với số lượng lớn.

Các giải pháp:

- Load model một lần khi Backend khởi động.
- Không load lại trọng số mỗi request.
- Giới hạn kích thước ảnh.
- Phân trang API.
- Cache dữ liệu danh mục ít thay đổi.
- Dùng hàng đợi xử lý nền khi inference hoặc tạo báo cáo quá lâu.
- Theo dõi thời gian response và lỗi inference.

Không nên tạo quá nhiều process Backend cùng load một model lớn trên máy có RAM hạn chế.

# **17. Tiêu chí nghiệm thu Frontend – Backend**

Tôi đề xuất chỉ xem sản phẩm hoàn thành khi đạt các tiêu chí dưới đây.

## **Frontend–Backend Integration Checklist**

**Authentication**

- Đăng ký và đăng nhập qua API thật.
- Session được duy trì sau khi refresh trang.
- USER và ADMIN được phân quyền.
- Backend bảo vệ các API riêng tư.\

  **AI Integration**
- Upload ảnh thực tế.
- Backend gọi đúng model đã nghiệm thu.
- Frontend nhận kết quả JSON.
- Hiển thị Top 3 và confidence.
- Xử lý uncertain và unsupported.
- Hiển thị Grad-CAM.
- Không dùng kết quả AI giả.\

  **Plant Management**
- Thêm, sửa, xóa cây.
- Liên kết kết quả AI với đúng cây.
- Xem lịch sử từng cây.\

  **Analytics**
- Dashboard lấy dữ liệu thật.
- Biểu đồ lấy dữ liệu từ Backend.
- Không tạo số liệu ngẫu nhiên.
- Không nhầm confidence với mức độ bệnh.\

  **Administration**
- Quản lý tài khoản.
- Quản lý dữ liệu bệnh.
- Quản lý phiên bản model.
- Xem kết quả Model Evaluation.\

  **Multi-platform**
- Giao diện laptop.
- Giao diện tablet.
- Giao diện điện thoại.
- Camera upload trên điện thoại.
- PWA có thể cài đặt.
- Các chức năng chính hoạt động trên trình duyệt di động.

# **18. MASTER PROMPT – FRONTEND VÀ BACKEND INTEGRATION**

Đây là prompt dành cho AI coding agent sau khi đã có AI Model và Backend API được nghiệm thu. Bạn có thể đưa cho Cursor, Codex hoặc Claude Code.

**FRONTEND–BACKEND MASTER SPECIFICATION**

Copy ready

Phần yêu cầu xây dựng ứng dụng React và tích hợp với FastAPI Backend đã có.

&#x20;Copy Frontend–Backend Master Prompt

# **19. Quyết định kiến trúc cuối cùng**

Tôi đề xuất khóa kiến trúc theo hướng sau:

# **Smart Plant Care AI**

Một hệ thống – một Backend – nhiều thiết bị sử dụng

**Web Frontend**

React + TypeScript

**Mobile PWA**

Responsive React

**Backend**

FastAPI REST API

**AI Engine**

PyTorch Inference

**Nguyên tắc tích hợp**

- Frontend chỉ hiển thị dữ liệu Backend trả về.
- Backend quản lý toàn bộ nghiệp vụ.
- AI Service chỉ trả dự đoán và thông tin kỹ thuật.
- Database lưu dữ liệu có tính lâu dài.
- API contract là cầu nối thống nhất.
- Một tài khoản có thể sử dụng trên nhiều thiết bị.

**Thứ tự tôi khuyên bạn thực hiện từ thời điểm này:**

1. Hoàn thành Dataset Audit, Training, Evaluation và khóa model.
2. Xây dựng AI Inference Backend và kiểm thử bằng Swagger.
3. Hoàn thiện Backend nghiệp vụ, Database và API Contract.
4. Dùng chính OpenAPI của Backend để xây dựng React Frontend.
5. Kiểm thử toàn bộ luồng trên laptop và điện thoại.
6. Cuối cùng mới Docker hóa và triển khai Web/PWA lên môi trường production.

Có một nguyên tắc cần giữ xuyên suốt dự án: **Frontend chỉ được xem là tích hợp hoàn chỉnh khi mọi chức năng quan trọng đều gọi được Backend thật, Backend xử lý được nghiệp vụ thật và dữ liệu được lưu đúng vào Database.** Giao diện đẹp nhưng nút bấm không có API, kết quả AI giả hoặc biểu đồ dùng số liệu tĩnh đều không được tính là hoàn thành.

Không. Database khi phát triển có thể chạy trên máy tính của bạn, nhưng khi deploy website thì database sẽ được đưa lên server hoặc cloud. **Tất cả người dùng sử dụng chung một hệ thống Database, nhưng dữ liệu riêng tư của mỗi người được phân quyền để người khác không thể nhìn thấy.**

Đây chính là cách hoạt động của các ứng dụng có nhiều tài khoản như Facebook, Instagram, Google Drive.

## **1. Phân biệt Database Local và Database khi Deploy**

### **Khi đang phát triển đồ án trên máy tính**

Ví dụ bạn chạy:

- Frontend: `localhost:5173`
- Backend: `localhost:8000`
- PostgreSQL: `localhost:5432`

Development – Local

**Máy tính của bạn**

Frontend + Backend + PostgreSQL

**PostgreSQL Local**

Lưu tài khoản, cây trồng, ảnh tham chiếu, lịch sử...

Dữ liệu được lưu trên máy tính của bạn. Nếu một người khác mở website từ máy tính của họ thì họ không tự động nhìn thấy database này.

### **Khi deploy website lên Internet**

Ta chuyển Backend và Database lên máy chủ có kết nối Internet.

Production – Cloud

**Người dùng A**

Laptop

**Người dùng B**

Điện thoại

**Người dùng C**

Laptop

**Người dùng D**

Điện thoại

**Internet / HTTPS**

**Frontend – React**

Một website dùng chung cho tất cả thiết bị

**Backend – FastAPI**

Xác thực, phân quyền, xử lý nghiệp vụ và AI

**PostgreSQL – Cloud Database**

Database trung tâm dùng chung

**Image Storage – Cloud**

Lưu ảnh người dùng và ảnh kết quả phân tích

Điểm quan trọng: Người dùng không kết nối trực tiếp đến PostgreSQL. Họ truy cập Frontend, Frontend gọi Backend, Backend mới được phép truy vấn Database.

## **2. Mỗi người dùng chỉ nhìn thấy dữ liệu của mình như thế nào?**

Đây là cơ chế phân quyền dữ liệu (Data Isolation).

Ví dụ có ba người đăng ký tài khoản:

| User ID | Tên tài khoản |
| ------- | ------------- |
| 001     | Nguyễn Văn A  |
| 002     | Trần Văn B    |
| 003     | Lê Văn C      |

Ba người này cùng sử dụng một PostgreSQL Database.

Nhưng dữ liệu cây trồng được lưu như sau:

**Bảng&#x20;**`user_plants`

| Plant ID | User ID | Tên cây          |
| -------- | ------- | ---------------- |
| 101      | 001     | Cà chua vườn nhà |
| 102      | 001     | Cây xoài         |
| 103      | 002     | Khoai tây        |
| 104      | 002     | Cà chua          |
| 105      | 003     | Cây táo          |

**Bảng&#x20;**`diagnoses`

| Diagnosis ID | User ID | Plant ID | Kết quả      |
| ------------ | ------- | -------- | ------------ |
| 501          | 001     | 101      | Early Blight |
| 502          | 001     | 102      | Healthy      |
| 503          | 002     | 103      | Late Blight  |
| 504          | 003     | 105      | Apple Scab   |

Khi đăng nhập:

- Nguyễn Văn A chỉ thấy cây 101, 102 và lịch sử 501, 502.
- Trần Văn B chỉ thấy cây 103, 104 và lịch sử của mình.
- Lê Văn C chỉ thấy cây 105 và lịch sử 504.

**Minh họa quyền truy cập dữ liệu**

**Database dùng chung**

Tài khoản A

Chỉ dữ liệu A

Tài khoản B

Chỉ dữ liệu B

Tài khoản C

Chỉ dữ liệu C

**Dữ liệu chung**

Danh mục cây, thư viện bệnh, thông tin mô hình AI và hướng dẫn chăm sóc được tất cả người dùng truy cập theo quyền.

### **Backend thực hiện việc này ra sao?**

Ví dụ khi người dùng đăng nhập, Backend xác định họ có `user_id = 001`.

Khi gọi API:

```
GET /api/v1/my-plants
```

Backend thực hiện truy vấn tương đương:

```
SELECT *
FROM user_plants
WHERE user_id = 001;
```

Chỉ những cây thuộc tài khoản A mới được trả về.

Khi tài khoản B đăng nhập, Backend tự xác định `user_id = 002` và truy vấn dữ liệu tương ứng.

**Cực kỳ quan trọng:** Backend phải lấy `user_id` từ session hoặc token đã xác thực, không tin `user_id` do Frontend gửi lên. Nếu không, người dùng có thể tự thay ID để cố truy cập dữ liệu của người khác.

Tôi cũng khuyến nghị bổ sung PostgreSQL Row-Level Security (RLS) như một lớp bảo vệ bổ sung, bên cạnh kiểm tra quyền trong Backend.

## **3. Vậy ảnh cây mà người dùng upload thì sao?**

Ảnh cũng phải được phân quyền riêng, không chỉ dữ liệu PostgreSQL.

Tôi đề xuất sử dụng Object Storage để lưu hình ảnh.

Ví dụ cấu trúc lưu trữ:

```
plant-care-storage/
│
├── users/
│   ├── user_001/
│   │   ├── plants/
│   │   │   ├── plant_101/
│   │   │   └── plant_102/
│   │   │
│   │   └── diagnoses/
│   │       ├── scan_501/
│   │       └── scan_502/
│   │
│   ├── user_002/
│   │   ├── plants/
│   │   └── diagnoses/
│   │
│   └── user_003/
│       ├── plants/
│       └── diagnoses/
│
└── public/
    ├── plant_images/
    └── disease_images/
```

Cấu trúc logic minh họa; các thư mục này có thể được tổ chức bằng storage key thay vì thư mục vật lý thực.

Ví dụ:

- User A upload ảnh lá cà chua.
- Backend lưu ảnh vào vùng lưu trữ riêng của A.
- PostgreSQL lưu đường dẫn ảnh, user ID và diagnosis ID.
- User B không có quyền lấy ảnh đó.
- Khi A xem lịch sử, Backend kiểm tra quyền rồi mới cho xem ảnh.

Ảnh riêng tư nên được lưu trong private bucket. Khi xem ảnh, Backend có thể trả URL ký số có thời hạn (presigned URL), thay vì để đường dẫn công khai.

### **Những loại dữ liệu nào dùng chung, loại nào riêng?**

| Dữ liệu                | Phạm vi truy cập            |
| ---------------------- | --------------------------- |
| Tài khoản              | Riêng từng người            |
| Ảnh upload             | Riêng từng người            |
| Cây người dùng quản lý | Riêng từng người            |
| Lịch sử AI             | Riêng từng người            |
| Nhật ký chăm sóc       | Riêng từng người            |
| Lịch nhắc nhở          | Riêng từng người            |
| Thông tin bệnh         | Dùng chung                  |
| Danh mục loại cây      | Dùng chung                  |
| Model AI               | Dùng chung                  |
| Thống kê toàn hệ thống | Admin                       |
| Feedback               | Người gửi và Admin có quyền |
| Báo cáo cá nhân        | Riêng từng người            |

Admin có thể có quyền xem dữ liệu phục vụ quản trị và xử lý phản hồi, nhưng phải có phân quyền và ghi nhận hoạt động truy cập.

## **4. Vậy hệ thống Database thực tế nên triển khai thế nào?**

Tôi đề xuất sử dụng ba thành phần riêng biệt:

**PostgreSQL**

Lưu tài khoản, cây trồng, bệnh, lịch sử, phân quyền và thông tin mô hình.

Có thể dùng dịch vụ PostgreSQL quản lý trên cloud hoặc tự quản lý trên VPS.

**Object Storage**

Lưu ảnh upload, ảnh Grad-CAM, ảnh đại diện và báo cáo.

Có thể dùng S3-compatible storage như Cloudflare R2 hoặc AWS S3.

**AI Model Storage**

Lưu EfficientNet, class mapping, model metadata và evaluation reports.

Backend tải model đã được phê duyệt để inference.

Một số nền tảng bạn có thể tham khảo:

| Nền tảng      | Vai trò                     |
| ------------- | --------------------------- |
| Supabase      | PostgreSQL, Auth và Storage |
| Neon          | Managed PostgreSQL          |
| AWS S3        | Lưu ảnh và file             |
| Cloudflare R2 | Lưu trữ hình ảnh            |
| Render        | Deploy Backend              |
| Vercel        | Deploy React Frontend       |

Không nhất thiết phải dùng tất cả. Với đồ án này, tôi ưu tiên PostgreSQL managed, storage riêng và FastAPI chạy trên một máy chủ có đủ tài nguyên cho AI.

## **5. Khi deploy, dữ liệu có bị mất khi tắt máy tính của bạn không?**

Không, nếu deploy đúng cách.

Ví dụ:

Bạn deploy ứng dụng lên cloud:

- Frontend chạy trên Vercel.
- Backend FastAPI chạy trên VPS.
- PostgreSQL chạy trên Supabase.
- Ảnh được lưu trên Cloudflare R2.
- AI model được lưu và nạp trên server chạy Backend.

Sau đó bạn tắt laptop của mình.

Hệ thống vẫn hoạt động

Người dùng vẫn có thể:

- Truy cập website.
- Đăng ký tài khoản.
- Đăng nhập.
- Upload ảnh.
- Chạy AI.
- Lưu lịch sử.
- Xem lại cây đã quản lý.

Vì toàn bộ hệ thống đã chạy trên máy chủ Internet, không còn phụ thuộc vào máy cá nhân của bạn.

Tuy nhiên cần cấu hình persistent storage, backup Database và backup ảnh. Không lưu PostgreSQL trong filesystem tạm thời của container vì dữ liệu có thể mất khi container bị thay thế.

## **6. Cấu trúc Database cuối cùng tôi đề xuất**

Để bảo đảm hệ thống nhiều người dùng, cần bổ sung rõ các cột quản lý chủ sở hữu dữ liệu.

| Bảng              | Trường quan trọng                         |
| ----------------- | ----------------------------------------- |
| users             | id, email, password_hash, role            |
| plants            | id, species, common_name                  |
| diseases          | id, name, description                     |
| user_plants       | id, user_id, plant_id, name               |
| diagnoses         | id, user_id, user_plant_id, model_version |
| diagnosis_images  | id, diagnosis_id, user_id, storage_key    |
| scan_predictions  | id, diagnosis_id, class_id, confidence    |
| care_logs         | id, user_id, user_plant_id                |
| reminders         | id, user_id, user_plant_id                |
| notifications     | id, user_id, content                      |
| model_versions    | id, version, metrics                      |
| model_evaluations | id, model_version_id, dataset, metrics    |
| audit_logs        | id, actor_user_id, action, created_at     |

Một nguyên tắc cần giữ: các bảng dữ liệu cá nhân phải gắn với `user_id` hoặc liên kết đến một bản ghi đã được kiểm tra quyền sở hữu.

## **7. Tôi đề xuất thêm một tính năng: Chia sẻ cây trồng**

Ngoài việc giữ dữ liệu riêng tư, bạn có thể phát triển thêm chức năng chia sẻ có chủ đích.

Ví dụ:

Người dùng A có cây cà chua đang bị bệnh. A muốn chia sẻ hồ sơ cây cho người dùng B cùng theo dõi.

Khi đó mới tạo chức năng:

- Chia sẻ cây cho tài khoản khác.
- Cấp quyền chỉ xem hoặc chỉnh sửa.
- Thu hồi quyền chia sẻ.
- Ghi lại lịch sử thao tác.

Có thể bổ sung bảng:

```
plant_shares
- id
- user_plant_id
- owner_user_id
- shared_with_user_id
- permission
- created_at
```

Đây là tính năng mở rộng, không bắt buộc trong phiên bản đầu.

## **8. Chốt phương án cho đồ án của bạn**

Tôi đề xuất kiến trúc chính thức như sau:

## **Production Database Architecture**

Phương án khuyến nghị

**Một Database trung tâm – nhiều tài khoản – dữ liệu được cô lập theo quyền**

- Frontend: React + TypeScript, deploy trên Internet.
- Backend: FastAPI, xác thực và phân quyền.
- Database: PostgreSQL managed trên cloud.
- Storage: Private Object Storage.
- AI: PyTorch model chạy trên Backend AI server.
- Authentication: Session/cookie bảo mật.
- Data isolation: `user_id` + kiểm tra quyền + PostgreSQL RLS.
- Backup: Database và hình ảnh.

  **Kết quả:** Nhiều người cùng sử dụng website nhưng mặc định không nhìn thấy ảnh, cây trồng, lịch sử và thông tin riêng của nhau.

**Một lưu ý cho đồ án:** Bạn không cần tạo một Database riêng cho mỗi người dùng. Làm như vậy sẽ phức tạp và tốn tài nguyên không cần thiết. Một PostgreSQL Database với thiết kế multi-user và cơ chế kiểm soát truy cập đúng là đủ cho quy mô đồ án và phiên bản sản phẩm ban đầu.

Đây cũng là kiến trúc tôi khuyên đưa thẳng vào tài liệu `ARCHITECTURE.md` và chương thiết kế hệ thống của báo cáo.