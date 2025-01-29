from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)
user_responses = []
# سوالات و تصاویر همراه با امتیازات
questions = [
    {
        "text": "I am a ...... person.",
        "images": ["static/item1_image1.jpg", "static/item1_image2.jpg", "static/item1_image3.jpg"],
        "descriptions": ["Low Extraversion", "Medium Extraversion", "High Extraversion"],
        "scores": [1, 2, 3]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item2_image1.jpg", "static/item2_image2.jpg", "static/item2_image3.jpg"],
        "descriptions": ["Low Critical/Quarrelsome", "Medium Critical/Quarrelsome", "High Critical/Quarrelsome"],
        "scores": [3, 2, 1]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item3_image1.jpg", "static/item3_image2.jpg", "static/item3_image3.jpg"],
        "descriptions": ["Low Organized", "Medium Organized", "Highly Organized"],
        "scores": [1, 2, 3]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item4_image1.jpg", "static/item4_image2.jpg", "static/item4_image3.jpg"],
        "descriptions": ["Low Anxious", "Medium Anxious", "Highly Anxious"],
        "scores": [3, 2, 1]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item5_image1.jpg", "static/item5_image2.jpg", "static/item5_image3.jpg"],
        "descriptions": ["Low Curious", "Medium Curious", "Highly Curious"],
        "scores": [1, 2, 3]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item6_image1.jpg", "static/item6_image2.jpg", "static/item6_image3.jpg"],
        "descriptions": ["Low Calm", "Medium Calm", "Highly Calm"],
        "scores": [3, 2, 1]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item7_image1.jpg", "static/item7_image2.jpg", "static/item7_image3.jpg"],
        "descriptions": ["Low Empathetic", "Medium Empathetic", "Highly Empathetic"],
        "scores": [1, 2, 3]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item8_image1.jpg", "static/item8_image2.jpg", "static/item8_image3.jpg"],
        "descriptions": ["Low Disorganized", "Medium Disorganized", "Highly Disorganized"],
        "scores": [3, 2, 1]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item9_image1.jpg", "static/item9_image2.jpg", "static/item9_image3.jpg"],
        "descriptions": ["Low Emotionally Stable", "Medium Emotionally Stable", "Highly Emotionally Stable"],
        "scores": [1, 2, 3]
    },
    {
        "text": "I am a ...... person.",
        "images": ["static/item10_image1.jpg", "static/item10_image2.jpg", "static/item10_image3.jpg"],
        "descriptions": ["Low Conventional", "Medium Conventional", "Highly Conventional"],
        "scores": [3, 2, 1]
    }
]


if not os.path.exists("user_data"):
    os.makedirs("user_data")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    global user_responses

    data = request.get_json()
    question_index = data.get('question')
    answer_index = data.get('answer') - 1  

    # ذخیره پاسخ کاربر
    selected_score = questions[question_index]['scores'][answer_index]
    selected_description = questions[question_index]['descriptions'][answer_index]

    user_responses.append({
        "question": question_index + 1,
        "answer": selected_description,
        "score": selected_score
    })

    # بررسی سوال بعدی
    next_index = question_index + 1
    if next_index < len(questions):
        return jsonify(nextQuestion=questions[next_index])
    else:
        # محاسبه نهایی امتیازات شخصیت
        final_scores = calculate_personality_traits(user_responses)

        # ذخیره داده‌های کاربر
        save_user_data(user_responses, final_scores)

        # ارسال نتایج نهایی به فرانت‌اند
        return jsonify(nextQuestion=None, finalScores=final_scores)



def calculate_personality_traits(user_data):
    """محاسبه ویژگی‌های شخصیتی بر اساس پاسخ‌ها"""
    
    scores_dict = {i+1: user_data[i]["score"] for i in range(len(user_data))}

    # محاسبه ویژگی‌های شخصیت (Big Five)
    extraversion = scores_dict[1] + scores_dict[6]  # Q1 + Q6
    agreeableness = scores_dict[7] + scores_dict[2]  # Q7 + Q2
    conscientiousness = scores_dict[3] + scores_dict[8]  # Q3 + Q8
    emotional_stability = scores_dict[9] + scores_dict[4]  # Q9 + Q4
    openness = scores_dict[5] + scores_dict[10]  # Q5 + Q10

    return {
        "Extraversion": extraversion,
        "Agreeableness": agreeableness,
        "Conscientiousness": conscientiousness,
        "Emotional-Stability": emotional_stability,
        "Openness": openness
    }


def save_user_data(user_data, final_scores):
    """ذخیره اطلاعات کاربر در یک فایل JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_data/user_{timestamp}.json"

    data_to_save = {
        "responses": user_data,
        "final_scores": final_scores
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    app.run(debug=True)
