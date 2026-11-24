import React, { useEffect, useState } from "react";
import { Navigate, NavLink, Route, Routes, useNavigate } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Bell, Camera, ClipboardList, Home, Leaf, LogOut, Menu, Search,
  Settings, ShieldCheck, Sprout, Stethoscope, Users, X,
} from "lucide-react";
import { apiRequest, clearSession, getToken, jsonHeaders, setToken } from "../services/api";
import type { Dashboard, Diagnosis, Plant, PlantSpecies, User } from "../types/api";

const statusLabel: Record<string, string> = {
  diagnosed: "Có dấu hiệu bệnh",
  disease_detected: "Có dấu hiệu bệnh",
  healthy: "Khỏe mạnh",
  uncertain: "Chưa đủ tin cậy",
  unsupported_crop: "Ngoài lớp hỗ trợ",
  unknown_disease: "Chưa xác định bệnh",
  poor_image_quality: "Chất lượng ảnh chưa đạt",
  invalid_image: "Ảnh không hợp lệ",
};

const riskLabel: Record<string, string> = {
  none: "Không phát hiện", low: "Thấp", medium: "Trung bình", high: "Cao", unassessed: "Chưa đánh giá",
};

function useUser() {
  return useQuery({
    queryKey: ["me"],
    queryFn: () => apiRequest<User>("/api/v1/auth/me"),
    enabled: Boolean(getToken()),
    retry: false,
  });
}

function Protected({ children, admin = false }: { children: React.ReactNode; admin?: boolean }) {
  const { data: user, isLoading } = useUser();
  if (!getToken()) return <Navigate to="/login" replace />;
  if (isLoading) return <div className="page-loading">Đang tải tài khoản...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (admin && user.role !== "ADMIN") return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}

function Brand() {
  return <NavLink className="brand" to="/"><span className="brand-mark"><Leaf size={22} /></span><span>Smart Plant Care <b>AI</b></span></NavLink>;
}

function PublicLayout({ children }: { children: React.ReactNode }) {
  return <div className="public-shell">
    <header className="public-nav"><Brand /><nav><NavLink to="/diseases">Thư viện bệnh</NavLink><NavLink to="/login" className="nav-login">Đăng nhập</NavLink></nav></header>
    {children}
  </div>;
}

function Landing() {
  return <PublicLayout><main className="landing">
    <section className="landing-hero">
      <div><p className="eyebrow">NỀN TẢNG CHĂM SÓC CÂY THÔNG MINH</p><h1>Nhận diện lá cây.<br /><em>Hiểu sức khỏe cây trồng.</em></h1><p>Chụp ảnh lá để nhận kết quả AI, theo dõi diễn biến từng cây và lưu lại nhật ký chăm sóc.</p><div className="hero-actions"><NavLink className="button-primary" to="/login">Bắt đầu kiểm tra</NavLink><NavLink className="button-secondary" to="/diseases">Khám phá thư viện</NavLink></div></div>
      <div className="hero-visual"><div className="scan-card"><div className="scan-leaf">🌿</div><span>AI Plant Analysis</span><div className="scan-line" /></div></div>
    </section>
    <section className="feature-grid">
      <article><Camera /><h3>Chẩn đoán bằng ảnh</h3><p>Tải ảnh hoặc chụp trực tiếp bằng điện thoại.</p></article>
      <article><Stethoscope /><h3>Kết quả có ngữ cảnh</h3><p>Hiển thị bệnh, mức tin cậy, triệu chứng và khuyến nghị.</p></article>
      <article><Sprout /><h3>Theo dõi từng cây</h3><p>Lưu lịch sử, nhật ký chăm sóc và nhắc nhở.</p></article>
    </section>
  </main></PublicLayout>;
}

function AuthPage({ register = false }: { register?: boolean }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const mutation = useMutation({
    mutationFn: () => apiRequest<{ access_token: string; refresh_token?: string }>(
      register ? "/api/v1/auth/register" : "/api/v1/auth/login",
      { method: "POST", headers: jsonHeaders(), body: JSON.stringify(register ? { email, password, name } : { email, password }) },
      false,
    ),
    onSuccess: data => { setToken(data.access_token); navigate("/dashboard"); },
    onError: err => setError(err instanceof Error ? err.message : "Không thể xác thực"),
  });

  return <PublicLayout><main className="auth-page"><section className="auth-card">
    <p className="eyebrow">{register ? "THAM GIA SMART PLANT CARE" : "CHÀO MỪNG TRỞ LẠI"}</p>
    <h1>{register ? "Tạo tài khoản" : "Đăng nhập"}</h1>
    <form onSubmit={e => { e.preventDefault(); mutation.mutate(); }}>
      {register && <label>Họ và tên<input value={name} onChange={e => setName(e.target.value)} minLength={2} required /></label>}
      <label>Email<input type="email" value={email} onChange={e => setEmail(e.target.value)} required /></label>
      <label>Mật khẩu<input type="password" value={password} onChange={e => setPassword(e.target.value)} minLength={8} required /></label>
      {error && <div className="error-box">{error}</div>}
      <button className="button-primary" disabled={mutation.isPending}>{mutation.isPending ? "Đang xử lý..." : register ? "Tạo tài khoản" : "Đăng nhập"}</button>
    </form>
    <NavLink className="text-link" to={register ? "/login" : "/register"}>{register ? "Đã có tài khoản? Đăng nhập" : "Chưa có tài khoản? Đăng ký"}</NavLink>
  </section></main></PublicLayout>;
}

const navItems = [
  { to: "/dashboard", label: "Tổng quan", icon: Home },
  { to: "/diagnosis", label: "Chẩn đoán AI", icon: Camera },
  { to: "/plants", label: "Cây của tôi", icon: Sprout },
  { to: "/history", label: "Lịch sử", icon: ClipboardList },
  { to: "/diseases", label: "Thư viện bệnh", icon: Leaf },
  { to: "/care", label: "Chăm sóc", icon: Bell },
];

function AppShell({ children }: { children: React.ReactNode }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const { data: user } = useUser();
  const navigate = useNavigate();
  function logout() {
    clearSession();
    navigate("/login");
  }
  return <div className="app-shell">
    <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
      <div className="sidebar-brand"><Brand /><button className="mobile-close" onClick={() => setMenuOpen(false)}><X /></button></div>
      <nav>
        {navItems.map(item => <NavLink key={item.to} to={item.to} onClick={() => setMenuOpen(false)}><item.icon size={18} /><span>{item.label}</span></NavLink>)}
        {user?.role === "ADMIN" && <NavLink to="/admin"><ShieldCheck size={18} /><span>Quản trị</span></NavLink>}
      </nav>
      <div className="sidebar-user"><div className="avatar">{user?.name?.charAt(0).toUpperCase() ?? "U"}</div><div><b>{user?.name ?? "Tài khoản"}</b><small>{user?.role === "ADMIN" ? "Quản trị viên" : "Người trồng cây"}</small></div><button onClick={logout} aria-label="Đăng xuất"><LogOut size={17} /></button></div>
    </aside>
    {menuOpen && <button className="drawer-overlay" aria-label="Đóng menu" onClick={() => setMenuOpen(false)} />}
    <div className="app-main">
      <header className="app-header"><button className="menu-button" onClick={() => setMenuOpen(true)}><Menu /></button><div><p>SMART PLANT CARE</p><span>{user?.name ?? ""}</span></div><NavLink to="/notifications" className="header-icon"><Bell size={19} /></NavLink></header>
      <main className="workspace">{children}</main>
    </div>
  </div>;
}

function PageHeading({ eyebrow, title, action }: { eyebrow: string; title: string; action?: React.ReactNode }) {
  return <div className="page-heading"><div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1></div>{action}</div>;
}

function DashboardPage() {
  const dashboard = useQuery({ queryKey: ["dashboard"], queryFn: () => apiRequest<Dashboard>("/api/v1/analytics/dashboard") });
  if (dashboard.isLoading) return <div className="page-loading">Đang tải dashboard...</div>;
  if (dashboard.isError) return <div className="error-box">{dashboard.error instanceof Error ? dashboard.error.message : "Không thể tải dashboard"}</div>;
  const data = dashboard.data!;
  const total = data.total_predictions || 1;
  const healthy = data.healthy_plants;
  const diseased = data.diseased_plants;
  return <>
    <PageHeading eyebrow="TỔNG QUAN" title="Tình trạng trang trồng" action={<NavLink className="button-primary" to="/diagnosis">Kiểm tra lá cây</NavLink>} />
    <section className="stat-grid">
      <article><span><Sprout /></span><b>{data.total_plants}</b><p>Cây đang theo dõi</p></article>
      <article><span><Camera /></span><b>{data.total_predictions}</b><p>Lượt chẩn đoán</p></article>
      <article><span><Leaf /></span><b>{healthy}</b><p>Kết quả khỏe mạnh</p></article>
      <article><span><Stethoscope /></span><b>{diseased}</b><p>Có dấu hiệu bệnh</p></article>
    </section>
    <section className="dashboard-grid">
      <article className="panel"><div className="panel-heading"><div><p className="eyebrow">HOẠT ĐỘNG GẦN ĐÂY</p><h2>Lần kiểm tra mới nhất</h2></div></div>
        {data.recent_diagnoses.length ? <div className="activity-list">{data.recent_diagnoses.slice(0, 6).map((item, index) => <div className="activity-row" key={`${item.id}-${index}`}><span className={`activity-dot ${item.status}`} /><div><b>{item.disease?.name_vi ?? statusLabel[item.status] ?? item.status}</b><small>{item.plant?.name_vi ?? item.plant?.name}</small></div><strong>{item.confidence ? `${Math.round(item.confidence * 100)}%` : "-"}</strong></div>)}</div> : <div className="empty-state"><Camera /><h3>Chưa có lượt kiểm tra</h3><p>Tải ảnh lá để tạo kết quả đầu tiên.</p></div>}
      </article>
      <article className="panel"><div className="panel-heading"><p className="eyebrow">PHÂN BỐ KẾT QUẢ</p><h2>Sức khỏe hiện tại</h2></div>
        <div className="health-ring" style={{ "--healthy": `${Math.round((healthy / total) * 100)}%` } as React.CSSProperties}><strong>{Math.round((healthy / total) * 100)}%</strong><small>khỏe mạnh</small></div>
        <div className="legend"><span><i className="green" />Khỏe mạnh <b>{healthy}</b></span><span><i className="amber" />Bất thường <b>{diseased}</b></span></div>
      </article>
    </section>
  </>;
}

function DiagnosisPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");
  const [plantId, setPlantId] = useState("");
  const [note, setNote] = useState("");
  const [dragging, setDragging] = useState(false);
  const [fileError, setFileError] = useState("");
  const queryClient = useQueryClient();
  const plants = useQuery({ queryKey: ["plants"], queryFn: () => apiRequest<Plant[]>("/api/v1/my-plants") });
  const species = useQuery({ queryKey: ["plant-species"], queryFn: () => apiRequest<PlantSpecies[]>("/api/v1/plants") });
  const [expectedSpecies, setExpectedSpecies] = useState("");
  const diagnosis = useMutation({
    mutationFn: async () => {
      if (!file) throw new Error("Chọn hoặc chụp một ảnh lá");
      const form = new FormData();
      form.append("file", file);
      if (expectedSpecies) form.append("expected_species", expectedSpecies);
      if (note) form.append("note", note);
      const suffix = plantId ? `?plant_id=${encodeURIComponent(plantId)}` : "";
      return apiRequest<Diagnosis>(`/api/v1/diagnoses/predict${suffix}`, { method: "POST", body: form });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      queryClient.invalidateQueries({ queryKey: ["diagnoses"] });
    },
  });

  function chooseFile(selected: File | undefined) {
    if (!selected) return;
    setFileError("");
    if (!["image/jpeg", "image/png", "image/webp"].includes(selected.type)) {
      setFile(null);
      setFileError("Định dạng không hợp lệ. Chỉ dùng JPG, PNG hoặc WEBP.");
      return;
    }
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  }

  function removeFile() {
    if (preview) URL.revokeObjectURL(preview);
    setPreview("");
    setFile(null);
  }

  const result = diagnosis.data;
  return <>
    <PageHeading eyebrow="AI DISEASE DETECTION" title="Phân tích lá cây" />
    <section className="diagnosis-layout">
      <article className="panel upload-panel"
        onDragOver={e => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={e => { e.preventDefault(); setDragging(false); chooseFile(e.dataTransfer.files[0]); }}>
        {preview ? <div className="image-preview"><img src={preview} alt="Ảnh lá đã chọn" /><button onClick={removeFile} aria-label="Xóa ảnh"><X /></button></div> : <label className={`upload-zone ${dragging ? "dragging" : ""}`}>
          <input type="file" accept="image/jpeg,image/png,image/webp" capture="environment" onChange={e => chooseFile(e.target.files?.[0])} />
          <span className="upload-icon"><Camera /></span><b>Tải ảnh hoặc mở camera</b><small>Kéo thả JPG, PNG hoặc WEBP · tối đa 10 MB</small>
        </label>}
        {fileError && <div className="error-box">{fileError}</div>}
        <div className="form-grid">
          <label>Cây đang theo dõi<select value={plantId} onChange={e => setPlantId(e.target.value)}><option value="">Không gắn với cây</option>{plants.data?.map(plant => <option value={plant.id} key={plant.id}>{plant.name} · {plant.species}</option>)}</select></label>
          <label>Loài cây dự kiến<select value={expectedSpecies} onChange={e => setExpectedSpecies(e.target.value)}><option value="">Mặc định để AI xác định</option>{species.data?.map(item => <option value={item.id} key={item.id}>{item.name} · {item.name_en}</option>)}</select></label>
          <label className="full">Ghi chú<textarea value={note} onChange={e => setNote(e.target.value)} placeholder="Quan sát triệu chứng, thời điểm chụp, khu vực cây..." /></label>
        </div>
        {diagnosis.isError && <div className="error-box">{diagnosis.error instanceof Error ? diagnosis.error.message : "Không thể phân tích ảnh"}</div>}
        <button className="button-primary submit-diagnosis" disabled={!file || diagnosis.isPending} onClick={() => diagnosis.mutate()}>{diagnosis.isPending ? "Đang phân tích mô hình..." : "Phân tích bằng AI"}</button>
      </article>
      <article className="panel result-panel">
        {!result ? <div className="empty-state"><Stethoscope /><h3>Kết quả chẩn đoán</h3><p>Chọn ảnh lá và chạy phân tích để xem kết quả.</p></div> : <DiagnosisResult result={result} />}
      </article>
    </section>
  </>;
}

function DiagnosisResult({ result }: { result: Diagnosis }) {
  const assessment = result.health_assessment;
  return <div className="diagnosis-result">
    <div className="result-heading"><span className={`status-badge ${result.status}`}>{statusLabel[result.status] ?? result.status}</span>{result.model && <small>Model {result.model.version}</small>}</div>
    <h2>{result.disease?.name_vi || "Chưa xác định"}</h2>
    {result.plant?.name && <p className="result-plant">{result.plant.name_vi || result.plant.name}</p>}
    {result.prediction ? <>
      {result.message && <div className="notice">{result.message}</div>}
      <div className="confidence"><div><span>Độ tin cậy</span><b>{Math.round(result.prediction.confidence * 100)}%</b></div><div className="confidence-track"><i style={{ width: `${Math.round(result.prediction.confidence * 100)}%` }} /></div></div>
      <div className="top-predictions"><p className="eyebrow">TOP 3 DỰ ĐOÁN</p>{result.prediction.top_predictions.map((item, index) => <div key={item.class}><span>{index + 1}. {item.class}</span><b>{Math.round(item.confidence * 100)}%</b></div>)}</div>
    </> : <div className="notice">{result.message || "Không thể đưa ra kết luận bệnh cho ảnh này."}</div>}
    {assessment && <div className="risk-row"><span>Mức nguy cơ</span><b className={assessment.risk}>{riskLabel[assessment.risk]}</b></div>}
    {result.symptoms && <InfoBlock title="Triệu chứng" text={result.symptoms} />}
    {result.cause && <InfoBlock title="Nguyên nhân" text={result.cause} />}
    <InfoBlock title="Khuyến nghị" text={result.recommendation} />
    {result.prevention && <InfoBlock title="Phòng ngừa" text={result.prevention} />}
    {assessment?.scope && <p className="scope-note">{assessment.scope}</p>}
    {result.explainability?.heatmap && <div className="heatmap-block"><p className="eyebrow">{result.explainability.method === "grad-cam" ? "GRAD-CAM" : "BẢN ĐỒ INPUT-GRADIENT (XẤP XỈ)"}</p><img src={result.explainability.heatmap} alt="Bản đồ vùng ảnh ảnh hưởng dự đoán" /></div>}
  </div>;
}

function InfoBlock({ title, text }: { title: string; text: string }) {
  return <div className="info-block"><b>{title}</b><p>{text}</p></div>;
}

function PlantsPage() {
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<Plant | null>(null);
  const plants = useQuery({ queryKey: ["plants"], queryFn: () => apiRequest<Plant[]>("/api/v1/my-plants") });
  const species = useQuery({ queryKey: ["plant-species"], queryFn: () => apiRequest<PlantSpecies[]>("/api/v1/plants") });
  const [name, setName] = useState("");
  const [speciesId, setSpeciesId] = useState("");
  const [location, setLocation] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const save = useMutation({
    mutationFn: () => apiRequest<Plant>(editing ? `/api/v1/my-plants/${editing.id}` : "/api/v1/my-plants", {
      method: editing ? "PUT" : "POST", headers: jsonHeaders(),
      body: JSON.stringify({ name, species: speciesId, location: location || null, notes: notes || null }),
    }),
    onSuccess: () => { setOpen(false); setEditing(null); setName(""); setSpeciesId(""); setLocation(""); setNotes(""); queryClient.invalidateQueries({ queryKey: ["plants"] }); queryClient.invalidateQueries({ queryKey: ["dashboard"] }); },
    onError: err => setError(err instanceof Error ? err.message : "Không thể lưu cây"),
  });
  const remove = useMutation({
    mutationFn: (id: string) => apiRequest<{ message: string }>(`/api/v1/my-plants/${id}`, { method: "DELETE" }),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ["plants"] }); queryClient.invalidateQueries({ queryKey: ["dashboard"] }); },
  });
  function openAdd() { setEditing(null); setName(""); setSpeciesId(species.data?.[0]?.id ?? ""); setLocation(""); setNotes(""); setError(""); setOpen(true); }
  function openEdit(plant: Plant) { setEditing(plant); setName(plant.name); setSpeciesId(plant.species); setLocation(plant.location ?? ""); setNotes(plant.notes ?? ""); setError(""); setOpen(true); }

  return <>
    <PageHeading eyebrow="QUẢN LÝ CÂY" title="Cây của tôi" action={<button className="button-primary" onClick={openAdd}>+ Thêm cây</button>} />
    {plants.isLoading ? <div className="page-loading">Đang tải danh sách cây...</div> : plants.data?.length ? <section className="plant-grid-page">{plants.data.map(plant => <article className="plant-card-page" key={plant.id}><div className="plant-card-icon">🌿</div><div><p className="eyebrow">{plant.species}</p><h2>{plant.name}</h2>{plant.location && <p><b>Khu vực:</b> {plant.location}</p>}<p className="muted">{plant.notes || "Chưa có ghi chú"}</p></div><div className="card-actions"><button className="button-secondary" onClick={() => openEdit(plant)}>Sửa</button><button className="button-danger" onClick={() => remove.mutate(plant.id)}>Xóa</button></div></article>)}</section> : <div className="panel empty-state"><Sprout /><h3>Chưa có cây theo dõi</h3><p>Thêm cây để gắn kết quả chẩn đoán và theo dõi lịch sử.</p><button className="button-primary" onClick={openAdd}>Thêm cây đầu tiên</button></div>}
    {open && <div className="modal-backdrop" onMouseDown={e => { if (e.target === e.currentTarget) setOpen(false); }}><section className="modal"><div className="modal-heading"><div><p className="eyebrow">{editing ? "CHỈNH SỬA CÂY" : "THÊM CÂY"}</p><h2>{editing ? "Cập nhật hồ sơ" : "Tạo hồ sơ cây mới"}</h2></div><button className="icon-button" onClick={() => setOpen(false)}><X /></button></div><form className="plant-form" onSubmit={e => { e.preventDefault(); save.mutate(); }}>
      <label>Tên do bạn đặt<input value={name} onChange={e => setName(e.target.value)} required maxLength={120} /></label>
      <label>Loài đã huấn luyện<select value={speciesId} onChange={e => setSpeciesId(e.target.value)} required>{species.data?.map(item => <option key={item.id} value={item.id}>{item.name} · {item.name_en}</option>)}</select></label>
      <label>Khu vực trồng<input value={location} onChange={e => setLocation(e.target.value)} maxLength={120} /></label>
      <label>Ghi chú<textarea value={notes} onChange={e => setNotes(e.target.value)} maxLength={1000} /></label>
      {error && <div className="error-box">{error}</div>}
      <div className="modal-actions"><button type="button" className="button-secondary" onClick={() => setOpen(false)}>Hủy</button><button className="button-primary" disabled={save.isPending}>{save.isPending ? "Đang lưu..." : "Lưu cây"}</button></div>
    </form></section></div>}
  </>;
}

function HistoryPage() {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const history = useQuery({
    queryKey: ["diagnoses", status],
    queryFn: () => apiRequest<Diagnosis[]>(`/api/v1/diagnoses${status ? `?status=${encodeURIComponent(status)}` : ""}`),
  });
  const filtered = history.data?.filter(item => `${item.plant?.name} ${item.disease?.name_vi} ${item.disease?.name}`.toLowerCase().includes(search.toLowerCase()));
  return <>
    <PageHeading eyebrow="LỊCH SỬ" title="Các lần chẩn đoán" />
    <section className="toolbar"><label><Search size={16} /><input value={search} onChange={e => setSearch(e.target.value)} placeholder="Tìm theo cây hoặc bệnh" /></label><select value={status} onChange={e => setStatus(e.target.value)}><option value="">Tất cả trạng thái</option><option value="diagnosed">Có dấu hiệu bệnh</option><option value="healthy">Khỏe mạnh</option><option value="uncertain">Chưa chắc chắn</option><option value="unsupported_crop">Ngoài lớp hỗ trợ</option></select></section>
    {history.isLoading ? <div className="page-loading">Đang tải lịch sử...</div> : filtered?.length ? <section className="history-list">{filtered.map(item => <article className="history-row" key={item.id}><span className={`history-icon ${item.status}`}><Leaf /></span><div><b>{item.disease?.name_vi || statusLabel[item.status] || item.status}</b><small>{item.plant?.name_vi || item.plant?.name || "Chưa gắn cây"} · {item.created_at ? new Date(item.created_at).toLocaleString("vi-VN") : ""}</small></div><strong>{item.confidence ? `${Math.round(item.confidence * 100)}%` : "-"}</strong><span className={`status-badge ${item.status}`}>{statusLabel[item.status] ?? item.status}</span></article>)}</section> : <div className="panel empty-state"><ClipboardList /><h3>Chưa có lịch sử</h3><p>Các kết quả chẩn đoán sẽ xuất hiện tại đây.</p></div>}
  </>;
}

type Disease = { id: string; code: string; plant: string; name: string; name_vi: string; pathogen?: string; symptoms: string; conditions: string; treatment: string; prevention: string };

function DiseasesPage() {
  const [search, setSearch] = useState("");
  const [plant, setPlant] = useState("");
  const diseases = useQuery({ queryKey: ["diseases", search, plant], queryFn: () => apiRequest<Disease[]>(`/api/v1/diseases${search ? `?search=${encodeURIComponent(search)}${plant ? `&plant=${encodeURIComponent(plant)}` : ""}` : plant ? `?plant=${encodeURIComponent(plant)}` : ""}`) });
  const catalog = useQuery({ queryKey: ["disease-catalog"], queryFn: () => apiRequest<Disease[]>("/api/v1/diseases") });
  const plants = Array.from(new Set((catalog.data ?? []).map(item => item.plant))).sort();
  return <>
    <PageHeading eyebrow="KIẾN THỨC CÂY TRỒNG" title="Thư viện bệnh" />
    <section className="library-summary"><div><b>{catalog.data?.length ?? "-"}</b><span>lớp/bệnh trong thư viện</span></div><div><b>{plants.length}</b><span>loài thực vật</span></div></section>
    <section className="toolbar"><label><Search size={16} /><input value={search} onChange={e => setSearch(e.target.value)} placeholder="Tìm tên bệnh..." /></label><select value={plant} onChange={e => setPlant(e.target.value)}><option value="">Tất cả loại cây</option>{plants.map(item => <option key={item} value={item}>{item}</option>)}</select></section>
    {diseases.isLoading ? <div className="page-loading">Đang tải thư viện...</div> : diseases.data?.length ? <section className="disease-grid">{diseases.data.map(disease => <article className="disease-card" key={disease.id}><div className="disease-icon"><Leaf /></div><p className="eyebrow">{disease.plant}</p><h2>{disease.name_vi}</h2><p>{disease.symptoms}</p><details><summary>Xem nguyên nhân và hướng dẫn</summary><p><b>Tác nhân:</b> {disease.pathogen || "Chưa cập nhật"}</p><p><b>Điều kiện:</b> {disease.conditions}</p><p><b>Xử lý:</b> {disease.treatment}</p><p><b>Phòng ngừa:</b> {disease.prevention}</p></details></article>)}</section> : <div className="panel empty-state"><Leaf /><h3>Không tìm thấy bệnh</h3><p>Thử thay đổi từ khóa hoặc bộ lọc loại cây.</p></div>}
  </>;
}

type CareLog = { id: string; plant_id?: string; kind: string; note?: string; occurred_at: string };
type Reminder = { id: string; plant_id?: string; kind: string; due_at: string; note?: string; completed: boolean };

function CarePage() {
  const queryClient = useQueryClient();
  const [kind, setKind] = useState("Kiểm tra lá");
  const [note, setNote] = useState("");
  const [dueAt, setDueAt] = useState("");
  const logs = useQuery({ queryKey: ["care"], queryFn: () => apiRequest<CareLog[]>("/api/v1/care-logs") });
  const reminders = useQuery({ queryKey: ["reminders"], queryFn: () => apiRequest<Reminder[]>("/api/v1/reminders") });
  const plants = useQuery({ queryKey: ["plants"], queryFn: () => apiRequest<Plant[]>("/api/v1/my-plants") });
  const [plantId, setPlantId] = useState("");
  const careMutation = useMutation({
    mutationFn: () => apiRequest("/api/v1/care-logs", { method: "POST", headers: jsonHeaders(), body: JSON.stringify({ kind, note: note || null, plant_id: plantId || null }) }),
    onSuccess: () => { setNote(""); queryClient.invalidateQueries({ queryKey: ["care"] }); },
  });
  const reminderMutation = useMutation({
    mutationFn: () => apiRequest("/api/v1/reminders", { method: "POST", headers: jsonHeaders(), body: JSON.stringify({ kind, due_at: new Date(dueAt).toISOString(), note: note || null, plant_id: plantId || null }) }),
    onSuccess: () => { setDueAt(""); setNote(""); queryClient.invalidateQueries({ queryKey: ["reminders"] }); },
  });
  const completeReminder = useMutation({
    mutationFn: (id: string) => apiRequest(`/api/v1/reminders/${id}/complete`, { method: "POST", headers: jsonHeaders(), body: JSON.stringify({ completed: true }) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["reminders"] }),
  });

  return <>
    <PageHeading eyebrow="NHẬT KÝ CHĂM SÓC" title="Lịch chăm sóc" />
    <section className="care-layout">
      <article className="panel"><div className="panel-heading"><p className="eyebrow">THÊM HOẠT ĐỘNG</p><h2>Ghi nhật ký</h2></div><form className="plant-form" onSubmit={e => { e.preventDefault(); careMutation.mutate(); }}>
        <label>Loại hoạt động<select value={kind} onChange={e => setKind(e.target.value)}><option>Kiểm tra lá</option><option>Tưới nước</option><option>Bón phân</option><option>Tỉa lá</option><option>Xử lý bệnh</option><option>Hoạt động khác</option></select></label>
        <label>Cây<select value={plantId} onChange={e => setPlantId(e.target.value)}><option value="">Chung cho tài khoản</option>{plants.data?.map(plant => <option key={plant.id} value={plant.id}>{plant.name}</option>)}</select></label>
        <label>Ghi chú<textarea value={note} onChange={e => setNote(e.target.value)} /></label>
        <button className="button-primary" disabled={careMutation.isPending}>{careMutation.isPending ? "Đang lưu..." : "Lưu nhật ký"}</button>
      </form></article>
      <article className="panel"><div className="panel-heading"><p className="eyebrow">NHẮC NHỞ</p><h2>Lịch sắp tới</h2></div><form className="plant-form" onSubmit={e => { e.preventDefault(); if (dueAt) reminderMutation.mutate(); }}>
        <label>Ngày và giờ<input type="datetime-local" value={dueAt} onChange={e => setDueAt(e.target.value)} required /></label>
        <button className="button-primary" disabled={reminderMutation.isPending}>Tạo nhắc nhở</button>
      </form><div className="reminder-list">{reminders.data?.map(reminder => <label className="reminder-row" key={reminder.id}><input type="checkbox" checked={Boolean(reminder.completed)} onChange={() => completeReminder.mutate(reminder.id)} /><div><b>{reminder.kind}</b><small>{new Date(reminder.due_at).toLocaleString("vi-VN")}</small></div></label>)}</div></article>
    </section>
    <section className="panel care-history"><div className="panel-heading"><p className="eyebrow">NHẬT KÝ GẦN ĐÂY</p><h2>Hoạt động đã lưu</h2></div>{logs.data?.length ? logs.data.map(log => <div className="history-row" key={log.id}><span className="history-icon"><Sprout /></span><div><b>{log.kind}</b><small>{log.note || "Không có ghi chú"} · {new Date(log.occurred_at).toLocaleString("vi-VN")}</small></div></div>) : <div className="empty-state"><ClipboardList /><p>Chưa có hoạt động chăm sóc.</p></div>}</section>
  </>;
}

function NotificationsPage() {
  const queryClient = useQueryClient();
  const notifications = useQuery({ queryKey: ["notifications"], queryFn: () => apiRequest<Array<{ id: string; title: string; message: string; is_read: number; created_at: string }>>("/api/v1/notifications") });
  const read = useMutation({
    mutationFn: (id: string) => apiRequest(`/api/v1/notifications/${id}/read`, { method: "POST" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notifications"] }),
  });
  return <><PageHeading eyebrow="THÔNG BÁO" title="Thông báo của tôi" /><section className="panel">{notifications.data?.length ? notifications.data.map(item => <button className={`notification-row ${item.is_read ? "read" : ""}`} key={item.id} onClick={() => read.mutate(item.id)}><Bell /><div><b>{item.title}</b><p>{item.message}</p><small>{new Date(item.created_at).toLocaleString("vi-VN")}</small></div></button>) : <div className="empty-state"><Bell /><h3>Không có thông báo mới</h3></div>}</section></>;
}

function AdminPage() {
  const queryClient = useQueryClient();
  const [userSearch, setUserSearch] = useState("");
  const users = useQuery({ queryKey: ["admin-users"], queryFn: () => apiRequest<Array<{ id: string; email: string; name: string; role: string; is_active: boolean | number }>>("/api/v1/admin/users") });
  const scans = useQuery({ queryKey: ["admin-scans"], queryFn: () => apiRequest<Array<{ id: string; plant: string; disease_code: string; status: string; confidence: number }>>("/api/v1/admin/scans") });
  const models = useQuery({ queryKey: ["admin-models"], queryFn: () => apiRequest<Array<{ id: string; name: string; version: string; status: string }>>("/api/v1/admin/models") });
  const evaluation = useQuery({ queryKey: ["admin-evaluation"], queryFn: () => apiRequest<{ evaluation: Record<string, number>; metrics: string[] }>("/api/v1/admin/model-evaluations") });
  const audit = useQuery({ queryKey: ["admin-audit"], queryFn: () => apiRequest<Array<{ id: string; actor_id: string; action: string; target_type: string; created_at: string }>>("/api/v1/admin/audit-logs") });
  const lockUser = useMutation({ mutationFn: (userId: string) => apiRequest(`/api/v1/admin/users/${userId}/lock`, { method: "POST" }), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin-users"] }) });
  const visibleUsers = users.data?.filter(user => `${user.name} ${user.email}`.toLowerCase().includes(userSearch.toLowerCase()));
  return <>
    <PageHeading eyebrow="ADMINISTRATION" title="Quản trị hệ thống" />
    <section className="stat-grid">
      <article><span><Users /></span><b>{users.data?.length ?? "-"}</b><p>Người dùng</p></article>
      <article><span><Camera /></span><b>{scans.data?.length ?? "-"}</b><p>Lượt dự đoán</p></article>
      <article><span><ShieldCheck /></span><b>{models.data?.length ?? "-"}</b><p>Phiên bản model</p></article>
      <article><span><Settings /></span><b>{audit.data?.length ?? "-"}</b><p>Sự kiện audit</p></article>
    </section>
    <section className="dashboard-grid">
      <article className="panel"><div className="panel-heading"><p className="eyebrow">MODEL EVALUATION</p><h2>Chỉ số thực tế</h2></div>{evaluation.isError ? <div className="notice">Chưa có báo cáo đánh giá model.</div> : evaluation.data ? <div className="metric-grid">{Object.entries(evaluation.data.evaluation).filter(([key]) => key !== "classes").map(([key, value]) => typeof value === "number" && <div key={key}><small>{key}</small><b>{key.includes("accuracy") || key.includes("f1") || key.includes("precision") || key.includes("recall") ? `${(value * 100).toFixed(1)}%` : value}</b></div>)}</div> : <div className="page-loading">Đang tải metrics...</div>}</article>
      <article className="panel"><div className="panel-heading"><p className="eyebrow">NGƯỜI DÙNG</p><h2>Quản lý tài khoản</h2></div><section className="toolbar"><label><Search size={16} /><input value={userSearch} onChange={event => setUserSearch(event.target.value)} placeholder="Tìm tên hoặc email" /></label></section><div className="admin-table">{visibleUsers?.map(user => <div key={user.id}><b>{user.name}</b><span>{user.email}</span><em>{user.role} · {user.is_active ? "Đang hoạt động" : "Đã khóa"}</em>{user.role !== "ADMIN" && <button className="button-secondary" disabled={lockUser.isPending} onClick={() => lockUser.mutate(user.id)}>{user.is_active ? "Khóa tài khoản" : "Mở khóa"}</button>}</div>)}</div></article>
    </section>
  </>;
}

function ProfilePage() {
  const [name, setName] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const me = useUser();
  useEffect(() => { if (me.data) setName(me.data.name); }, [me.data]);
  const mutation = useMutation({
    mutationFn: async () => {
      await apiRequest("/api/v1/auth/me", { method: "PUT", headers: jsonHeaders(), body: JSON.stringify({ name }) });
      if (currentPassword && newPassword) await apiRequest("/api/v1/auth/password", { method: "PUT", headers: jsonHeaders(), body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }) });
    },
    onSuccess: () => setMessage("Cập nhật hồ sơ thành công"),
  });
  return <><PageHeading eyebrow="TÀI KHOẢN" title="Hồ sơ cá nhân" /><section className="panel profile-page"><form className="plant-form" onSubmit={e => { e.preventDefault(); mutation.mutate(); }}><label>Họ và tên<input value={name} onChange={e => setName(e.target.value)} required /></label><label>Email<input value={me.data?.email ?? ""} disabled /></label><label>Mật khẩu hiện tại<input type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} /></label><label>Mật khẩu mới<input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} minLength={8} /></label>{message && <div className="success-box">{message}</div>}<button className="button-primary" disabled={mutation.isPending}>Lưu thay đổi</button></form></section></>;
}

function DiseaseLibraryRoute() {
  if (getToken()) {
    return <Protected><AppShell><DiseasesPage /></AppShell></Protected>;
  }
  return <PublicLayout><main className="public-content"><DiseasesPage /></main></PublicLayout>;
}

export function App() {
  return <Routes>
    <Route path="/" element={<Landing />} />
    <Route path="/login" element={<AuthPage />} />
    <Route path="/register" element={<AuthPage register />} />
    <Route path="/diseases" element={<DiseaseLibraryRoute />} />
    <Route path="/*" element={<Protected><AppShell><Routes>
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/diagnosis" element={<DiagnosisPage />} />
      <Route path="/plants" element={<PlantsPage />} />
      <Route path="/history" element={<HistoryPage />} />
      <Route path="/diseases" element={<DiseasesPage />} />
      <Route path="/care" element={<CarePage />} />
      <Route path="/notifications" element={<NotificationsPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/admin" element={<Protected admin><AdminPage /></Protected>} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes></AppShell></Protected>} />
  </Routes>;
}
