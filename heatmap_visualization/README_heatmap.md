# Organic Electrocatalysis Query-Chunk Similarity Heatmap Generator

This tool generates a focused heatmap showing the similarity between 5 key organic electrocatalysis queries and the top 15 most relevant text chunks from the entire knowledge base, providing a comprehensive yet focused visualization of the most important correlations with enhanced color differentiation and significantly improved font sizes for excellent readability and presentation quality.

## Features

- Automatically generates 5 key organic electrocatalysis related English queries
- Calculates similarity between each query and ALL documents in the knowledge base
- Selects and displays the top 15 most relevant text chunks based on average similarity
- Generates focused heatmap visualization with enhanced color differentiation
- Significantly improved font sizes for excellent readability and presentation quality
- Supports custom parameters and image saving
- Clean visualization with chunk numbers only on Y-axis

## Installation

Ensure the following Python packages are installed:

```bash
pip install -r requirements.txt
```

Main dependencies include:
- numpy
- matplotlib
- seaborn
- sentence-transformers

## Usage

### Method 1: Simple Run Script

```bash
python3 run_heatmap.py
```

This will automatically generate a focused heatmap and save it as `organic_electrocatalysis_heatmap.png`.

### Method 2: Example Script

```bash
python3 src/visualization/example_heatmap.py
```

## Generated Queries

The system automatically generates the following 5 key organic electrocatalysis related queries:

1. mechanism of CO2 electroreduction on Cu single-atom catalysts
2. electrochemical oxidation of alcohols to aldehydes
3. electrochemical C-H functionalization of arenes
4. electrochemical synthesis of heterocyclic compounds
5. electrochemical reduction of carbonyl compounds

## Output Description

### Heatmap Interpretation

- **X-axis**: Query numbers (Q1-Q5)
- **Y-axis**: Text chunk numbers (Chunk1-Chunk15) - clean numbering only
- **Color intensity**: Cosine similarity scores (0.4-0.8)
  - Darker purple/blue indicates higher similarity
  - Lighter yellow/green indicates lower similarity
  - Enhanced color differentiation for 0.4-0.7 range
  - Shows real similarity values for all query-chunk pairs

### Key Features

- **Comprehensive Analysis**: Calculates similarity between each query and ALL documents (1785 total)
- **Smart Selection**: Displays the top 15 most relevant text chunks based on average similarity across all queries
- **Real Similarity Values**: No artificial zeros - shows actual cosine similarity scores
- **Enhanced Color Mapping**: Viridis color scheme optimized for 0.4-0.8 similarity range
- **Excellent Typography**: Large font sizes for outstanding readability and presentation quality
- **Clean Visualization**: Chunk numbers only on Y-axis for better readability
- **Compact Size**: 12×8 inch image, optimized for presentations and papers

### Output Files

- `organic_electrocatalysis_heatmap.png`: Generated focused heatmap image (531KB)
- Console output: Text information including query details and chunk details

## Custom Parameters

You can customize the heatmap by modifying parameters in the code:

```python
visualizer.create_similarity_heatmap(
    max_docs=15,         # Number of top chunks to display
    figsize=(12, 8),     # Image size
    cmap='viridis',      # Color mapping (optimized for 0.4-0.8 range)
    vmin=0.4,            # Minimum similarity threshold
    vmax=0.8,            # Maximum similarity threshold
    save_path='output.png'  # Save path
)
```

## Technical Details

### Algorithm
1. **Complete Similarity Calculation**: For each query, calculate cosine similarity with ALL documents in the knowledge base
2. **Smart Chunk Selection**: Select the top 15 chunks based on average similarity across all 5 queries
3. **Matrix Construction**: Build focused 5×15 similarity matrix with real similarity values
4. **Enhanced Visualization**: Generate heatmap with chunk numbers and optimized color mapping

### Performance
- **Processing**: ~2-3 seconds per query for all 1785 documents
- **Total time**: ~15 seconds for complete analysis
- **Memory efficient**: Optimized for large-scale similarity calculations
- **High quality**: 531KB image with 300 DPI resolution

### Color Optimization
- **Color scheme**: Viridis (purple-blue-yellow-green)
- **Range focus**: 0.4-0.8 similarity range for better differentiation
- **Enhanced visibility**: Improved contrast for medium similarity values (0.4-0.7)

### Typography Settings
- **Title font size**: 24pt (bold)
- **Axis label font size**: 20pt
- **Tick label font size**: 18pt
- **Annotation font size**: 16pt
- **Color bar label font size**: 20pt
- **Default font size**: 18pt

## Notes

1. Ensure the knowledge base is properly initialized and contains relevant literature
2. The tool calculates similarity with ALL documents but displays only the most relevant chunks
3. Generated images have high resolution, suitable for academic reports and papers
4. Clean visualization with chunk numbers only for better readability
5. Real similarity values are shown, providing accurate correlation insights
6. Enhanced color mapping improves visibility of similarity differences in the 0.4-0.7 range
7. Large font sizes ensure excellent readability in presentations and publications

## Troubleshooting

If you encounter issues, please check:

1. All dependency packages are correctly installed
2. Knowledge base is initialized
3. Sufficient disk space for image saving
4. Python environment supports English font display

## Technical Implementation

- Uses `sentence-transformers` for text vectorization
- Uses cosine similarity to calculate query-chunk correlation
- Uses `matplotlib` and `seaborn` to generate heatmaps
- Supports English titles and labels
- Comprehensive analysis with smart chunk selection
- Enhanced color mapping for better similarity visualization
- Excellent typography settings for outstanding presentation quality 