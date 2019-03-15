import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from TrainForm import Ui_TrainForm
from PyQt5 import QtCore
from util import *
from computational_graph_lstm import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class MyWindow(QWidget, Ui_TrainForm):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    @QtCore.pyqtSlot()
    def initUI(self):
        self.StartpushButton.setEnabled(False)
        self.ServerpushButton.setEnabled(False)
        self.step = 0

    @QtCore.pyqtSlot()
    def on_ChooseFilepushButton_clicked(self):
        directory = QFileDialog.getExistingDirectory(self, '选择文件夹','./')
        self.lineEdit.setText(directory)
        self.StartpushButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_StartpushButton_clicked(self):
        directory = self.lineEdit.text()
        if directory == "":
            QMessageBox.information(self, 'information', u'请选择需要训练的图片集')
            return
        self.timerEvent(directory)

    @QtCore.pyqtSlot()
    def timerEvent(self, directory):
        if self.step >= 100:
            self.timer.stop()
            self.textBrowser.append("训练完成")
            self.step = 0
        else:
            x = tf.placeholder("float", [None, time_steps, n_input], name="x")  # 输入图像占位符
            y = tf.placeholder("float", [None, captcha_num, n_classes], name="y")  # 输入标签占位符

            opt, loss, accuracy, pre_arg, y_arg = computational_graph_lstm(x, y)
            saver = tf.train.Saver()  # 创建训练模型保存类
            init = tf.global_variables_initializer()  # 初始化变量值
            with tf.Session() as sess:  # 创建tensorflow session
                sess.run(init)
                iter = 1
                step_tmp = 100/iteration
                while iter < iteration:
                    QApplication.processEvents()
                    batch_x, batch_y = get_batch(directory)
                    sess.run(opt, feed_dict={x: batch_x, y: batch_y})  # 只运行优化迭代计算图
                    self.textBrowser.append("开始第 {iter} 次迭代".format(iter=iter))
                    if iter % 100 == 0:
                        los, acc, parg, yarg = sess.run([loss, accuracy, pre_arg, y_arg],
                                                        feed_dict={x: batch_x, y: batch_y})
                        self.textBrowser.append("For iter: {iter}".format(iter=iter))
                        # print("For iter ", iter)
                        self.textBrowser.append("Accuracy: {acc}".format(acc=acc))
                        # print("Accuracy ", acc)
                        self.textBrowser.append("Loss: {los}".format(los=los))
                        # print("Loss ", los)
                        if iter % 1000 == 0:
                            self.textBrowser.append("predict arg: {parg}".format(parg=parg[0:10]))
                        #     print("predict arg:", parg[0:10])
                            self.textBrowser.append("yarg : {yarg}".format(yarg=parg[0:10]))
                        #     print("yarg :", yarg[0:10])
                        # print("__________________")
                    if iter % 1000 == 0:  # 保存模型
                        saver.save(sess, model_path, global_step=iter)
                    iter += 1
                    self.step = self.step + step_tmp
                    self.pbar.setValue(self.step)

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())