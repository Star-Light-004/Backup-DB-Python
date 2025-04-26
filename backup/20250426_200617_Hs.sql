-- 1. Tạo cơ sở dữ liệu
CREATE DATABASE QuanLyHocSinh;
GO

-- Sử dụng cơ sở dữ liệu vừa tạo
USE QuanLyHocSinh;
GO

-- 2. Tạo bảng Trường
CREATE TABLE Truong (
    MaTruong INT PRIMARY KEY IDENTITY(1,1),
    TenTruong NVARCHAR(100) NOT NULL
);

-- 3. Tạo bảng Lớp
CREATE TABLE Lop (
    MaLop INT PRIMARY KEY IDENTITY(1,1),
    TenLop NVARCHAR(50) NOT NULL,
    MaTruong INT NOT NULL,
    FOREIGN KEY (MaTruong) REFERENCES Truong(MaTruong)
);

-- 4. Tạo bảng Học sinh
CREATE TABLE HocSinh (
    MaHocSinh INT PRIMARY KEY IDENTITY(1,1),
    HoTen NVARCHAR(100) NOT NULL,
    MaLop INT NOT NULL,
    FOREIGN KEY (MaLop) REFERENCES Lop(MaLop)
);

-- 5. Chèn dữ liệu vào bảng Trường
INSERT INTO Truong (TenTruong) VALUES 
(N'Trường THPT Lê Quý Đôn'),
(N'Trường THCS Nguyễn Huệ');

-- 6. Chèn dữ liệu vào bảng Lớp
INSERT INTO Lop (TenLop, MaTruong) VALUES 
(N'12A1', 1),
(N'12A2', 1),
(N'9B', 2);

-- 7. Chèn dữ liệu vào bảng Học sinh
INSERT INTO HocSinh (HoTen, MaLop) VALUES 
(N'Nguyễn Văn A', 1),
(N'Lê Thị B', 2),
(N'Trần Văn C', 3);

-- 8. Truy vấn kết quả để kiểm tra
SELECT 
    hs.MaHocSinh, hs.HoTen, 
    l.TenLop, 
    t.TenTruong
FROM HocSinh hs
JOIN Lop l ON hs.MaLop = l.MaLop
JOIN Truong t ON l.MaTruong = t.MaTruong;





