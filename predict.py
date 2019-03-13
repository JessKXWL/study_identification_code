# -*- coding:utf-8 -*

from computational_graph_lstm import *
from util import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def get_test_set():
    target_file_list = os.listdir(test_data_path)  # 获取测试集路径下的所有文件
    print("预测的验证码文件:", len(target_file_list))

    # 判断条件
    flag = len(target_file_list) // batch_size  # 计算待检测验证码个数能被batch size 整除的次数
    batch_len = flag if flag > 0 else 1  # 共有多少个batch
    flag2 = len(target_file_list) % batch_size  # 计算验证码被batch size整除后的取余
    batch_len = batch_len if flag2 == 0 else batch_len + 1  # 若不能整除，则batch数量加1

    print("共生成batch数:", batch_len)
    print("验证码根据batch取余:", flag2)

    batch = np.zeros([batch_len * batch_size, time_steps, n_input])
    for i in range(len(target_file_list)):
        batch[i] = open_image(target_file_list[i])
    batch = batch.reshape([batch_len, batch_size, time_steps, n_input])
    return batch, target_file_list  # batch_file_name


def open_image(file):
    img = Image.open(test_data_path + '/' + file)  # 打开图片
    img = np.array(img)
    if len(img.shape) > 2:
        img = np.mean(img, -1)  # 转换成灰度图像:(26,80,3) =>(26,80)
        img = img / 255
    return img


def predict():
    global errors
    errors = 0
    with tf.Session() as sess:
        print(path)
        saver = tf.train.import_meta_graph(path + "\model\\" + "model.ckpt-5000.meta")
        saver.restore(sess, tf.train.latest_checkpoint(path + "\model\\"))  # 读取已训练模型

        graph = tf.get_default_graph()  # 获取原始计算图，并读取其中的tensor
        x = graph.get_tensor_by_name("x:0")
        y = graph.get_tensor_by_name("y:0")
        pre_arg = graph.get_tensor_by_name("predict:0")
        test_x, file_list = get_test_set()  # 获取测试集
        predict_result = []
        for i in range(0,len(test_x)):
            batch_test_x = test_x[i]
            batch_test_y = np.zeros([batch_size, captcha_num, n_classes])  # 创建空的y输入
            test_predict = sess.run([pre_arg], feed_dict={x: batch_test_x, y: batch_test_y})
            print("测试数据特征向量: ", test_predict)
            for line in test_predict[i-1]: # 将预测结果转换为字符
                character = ""
                for each in line:
                    character += index2char(each)
                predict_result.append(character)

        predict_result = predict_result[:len(file_list)]  # 预测结果
        write_to_file(predict_result, file_list)  # 保存到文件
        calculate_correct_rate(predict_result, file_list)


def write_to_file(predict_list, file_list):
    with open(output_path, 'w+') as f:
        for i, res in enumerate(predict_list):
            if i == 0:
                f.write("id\tfile\tresult\n")
            f.write(str(i) + "\t" + file_list[i] + "\t" + res + "\n")
    print("预测结果保存在：", output_path)


def calculate_correct_rate(predict_result, file_list):
    global errors
    errors = 0
    for i, res in enumerate(predict_result):
        true_value = str(file_list[i]).split('.')[0]
        print("预测结果: %s 实际结果: %s " % (res, true_value))
        if true_value != res:
            errors = errors + 1
    correct_rate = (1 - errors / len(file_list)) * 100
    print("错误个数: %d \t 测试个数: %d " % (errors, len(file_list)))
    print("预测正确率:%f %%" % correct_rate)


if __name__ == '__main__':
    predict()
