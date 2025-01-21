from flask import Flask, request, jsonify, render_template
from package.use import llama3, judge_1, judge_2
import threading
import queue

app = Flask(__name__)

@app.route('/')
def login_html():
    return render_template('index.html')

def get_ai_response(question):
    """呼叫 Llama3 取得回答"""
    resLlama = llama3(question)

    if resLlama.message and hasattr(resLlama.message, 'content'):
        return resLlama.message.content
    return None

def get_judges_results(answer, question):
    """並行執行兩個評審模型"""
    results_queue = queue.Queue()

    def judge_1_thread():
        result = judge_1(answer, question)
        results_queue.put(('judge_1', result.message.content if result.message else "無結果"))

    def judge_2_thread():
        result = judge_2(answer, question)
        results_queue.put(('judge_2', result.message.content if result.message else "無結果"))

    # 啟動執行緒
    t1 = threading.Thread(target=judge_1_thread)
    t2 = threading.Thread(target=judge_2_thread)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # 收集結果
    results = {}
    while not results_queue.empty():
        model, result = results_queue.get()
        results[model] = result

    return results

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "問題不能為空"}), 400

    # AI 生成回答
    answer = get_ai_response(question)

    if not answer:
        return jsonify({"error": "AI 無法生成有效回答"}), 500

    # 取得評審結果
    judges_results = get_judges_results(answer, question)

    return jsonify({
        "question": question,
        "answer": answer,
        "judges": judges_results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
