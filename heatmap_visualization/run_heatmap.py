#!/usr/bin/env python3
"""
Organic Electrocatalysis Query-Chunk Similarity Heatmap Generator

This script generates a focused heatmap showing the similarity between 5 key organic electrocatalysis queries 
and the top 15 most relevant text chunks from the entire knowledge base.
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.visualization.heatmap import HeatmapVisualizer


def main():
    """Generate the focused heatmap"""
    print("🧪 Generating Organic Electrocatalysis Query-Chunk Similarity Heatmap")
    print("="*70)
    
    # Initialize visualizer
    visualizer = HeatmapVisualizer()
    
    # Create focused heatmap
    visualizer.create_similarity_heatmap(
        max_docs=15,         # Number of top chunks to display
        figsize=(12, 8),     # Image size
        cmap='viridis',      # Color mapping (optimized for 0.4-0.8 range)
        vmin=0.4,            # Minimum similarity threshold
        vmax=0.8,            # Maximum similarity threshold
        save_path='organic_electrocatalysis_heatmap.png'  # Save path
    )
    
    print("✅ Heatmap generation completed!")
    print("📁 Output saved as: organic_electrocatalysis_heatmap.png")


if __name__ == "__main__":
    main() 