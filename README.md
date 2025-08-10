# 🚨 Finding Missing Person Using AI

> **An AI-powered platform to assist authorities & the public in quickly locating missing individuals.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-orange)
![Database](https://img.shields.io/badge/Database-SQLite-green)
![MediaPipe](https://img.shields.io/badge/Face%20Recognition-MediaPipe-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🧠 **Objective**

Every day in India, hundreds of people — especially children — go missing.
While police and NGOs are actively involved in recovery efforts, **traditional investigation** often takes too long, especially when the person has been moved to another city or country.

Our project leverages **AI-powered facial recognition** to **scan, match, and track missing individuals faster** by:

* Analysing CCTV footage & public submissions
* Reducing manual effort via automated face matching
* Enabling real-time collaboration between police, NGOs, and citizens

---

## 🖼 Screenshots

| Dashboard                     | Case registration             | Public Submission             | Case Matching |
| ----------------------------- | ----------------------------- | ----------------------------- | -------------- |
| ![Desc1](https://github.com/codecortex25/Finding-Missing-Person-Using-AI-IBM-Internship/blob/main/Snapshots/Screenshot%202025-08-05%20150355.png) | ![Desc2](https://github.com/codecortex25/Finding-Missing-Person-Using-AI-IBM-Internship/blob/main/Snapshots/Screenshot%202025-08-05%20150724.png) | ![Desc3](https://github.com/codecortex25/Finding-Missing-Person-Using-AI-IBM-Internship/blob/main/Snapshots/Screenshot%202025-08-05%20150850.png) | ![Desc3](https://github.com/codecortex25/Finding-Missing-Person-Using-AI-IBM-Internship/blob/main/Snapshots/Screenshot%202025-08-05%20150932.png)
|   Admin Dashboard             | Register New case by Admin                 | Public Submission            | Match Case with Public Submission and Admin Registered case                    |

---

## ⚙️ **Key Features**

* **Seamless Registration**: Upload missing person details & image, auto-extract face mesh.
* **AI-Powered Matching**: Match new submissions with existing records using MediaPipe Face Mesh.
* **Multi-User Dashboards**: Separate views for Admin, Police, and Public.
* **Public Participation**: Citizens can submit sightings via web/mobile.
* **Lightweight & Portable**: SQLite-based storage, ready to run without complex setup.

---

## 🚀 **How to Run**

```bash
# Clone repository
git clone https://github.com/yourusername/Finding-missing-person-using-AI.git
cd Finding-missing-person-using-AI

# Install dependencies
pip install -r requirements.txt

# Run main web app
streamlit run Home.py

# (Optional) Run public/mobile submission app
streamlit run mobile_app.py
```

📌 **Note**:

* Database (`sqlite_database.db`) auto-creates on first run.
* Images are stored in `resources/` folder.

---

## 📌 **Use Cases**

* Police & NGOs scanning CCTV images for matches.
* Crowdsourced submissions from citizens.
* Automated prioritization of leads.

---

## 🎓 **IBM SkillsBuild Internship Context**

This project was developed as part of the **IBM SkillsBuild “From Learner to Builder: Become an AI Agent Architect” 1-month internship**.

* **Team Name**: Code Cortex
* **Team Size**: 7 members
* **Nishtha Thakore**: Team Leader
* **Outcome**: Designed and implemented AI-powered missing person identification system with working demo, Lean Canvas, and presentation.

---

## 📄 **Resources**

* [Lean Canvas]([docs/lean_canvas.pdf](https://github.com/codecortex25/Finding-Missing-Person-Using-AI-IBM-Internship/blob/main/Lean-Canvas/Code-cortex-Team_lean-canvas.pdf))
* [Project Presentation]([docs/presentation.pdf](https://github.com/codecortex25/Finding-Missing-Person-Using-AI-IBM-Internship/blob/main/Presentation%20Document/Code-Cortex-Finding-Missing-Persons-Using-AI%20%5BAutosaved%5D_choladeck.pptx))

---

## 👥 **Team Contributions**

| Role            | Name      | Contribution                                                           |
| --------------- | --------- | ---------------------------------------------------------------------- |
| **Team Leader** | Nishtha Thakore | Led the team, developed core AI model, integrated Streamlit & database |
| Member          | Drashti Sojitra    | Designed UI components & dashboards                                    |
| Member          | Monalisa Padhy    | Developed public submission portal                                     |
| Member          | Yashvi Malani    | Handled database schema & backend                                      |
| Member          | Dhruvil Nakrani    | Created PPT & documentation                                            |
| Member          | Dhruv Chovatiya    | Tested model & optimized performance                                   |
| Member          | Jeel Virani    | Collected datasets & performed preprocessing                           |

---

## 🙏 **Acknowledgements**

* **MediaPipe** team for open-source Face Mesh.
* **IBM SkillsBuild** for internship guidance & mentorship.
* Everyone who contributed to data collection & testing.

---

## 📬 **Suggestions, Contributions & Contact**

💡 If you have suggestions, want to contribute, or collaborate on enhancing this solution — we’d love to hear from you!
📧 **Email us at:** `codecortexibm25@gmail.com`

