# Image to Text Extractor(Bill to Data)

This project processes images of food bills and extracts structured information such as item details, quantities, unit prices, and totals. The extracted data is output in JSON format. It is powered by state-of-the-art AI models and frameworks, making it robust, fast, and OCR-free.

---

## 🚀 Features
- **OCR-Free Document Understanding**: Uses a vision-language model to process images directly.
- **Structured Output**: Extracts and outputs information in JSON format for easy integration.
- **Multilingual Support**: Capable of handling diverse languages in receipts.
- **Fast and Accurate**: Optimized for high-speed and precise information extraction.

---

## 🛠️ Tech Stack
### Programming Language:
- **Python**: Core language for scripting and processing.

### Frameworks and Libraries:
- **PyTorch**: For loading and running deep learning models.
- **Transformers**: For model handling and tokenization.
- **Pillow (PIL)**: For image processing.
- **Regular Expressions (re)**: For cleaning and structuring text data.

### Model:
- **Donut (Document Understanding Transformer)**:
  - **Base Model**: `donut-base`
  - **Fine-Tuned Version**: `naver-clova-ix/donut-base-finetuned-cord-v2`
  - **Specialization**: Extracts structured data from receipts (fine-tuned on the CORD dataset).

---

## 🧠 Algorithms and Techniques
1. **Vision-Transformer (ViT)**:
   - Processes input images to generate feature embeddings.

2. **Transformer Decoder**:
   - Converts the visual features into text sequences for structured output.

3. **Beam Search Decoding**:
   - Used during the generation phase for producing high-quality structured text.

4. **Regex-Based Text Cleaning**:
   - Cleans and processes raw text to remove unwanted characters and standardize the format.

---

## 🖼️ Example Input and Output
### Input:
A food bill image (e.g., `food-bill.jpg`).

### Output (JSON):
```json
{
  "menu": [
    {"nm": "Water Bottle", "unitprice": "170.00", "cnt": "2", "price": "170.00"},
    {"nm": "Crispy Chilli", "unitprice": "250.00", "cnt": "4", "price": "250.00"},
    {"nm": "Chicken", "unitprice": "840.00", "cnt": "6", "price": "250.00"}
  ],
  "total": {
    "total_price": "840.00",
    "menuqty_cnt": "6"
  }
}
