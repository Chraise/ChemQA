from src.visualization.heatmap import HeatmapVisualizer

def main():
    """
    Example: Generate organic electrocatalysis query-chunk similarity heatmap
    """
    print("Starting organic electrocatalysis query-chunk similarity heatmap generation...")
    
    # 初始化热力图可视化器
    visualizer = HeatmapVisualizer()
    
    # 生成热力图（使用默认的有机电催化查询）
    visualizer.create_similarity_heatmap(
        max_docs=15,  # 显示前15个最相关文档
        figsize=(12, 8),  # 设置图像大小
        cmap='viridis',  # 使用viridis颜色映射以提高区分度
        vmin=0.4,  # 最小相似度阈值，聚焦在0.4-0.8范围
        vmax=0.8,  # 最大相似度阈值
        save_path='organic_electrocatalysis_heatmap.png'  # 保存图像
    )
    
    print("Heatmap generation completed!")

if __name__ == "__main__":
    main() 