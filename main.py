from flask import Flask, request, jsonify, render_template
from package.use import llama3, judge_1, judge_2
import threading
import queue
import concurrent.futures

app = Flask(__name__)

@app.route('/index')
def index_html():
    return render_template('index.html')

def get_ai_response(question):
    """呼叫 Llama3 取得回答"""
    resLlama = llama3(question)

    if resLlama.message and hasattr(resLlama.message, 'content'):
        return resLlama.message.content
    return None

def get_judges_results(answer, question):
    """並行執行兩個評審模型，確保兩者都執行完成後回傳"""
    
    def judge_1_thread():
        try:
            result = judge_1(answer, question)
            print("====================judge_1====================\n")
            print(result)
            print("====================judge_1====================\n")
            return 'judge_1', result.message.content if (result and result.message) else "無結果"
        except Exception as e:
            return 'judge_1', f"錯誤: {str(e)}"

    def judge_2_thread():
        try:
            result = judge_2(answer, question)
            print("====================judge_2====================\n")
            print(result)
            print("====================judge_2====================\n")
            return 'judge_2', result.message.content if (result and result.message) else "無結果"
        except Exception as e:
            return 'judge_2', f"錯誤: {str(e)}"

    # 使用 ThreadPoolExecutor 來管理執行緒
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_judge = {
            executor.submit(judge_1_thread): 'judge_1',
            executor.submit(judge_2_thread): 'judge_2'
        }
        for future in concurrent.futures.as_completed(future_to_judge):
            result = future.result()
            if result is None:
                continue  # 避免 unpack 錯誤
            judge_name, result = result
            results[judge_name] = result

    return results

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    print("=================分隔線====================")
    print(f"問題：{question}")
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
