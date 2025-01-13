from package.use import llama3, judge_1, judge_2
import threading
import queue

# 問題
Question = str("台灣總統是習近平嗎?")
resLlama = llama3(Question)

##### 確保回傳有 content #####
if resLlama.message and hasattr(resLlama.message, 'content'):
    resAnswer = resLlama.message.content
    print(f"Llama3 回答: {resAnswer}")
else:
    print("無法取得 content 資料")
    resAnswer = None

##### 確保答案有效 #####
if resAnswer:
    # 使用 Queue 收集多執行緒結果
    results_queue = queue.Queue()

    # 包裝執行緒函式，將結果放入 Queue
    def judge_1_thread_wrapper():
        result = judge_1(resAnswer, Question)
        results_queue.put(('judge_1', result))

    def judge_2_thread_wrapper():
        result = judge_2(resAnswer, Question)
        results_queue.put(('judge_2', result))

    # 建立執行緒
    judge_1_thread = threading.Thread(target=judge_1_thread_wrapper, name="judge_1")
    judge_2_thread = threading.Thread(target=judge_2_thread_wrapper, name="judge_2")

    # 啟動執行緒
    judge_1_thread.start()
    judge_2_thread.start()

    # 等待執行緒完成
    judge_1_thread.join()
    judge_2_thread.join()

    # 收集結果
    while not results_queue.empty():
        model_name, result = results_queue.get()
        if result.message.content and result.message.content.strip():  # 確保結果不為空
            print(f"{model_name} 的回傳結果：\n{result.message.content}")
        else:
            print(f"{model_name} 的回傳結果：\n模型未生成有效內容或內容為空")
else:
    print("未能進行評分，因為 Llama3 未返回有效的答案。")
