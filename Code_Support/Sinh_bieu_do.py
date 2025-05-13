import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

# Đọc dữ liệu từ file CSV
data = pd.read_csv('gia_ca.csv', header=None, names=["date_price"])

# Tách ngày và giá trị từ cột 'date_price'
data[['date', 'price']] = data['date_price'].str.split(':', expand=True)

# Loại bỏ khoảng trắng ở đầu và cuối của cột 'date' và 'price'
data['date'] = data['date'].str.strip()
data['price'] = data['price'].str.strip()

# Chuyển đổi cột 'date' thành datetime và cột 'price' thành float
data['date'] = pd.to_datetime(data['date'])
data['price'] = data['price'].astype(float)

# Vẽ biểu đồ cho từng năm từ 2015 đến 2024 và lưu dưới dạng ảnh
for year in range(2015, 2025):
    yearly_data = data[data['date'].dt.year == year]
    
    # Tạo biểu đồ với Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=yearly_data['date'], 
        y=yearly_data['price'], 
        mode='lines',
        name=f'Giá cà phê năm {year}'
    ))

    # Cập nhật các thông số của biểu đồ
    fig.update_layout(
        title=f'Giá cà phê năm {year}',
        xaxis_title='Ngày',
        yaxis_title='Giá (VND)',
        template='plotly_dark'
    )

    # Lưu biểu đồ dưới dạng ảnh .png
    fig.write_image(f"gia_ca_{year}.png")
    print(f"gia_ca_{year}.png")
