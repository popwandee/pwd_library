# graph_utils.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_line(x, y, title='Line Graph', xlabel='X-axis', ylabel='Y-axis'):
    """
    สร้างกราฟเส้น (Line Graph)
    
    Parameters:
        x (list or array): ข้อมูลแกน X
        y (list or array): ข้อมูลแกน Y
        title (str): หัวข้อกราฟ
        xlabel (str): ชื่อแกน X
        ylabel (str): ชื่อแกน Y
    """
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_bar(categories, values, title='Bar Chart', xlabel='Categories', ylabel='Values'):
    """
    สร้างกราฟแท่ง (Bar Chart)
    
    Parameters:
        categories (list): หมวดหมู่บนแกน X
        values (list): ค่าแต่ละหมวดหมู่
        title (str): หัวข้อกราฟ
        xlabel (str): ชื่อแกน X
        ylabel (str): ชื่อแกน Y
    """
    plt.figure()
    plt.bar(categories, values, color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

def plot_pie(labels, sizes, title='Pie Chart'):
    """
    สร้างกราฟวงกลม (Pie Chart)
    
    Parameters:
        labels (list): ป้ายชื่อแต่ละชิ้นส่วน
        sizes (list): ขนาดของแต่ละชิ้นส่วน
        title (str): หัวข้อกราฟ
    """
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def plot_hist(data, bins=10, title='Histogram', xlabel='Value', ylabel='Frequency'):
    """
    สร้างฮิสโตแกรมแสดงการกระจายของข้อมูล
    
    Parameters:
        data (list or array): ข้อมูลที่ต้องการวิเคราะห์
        bins (int): จำนวนช่องข้อมูล
        title (str): หัวข้อกราฟ
        xlabel (str): ชื่อแกน X
        ylabel (str): ชื่อแกน Y
    """
    plt.figure()
    plt.hist(data, bins=bins, color='orange', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

def plot_heatmap(data, title='Heatmap', xlabel='X', ylabel='Y'):
    """
    สร้าง heatmap สำหรับแสดงค่าหรือความสัมพันธ์ในรูปแบบ matrix
    
    Parameters:
        data (2D array or list of lists): ข้อมูลในรูปแบบเมทริกซ์
        title (str): หัวข้อกราฟ
        xlabel (str): ชื่อแกน X
        ylabel (str): ชื่อแกน Y
    """
    plt.figure()
    sns.heatmap(data, annot=True, fmt='.1f', cmap='coolwarm')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

def plot_scatter(x, y, title='Scatter Plot', xlabel='X-axis', ylabel='Y-axis'):
    """
    สร้าง scatter plot สำหรับแสดงความสัมพันธ์ระหว่างข้อมูลสองชุด
    
    Parameters:
        x (list or array): ข้อมูลแกน X
        y (list or array): ข้อมูลแกน Y
        title (str): หัวข้อกราฟ
        xlabel (str): ชื่อแกน X
        ylabel (str): ชื่อแกน Y
    """
    plt.figure()
    plt.scatter(x, y, c='green', alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
