# Smart-Face-Analytics

## Project Overview

The **Smart Face Analytics** system leverages transfer learning via the DeepFace framework to deliver real-time facial recognition and analysis. It integrates pre-trained models with custom functionality and collects high-quality data for potential future fine-tuning.

### Motivation  
I developed this project to test my understanding of transfer learning and to explore the capabilities of the DeepFace GitHub repository. My goal was to create a robust facial recognition system that not only identifies faces in real-time but also allows for the easy addition of new individuals with customizable data entry. The data is structured to be readily usable for further transfer learning, making it possible to improve upon the DeepFace program over time.

During testing, I observed that the system’s age prediction accuracy tends to falter for individuals under 25 or over 50. If a dataset were created specifically for these age groups and used to fine-tune the model, I believe significant improvements in accuracy could be achieved. Ultimately, this project is a foundational component for one of my upcoming projects.

![Main Interface](main_interface.png)

---

## How the System Works

When you launch **Smart Face Analytics**, the **main screen** appears with three options:  
- **Start Recognition System**  
- **Add Person**  
- **Exit**

### **1. Start Recognition System**
If you click **Start Recognition System**, the application opens a real-time video feed that scans for faces. The system then predicts the following attributes for any detected individual:
- **Age**
- **Gender (with confidence percentage)**
- **Ethnicity**
- **Emotional state**

If the detected individual is already registered in the system, their **stored data** is displayed alongside the real-time predictions.

![Real-Time Analysis](realtime_analysis.png)

---

### **2. Add Person**
If you click **Add Person**, you will be taken to the **registration screen**, where you can enter the following details:
- **Name**
- **Age**
- **Gender**
- **Ethnicity**

Once the information is entered, you have the option to **start the camera** and take a profile photo.

![Add Person Interface](add_person.png)

#### **Capturing a Photo**
When you press the **Start Camera** button, a live camera feed appears, allowing you to take a photo. You will see a button labeled **Capture Photo**.

![Capture Photo](capture_photo.png)

After capturing the photo, a confirmation screen appears stating **"Photo was successfully saved."**

![Successful Photo](successful_photo.png)

---

### **3. Returning to Recognition Mode**
After adding a person to the database, returning to **Start Recognition System** will now show their stored information alongside real-time predictions.

![Main Interface Updated](main_interface_2.png)

---

## Setup Instructions

For full installation and setup instructions, refer to [docs/setup.txt](docs/setup.txt).


