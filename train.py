#-*- coding:utf-8 -*


from util import *
from computational_graph_lstm import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def train():

    x = tf.placeholder("float",[None,time_steps,n_input], name = "x") #输入图像占位符
    y = tf.placeholder("float",[None,captcha_num,n_classes], name = "y")  #输入标签占位符

    opt, loss, accuracy, pre_arg, y_arg = computational_graph_lstm(x, y)

    saver = tf.train.Saver()  # 创建训练模型保存类
    init = tf.global_variables_initializer()    #初始化变量值

    with tf.Session() as sess:  # 创建tensorflow session
        sess.run(init)
        iter = 1
        while iter < iteration:
            batch_x, batch_y = get_batch()
            sess.run(opt, feed_dict={x: batch_x, y: batch_y})   #只运行优化迭代计算图
            if iter %100==0:
                los, acc, parg, yarg = sess.run([loss, accuracy, pre_arg, y_arg],feed_dict={x:batch_x,y:batch_y})
                print("For iter ",iter)
                print("Accuracy ",acc)
                print("Loss ",los)
                if iter % 1000 ==0:
                    print("predict arg:",parg[0:10])
                    print("yarg :",yarg[0:10])
                print("__________________")
            if iter % 1000 == 0:   #保存模型
                saver.save(sess, model_path, global_step=iter)
            iter += 1
        # 计算验证集准确率
        valid_x, valid_y = get_batch(data_path=validation_path, is_training=False)
        print("Validation Accuracy:", sess.run(accuracy, feed_dict={x: valid_x, y: valid_y}))

        
if __name__ == '__main__':
    train()

