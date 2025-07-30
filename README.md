# 🌿 FarmAssist – Your Go-To Buddy for Farm Matters in Nigeria

**FarmAssist** is your smart, friendly farming assistant built to help smallholder farmers across Nigeria get the best from their crops! Powered by Google’s Gemini AI and running on a simple Streamlit app, it’s like having an agritech expert in your pocket. It supports major Nigerian Languages and current weather data. 

Chat with it like WhatsApp for instant advice, or snap a picture of a leaf for quick disease checks. No fancy apps or heavy internet needed. Made for real farmers in real fields, whether you're in Lagos or a remote village in Bauchi, FarmAssist gives practical, local-knowledge-backed tips to boost your harvests.

Simple. Smart. Made for you. 🌱

## 🚜 What Can FarmAssist Do?

- 🌱 **Farming Tips** – From soil prep to harvest
- 🌍 **Local language support (Yoruba, Hausa, Igbo)**
- 🌤 **Weather data APIs**
- 🌾 **Seasonal Crop Recommendations**
- 🐛 **Pest & Disease Prediction from image uploads**
- 💧 **Irrigation Guidance**
- 🧠 **Remembers Chat History for Context**
- 🇳🇬 **Only Supports Farmers in Nigeria**

## 🛠️ Tech Stack

| Tool / Framework        | Purpose                          |
|------------------------|----------------------------------|
| Streamlit              | UI and chat interface            |
| TensorFlow             | Crop disease image classifier    |
| Google Gemini API      | LLM-powered farming assistant    |
| Pillow, NumPy          | Image processing & array ops     |
| dotenv                 | API key management               |


## 📁 Project Structure

```
FarmAssist/
│
├── app.py                       
├── requirements.txt            
├── .gitignore                  
├── README.md                   
│
├── models/                    
│   ├── crop_disease_model.h5
│   └── mobilenetv2_best_model.h5
│
├── notebooks/                 
│
├── Test Images/                 
│
├── src/                        
│   ├── config.py                
│   ├── gemini_client.py         
│   ├── prompts.py               
│   ├── tools.py                 
│   │
│   ├── utils/                   
│   │   └── farm_tools.py       
│   │
│   └── styles/                  
│       └── SL_chat_theme_Olusola.py
│
├── .env                         
           
```

## ✅ Use Cases
FarmAssist solves real problems Nigerian farmers face daily. Here are a few scenarios:
| **Use Case**                                              | **How FarmAssist Helps**                                                                  |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 👨🏿‍🌾 *A farmer in Benue notices leaf spots on cassava* | Uploads image → Gets disease name → Gemini explains symptoms, spread, and treatments.     |
| 🌽 *Choosing what to plant this rainy season*             | Asks chatbot: *"What crop is best for July in Ogun?"* → Gets location-based suggestions.  |
| 🌾 *New to farming and doesn’t know where to start*       | Asks: *"How do I prepare my soil for maize?"* → Receives step-by-step tips.               |
| 🌤 *Checking rain forecast before planting*               | FarmAssist pulls current weather data for user’s location.                                |
| 🐛 *Detecting pests on crops*                                | Uploads image of pest → Receives identification and natural or chemical treatment advice. |


## 📂 Dataset

⚠️ The dataset used for this project is not included in this repository due to its size.

You can download it here:

📥 [Crop Pest and Disease Classification Dataset on Kaggle](https://www.kaggle.com/datasets/olusolaowoso/crop-pest-and-disease-detection-dataset) 

## 🧪 Model: Crop Disease Classifier

We use a fine-tuned MobileNetV2 model trained on crop disease image datasets (Cashew, Maize, Cassava, Tomato) with categories:

- **Healthy**
- **Disease 1**
- **Disease 2** ...

**Image preprocessing:** Resize to `(224, 224)`, normalized (1/255), augmented (rotation, zoom, flip).

**Training Code Includes:**
- `ImageDataGenerator`
- `ModelCheckpoint`, `EarlyStopping`
- Fine-tuning (unfreeze last 20 layers)
- Accuracy/loss plotting
- Classification report

## 💻 Local Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Sholz22/FarmAssist..git
cd FarmAssist
````

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On macOS/Linux
venv\Scripts\activate        # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_real_gemini_api_key_here
```

### 5. Run the App

```bash
streamlit run app.py
```


## 🌐 Deployment

Deployed with Streamlit Cloud

* ✅ [**Streamlit Cloud**](https://streamlit.io/cloud)


## 🧭 App Interface Workflow

Here's how users interact with the platform:

1. ### 🔓 **Launch the App**

   * Visit deployed Streamlit URL on a browser.

2. ### 🗣 **Start a Conversation**

   * Text-based chat interface appears.
   * User can ask farming-related questions.
   * FastAssist responds conversationally.

3. ### 📷 **Upload an Image**

   * Click **“Upload Crop Image”**.
   * Upload a diseased crop image (Limited to cassava, cashew, maize, and tomato for now).
   * The trained model processes it and predicts the disease name.

4. ### 🧠 **AI Explains Diagnosis**

   * The disease name is sent to Gemini with a prompt to explain in farmer-friendly terms.
   * Gemini returns an easy-to-understand explanation with advice, and user can request for response in their local languages.

5. ### 🌤 **Weather Insights (Optional)**

   * Automatically fetches weather data based on location or lets user request:
     *“What is the weather in my region?”*

6. ### 🧩 **Continuous Chat**

   * FarmAssist remembers context in the current session.
   * User can ask follow-ups like:
     *“Can this disease affect other crops?”*

7. ### 📤 **Get Recommendations**

   * Ask questions like:
     *“What should I plant next month in Plateau?”*

     * FarmAssist gives seasonal guidance using local context.


## Landing Page
<img width="574" height="399" alt="image" src="https://github.com/user-attachments/assets/8082b99c-e117-4c04-bd46-e8b22cd37980" />

## Image upload interface
<img width="525" height="461" alt="image" src="https://github.com/user-attachments/assets/5fc4e5a9-4332-434c-b2ce-749ee9e769ef" />

## Sample prediction output
<img width="516" height="410" alt="image" src="https://github.com/user-attachments/assets/4ba3cf02-49b8-4f1c-8364-60ba45b29a78" />


## ✨ Future Enhancements

* 🎙 Voice input/output
* 💻 Train the prediction model on more crops and diseases
* 🌤 Market data APIs
* 🧑‍🌾 Personal dashboard for farmers


## 🙋 About the Developer

Made with ❤️ for Nigerian farmers by [**Sholz22**](https://github.com/Sholz22)

> *"Farming shouldn't feel like guesswork — let's make it smarter, simpler, and more Naija."* 🇳🇬


## 📄 License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

