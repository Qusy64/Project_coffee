import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import random
from datetime import datetime

data = {}
gia_ca = {}         

def load_gia_ca(file_path, gia_ca):
    """
    Đọc dữ liệu từ file CSV và lưu giá bán theo ngày vào gia_ca.

    Hàm này mở file CSV, đọc từng dòng và tách dữ liệu ngày và giá bán. Nếu dữ liệu ngày thuộc năm 2024, giá bán sẽ được lưu vào dictionary `gia_ca` với ngày là key và giá là value.

    Args:
        file_path (str): Đường dẫn đến file CSV chứa dữ liệu ngày và giá bán.
        gia_ca (dict): Dictionary sẽ chứa dữ liệu ngày và giá bán. Key là chuỗi ngày (định dạng 'YYYY-MM-DD'),và value là giá bán.

    Returns:
        None: Hàm này không trả về giá trị. Dữ liệu được cập nhật trực tiếp vào dictionary `gia_ca`.
    """
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = row["ngay"].strip() if row["ngay"] else ""  
            if data:  
                ngay, gia = data.split(":")
                ngay = ngay.strip()  
                gia = gia.strip()  
                if "2024-" in ngay:  
                    gia_ca[ngay] = float(gia)  

load_gia_ca("gia_ca.csv", gia_ca)

def tinh_trung_binh_2024(gia_ca):
    """
    Tính giá bán trung bình trong năm 2024 từ dữ liệu giá theo ngày.

    Args:
        gia_ca (dict): Một dictionary với key là chuỗi ngày (định dạng 'YYYY-MM-DD') và value là giá bán của ngày đó.

    Returns:
        float | None: Giá trung bình của các ngày trong năm 2024.
    """
    tong = dem = 0
    for ngay, gia in gia_ca.items():  
        if "2024-" in ngay: 
            tong += gia
            dem += 1
    return tong / dem

trung_binh = tinh_trung_binh_2024(gia_ca)

def save_data_to_file():
    """
    Lưu dữ liệu giá bán vào file CSV.

    Hàm này mở file CSV với chế độ ghi và lưu dữ liệu từ `data` vào file. Mỗi dòng trong file sẽ chứa một cặp giá trị: ngày và giá bán tương ứng. Nếu file không tồn tại, nó sẽ được tạo mới.
    File được lưu với định dạng CSV, mỗi dòng sẽ có hai giá trị: 'ngay' (chuỗi ngày) và 'gia' (giá bán dưới dạng số).

    Args:
        None: Hàm này không nhận bất kỳ đối số nào.

    Returns:
        None: Hàm này không trả về giá trị. Dữ liệu được lưu trực tiếp vào file được chỉ định trong `DATA_FILE`.
    """
    with open("da_ban.csv", "a", encoding="utf-8", newline="") as file:
        for ngay, gia in data.items():
            try:
                ngay_date = datetime.strptime(ngay, "%d/%m/%Y")
                ngay_chuan = ngay_date.strftime("%Y-%m-%d")
                file.write(f"{ngay_chuan}: {gia}\n")  
            except ValueError:
                print(f"Ngày không hợp lệ: {ngay}")

def load_data_from_file():
    """
    Đọc dữ liệu từ file CSV và cập nhật vào biến `data`.

    Hàm này sẽ đọc từng dòng trong file `gia_ca.csv`, chuyển đổi ngày và giá bán
    thành dạng phù hợp, và lưu vào biến `data` dưới dạng dictionary.
    """
    with open("gia_ca.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            gia = row["gia"]
            if gia:  
                data[row["ngay"]] = float(gia)

def tinh_loi_nhuan():
    """
    Tính toán lợi nhuận và đánh giá vụ mùa dựa trên chi phí, sản lượng và giá bán.

    Lấy dữ liệu đầu vào từ các Entry widget (entry_chi_phi, entry_san_luong, entry_gia_ban), tính lợi nhuận và đưa ra đánh giá chất lượng vụ mùa và mức giá bán hiện tại so với trung bình năm trước.

    Kết quả sẽ được hiển thị lên các Label giao diện người dùng:
    - `label_ket_qua`: Hiển thị lợi nhuận tính được.
    - `label_danh_gia`: Đưa ra nhận xét về giá bán hiện tại.
    - `label_danh_gia_vu_mua`: Đưa ra đánh giá năng suất vụ mùa.

    Args:
        None

    Returns:
        None
    """
    try:
        chi_phi = float(entry_chi_phi.get())  # type: ignore
        san_luong = float(entry_san_luong.get())  # type: ignore
        gia_ban = float(entry_gia_ban.get())  # type: ignore

        tong_thu = san_luong * gia_ban
        loi_nhuan = tong_thu - chi_phi

        color = "green" if loi_nhuan >= 0 else "red"
        
        if gia_ban >= trung_binh + 10000:
            danh_gia = "✅ Giá bán tốt so với trung bình năm trước! "
            color = "dark green"
        elif gia_ban >= trung_binh:
            danh_gia = "🟢 Giá bán khá ổn."
            color = "green"
        elif gia_ban >= trung_binh - 5000:
            danh_gia = "🟠 Không nên bán, hãy chờ đợi giá bán tăng."
            color = "orangered"
        else:
            danh_gia = "❗️ Bị lỗ tiền công! Chờ giá lên đi ."
            color = "red"

        if san_luong < chi_phi * 0.00001:
            danh_gia_vu_mua = "❗️ Sản lượng quá thấp so với chi phí đầu tư. Cần cải thiện năng suất."
            color_vu_mua = "red"
        elif san_luong < chi_phi * 0.00005:
            danh_gia_vu_mua = "🟠 Sản lượng chưa tốt lắm! Cần cải thiện sản lượng ."
            color_vu_mua = "orangered"
        elif san_luong < chi_phi * 0.00012:
            danh_gia_vu_mua = "🟢 Sản lượng vừa phải, đạt mức trung bình."
            color_vu_mua = "green"
        else:
            danh_gia_vu_mua = "✅ Sản lượng tốt."
            color_vu_mua = "dark green"

        label_ket_qua.config(
            text=f"Lợi nhuận: {loi_nhuan:,.0f} VND",
            foreground=color
        )
        label_danh_gia.config(
            text=danh_gia,
            foreground=color
        )
        label_danh_gia_vu_mua.config( 
            text=danh_gia_vu_mua,
            foreground=color_vu_mua
        )

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ", icon="warning")

def xem_lich_su():
    """
    Hiển thị cửa sổ phụ chứa lịch sử giá đã bán, cho phép người dùng xem và xóa từng dòng dữ liệu.
    """
    # Đọc dữ liệu từ file da_ban.csv
    data = {}  # Khởi tạo dictionary để lưu dữ liệu từ file
    try:
        with open("da_ban.csv", "r", encoding="utf-8") as file:
            for line in file:
                try:
                    ngay, gia = line.strip().split(": ")
                    # Chuyển đổi ngày từ dạng string thành datetime
                    ngay_date = datetime.strptime(ngay, "%Y-%m-%d")
                    # Thêm vào dictionary
                    data[ngay_date.strftime("%d/%m/%Y")] = float(gia)
                except ValueError:
                    print(f"Không thể đọc dòng: {line}")
    except FileNotFoundError:
        print("File da_ban.csv không tồn tại, chưa có dữ liệu.")
    
    def xoa_gia_ban():
        """
        Khi người dùng chọn một dòng và nhấn nút xóa:
        - Dữ liệu tương ứng sẽ bị xóa khỏi bảng.
        - Cập nhật lại file CSV bằng cách gọi hàm `save_data_to_file()`.
        - Hiển thị thông báo xác nhận.
        """
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một dòng để xóa.")
            return

        values = tree.item(selected_item[0], "values")
        ngay = values[0]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa giá bán ngày {ngay}?"):
            tree.delete(selected_item)
            data.pop(ngay, None)
            save_data_to_file()  
            messagebox.showinfo("Đã xóa", f"Đã xóa giá bán ngày {ngay}")

    window = tk.Toplevel(app)
    window.title("Lịch sử giá bán của bạn")
    window.geometry("500x500")
    window.configure(bg="#A8E6CF")

    frame = tk.Frame(window, bg="#A8E6CF")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    cols = ("Ngày", "Giá bán (VND/kg)")
    tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
    tree.heading("Ngày", text="Ngày")
    tree.heading("Giá bán (VND/kg)", text="Giá bán (VND/kg)")
    tree.pack(fill="both", expand=True, side="left")

    for ngay, gia in sorted(data.items()):
        tree.insert("", "end", values=(ngay, f"{gia:,.0f}"))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    btn_xoa = ttk.Button(window, text="🗑 XÓA GIÁ BÁN ĐÃ CHỌN", command=xoa_gia_ban)
    btn_xoa.pack(pady=10, ipadx=10)

def mo_cua_so_bieu_do():
    """
    Mở cửa sổ phụ hiển thị chuỗi biểu đồ giá cà phê từ các năm, cho phép người dùng chuyển qua lại giữa các ảnh biểu đồ.

    Cửa sổ bao gồm:
    - Một khung chính hiển thị ảnh biểu đồ giá cà phê từ các file `gia_ca_2015.png` đến `gia_ca_2024.png`.
    - Hai nút điều hướng "← Năm trước" và "Năm sau →" để chuyển đổi giữa các ảnh theo thứ tự năm.
    - Nếu không tải được ảnh tại một vị trí nào đó, hiển thị thông báo lỗi thay cho ảnh.

    Args:
        None

    Returns:
        None
    """
    window = tk.Toplevel(app)
    window.title("Biểu đồ giá cà phê")
    window.geometry("800x600")
    window.configure(bg="#A8E6CF")

    image_files = [f"gia_ca_{i}.png" for i in range(2015, 2025)]
    images = []

    for file in image_files:
        try:
            img = tk.PhotoImage(file=file)
            img = img.subsample(1, 1)
            images.append(img)
        except Exception:
            images.append(None)

    current_index = [0]

    img_label = tk.Label(window, bg="#A8E6CF")
    img_label.pack(pady=20)

    def update_image():
        """
        Cập nhật hình ảnh biểu đồ đang hiển thị trong giao diện.

        Args:
            None

        Returns:
            None
        """
        img = images[current_index[0]]
        if img:
            img_label.config(image=img, text="")
            img_label.image = img
        else:
            img_label.config(text=f"Không thể tải ảnh số {current_index[0] + 1}", image="", font=("Comic Sans MS", 12))

    def next_image():
        """
        Chuyển sang biểu đồ năm sau (ảnh tiếp theo) nếu còn ảnh trong danh sách.

        Args:
            None

        Returns:
            None
        """
        if current_index[0] < len(images) - 1:
            current_index[0] += 1
            update_image()

    def prev_image():
        """
        Quay về biểu đồ năm trước (ảnh trước đó) nếu còn ảnh trong danh sách.

        Args:
            None

        Returns:
            None
        """
        if current_index[0] > 0:
            current_index[0] -= 1
            update_image()

    btn_frame = tk.Frame(window, bg="#A8E6CF")
    btn_frame.pack()

    prev_btn = tk.Button(btn_frame, text="← Năm trước", command=prev_image)
    prev_btn.pack(side=tk.LEFT, padx=10)

    next_btn = tk.Button(btn_frame, text="Năm sau →", command=next_image)
    next_btn.pack(side=tk.LEFT, padx=10)

    update_image()

def them_gia_ban():
    """
    Mở một cửa sổ mới cho phép người dùng nhập và lưu giá bán cà phê theo ngày.

    Trong cửa sổ này, người dùng có thể nhập:
    - Ngày, tháng, năm (dưới dạng số)
    - Giá bán tương ứng (VND/kg)

    Args:
        None

    Returns:
        None
    """
    def save_new_price():
        """
        Lưu giá bán mới được người dùng nhập vào giao diện.

        Hàm này sẽ:
        - Lấy thông tin ngày, tháng, năm và giá bán từ các ô nhập liệu.
        - Kiểm tra định dạng hợp lệ (ngày, tháng, năm phải là số).
        - Kết hợp thành chuỗi ngày đầy đủ (dd/mm/yyyy) và lưu giá bán.
        - Ghi dữ liệu mới vào file lưu trữ bằng `save_data_to_file()`.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError: Nếu người dùng nhập ngày, tháng hoặc năm không phải là số, hoặc giá bán không hợp lệ.
        """
        try:
            ngay = entry_ngay.get()
            thang = entry_thang.get()
            nam = entry_nam.get()
            gia = float(entry_gia_moi.get())

            if not (ngay.isdigit() and thang.isdigit() and nam.isdigit()):
                raise ValueError("Ngày, tháng, năm phải là số")

            ngay_full = f"{int(ngay):02d}/{int(thang):02d}/{nam}"

            data[ngay_full] = gia
            save_data_to_file()
            messagebox.showinfo("Thành công", f"Đã lưu giá {gia:,.0f} VND cho ngày {ngay_full}")
            entry_ngay.delete(0, tk.END)
            entry_thang.delete(0, tk.END)
            entry_nam.delete(0, tk.END)
            entry_gia_moi.delete(0, tk.END)
            new_window.destroy()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng!", icon="warning")

    new_window = tk.Toplevel(app)
    new_window.title("Nhập giá bán mới")
    new_window.geometry("400x300")
    new_window.configure(bg="#A8E6CF")

    add_frame = ttk.Frame(new_window)
    add_frame.pack(padx=20, pady=20)

    ttk.Label(add_frame, text="Ngày:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_ngay = ttk.Entry(add_frame, width=5)
    entry_ngay.grid(row=0, column=1, pady=5)

    ttk.Label(add_frame, text="Tháng:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_thang = ttk.Entry(add_frame, width=5)
    entry_thang.grid(row=0, column=3, pady=5)

    ttk.Label(add_frame, text="Năm:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    entry_nam = ttk.Entry(add_frame, width=7)
    entry_nam.grid(row=0, column=5, pady=5)

    ttk.Label(add_frame, text="Giá bán (VND/kg):").grid(row=1, column=0, columnspan=2, sticky="e", pady=5)
    entry_gia_moi = ttk.Entry(add_frame, width=20)
    entry_gia_moi.grid(row=1, column=2, columnspan=4, pady=5)

    ttk.Button(new_window, text="LƯU GIÁ BÁN", command=save_new_price).pack(pady=10, ipadx=10)

app = tk.Tk()
app.title("Tính toán lợi nhuận nông nghiệp")
app.geometry("900x650")
app.configure(bg="#A8E6CF")

class EffectCanvas(tk.Canvas):
    """
    Lớp kế thừa từ `tk.Canvas` với hàm `lift()` được tùy chỉnh.

    Nếu không có đối tượng chỉ định, canvas sẽ được đưa lên trên cùng.
    Nếu có, gọi hàm `lift()` chuẩn để nâng canvas lên trên widget được chỉ định.
    """
    def lift(self, aboveThis=None):
        """
        Điều khiển thứ tự hiển thị của widget canvas.

        Nếu không truyền đối số, canvas sẽ được đưa lên trên tất cả các widget khác bằng cách gọi trực tiếp lệnh `raise` của Tk.
        Nếu truyền `aboveThis`, sẽ sử dụng lại hàm `lift` của lớp cha (`tk.Canvas`) để đưa canvas lên trên widget được chỉ định.

        Args:
            aboveThis (widget, optional): Widget mà canvas sẽ được đưa lên phía trên. Mặc định là None.

        Returns:
            None
        """
        if aboveThis is None:
            self.tk.call('raise', self._w)
        else:
            super().lift(aboveThis)

canvas = EffectCanvas(app, width=900, height=650, bg="#A8E6CF", highlightthickness=0)
canvas.place(x=0, y=0)
canvas.lift()

try:
    bean_img = tk.PhotoImage(file="hat_cafe.png").subsample(20)
except Exception:
    bean_img = None

beans = []

def create_bean():
    """
    Tạo một hạt cà phê mới và thêm vào canvas với vị trí và hướng rơi ngẫu nhiên.
    
    Hàm này sẽ:
    - Chọn ngẫu nhiên một vị trí theo trục X trong khoảng từ 100 đến 800.
    - Chọn ngẫu nhiên một hướng di chuyển ngang `dx` (-2, -1, 1 hoặc 2) để tạo hiệu ứng rơi chéo.
    - Thêm hình ảnh hạt cà phê vào canvas tại vị trí (x, 0).
    - Lưu ID của hình ảnh cùng với hướng di chuyển.

    Args:
        None

    Returns:
        None
    """
    if bean_img:
        x = random.randint(100, 800)
        dx = random.choice([-2, -1, 1, 2])  
        bean = canvas.create_image(x, 0, image=bean_img)
        beans.append((bean, dx))

def move_beans():
    """
    Di chuyển các hạt cà phê đã tạo trên canvas theo hướng rơi chéo, đồng thời tạo hiệu ứng rơi liên tục.

    Cụ thể:
    - Duyệt qua từng hạt cà phê trong danh sách `beans`, di chuyển chúng theo hướng `dx` (trái/phải) và xuống dưới theo trục Y.
    - Nếu một hạt rơi xuống quá giới hạn (tọa độ Y > 650), nó sẽ bị xóa khỏi canvas và danh sách.
    - Với xác suất 50%, hàm sẽ tạo thêm một hạt cà phê mới bằng cách gọi `create_bean()`.
    - Hàm tự gọi lại sau mỗi 30ms để tạo hiệu ứng chuyển động liên tục.

    Args:
        None

    Returns:
        None
    """
    for bean, dx in beans[:]:
        canvas.move(bean, dx, 9)
        x, y = canvas.coords(bean)
        if y > 650:
            canvas.delete(bean)
            beans.remove((bean, dx))
    if random.random() < 0.5:
        create_bean()
    app.after(30, move_beans)

move_beans()

main_frame = ttk.Frame(app)
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600)

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#A8E6CF", relief="flat", borderwidth=0)
style.configure("TLabel", background="#A8E6CF", font=("Comic Sans MS", 11))
style.configure("TButton", font=("Comic Sans MS", 12, "bold"), padding=10,
                background="#FF8B94", foreground="white")
style.map("TButton",
          background=[("active", "#FF6F80")],
          relief=[("pressed", "sunken"), ("!pressed", "raised")])

ttk.Label(main_frame,
          text="🌱 TÍNH LỢI NHUẬN NÔNG NGHIỆP 🌱",
          font=("Comic Sans MS", 20, "bold"),
          background="#A8E6CF",
          foreground="#555").pack(pady=(20, 15))

input_frame = ttk.Frame(main_frame)
input_frame.pack(padx=30, pady=10)

fields = [
    ("Chi phí đầu tư (VND):", "entry_chi_phi"),
    ("Sản lượng thu hoạch (kg):", "entry_san_luong"),
    ("Giá bán dự kiến (VND/kg):", "entry_gia_ban")
]

for i, (label_text, var_name) in enumerate(fields):
    ttk.Label(input_frame, text=label_text).grid(row=i, column=0, padx=5, pady=8, sticky="e")
    entry = ttk.Entry(input_frame, font=("Comic Sans MS", 11))
    entry.grid(row=i, column=1, padx=5, pady=8, ipady=4)
    globals()[var_name] = entry

ttk.Button(main_frame, text="TÍNH LỢI NHUẬN", command=tinh_loi_nhuan).pack(pady=(15, 10), ipadx=15)

label_ket_qua = ttk.Label(main_frame, text="Lợi nhuận: ", font=("Comic Sans MS", 12, "bold"))
label_ket_qua.pack(pady=(0, 15))

label_danh_gia = ttk.Label(main_frame, text="", font=("Comic Sans MS", 11))
label_danh_gia.pack(pady=(0, 15))

label_danh_gia_vu_mua = ttk.Label(main_frame, text="", font=("Comic Sans MS", 11))
label_danh_gia_vu_mua.pack(pady=(0, 15))

ttk.Button(main_frame, text="📊 BIỂU ĐỒ GIÁ CÀ PHÊ CÁC NĂM TRƯỚC", command=mo_cua_so_bieu_do).pack(pady=(5, 15))
ttk.Button(main_frame, text="📜 LỊCH SỬ GIÁ ĐÃ BÁN", command=xem_lich_su).pack(pady=(5, 15))
ttk.Button(main_frame, text="➕ THÊM GIÁ BÁN MỚI", command=them_gia_ban).pack(pady=(5, 15))

load_data_from_file()
app.mainloop()