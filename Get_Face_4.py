import numpy as np
from ReadImg import *
from ExtractFeature import *
import random
from sklearn.svm import LinearSVC


file_kun = 'D:/PycharmWorkSpace/MScProj/data/753-kun.dat'


def prepare_data(img_frames, time_arr):
    # split train and test set
    time_arr = time_arr[1:]
    relex_begin = np.amin(np.where(time_arr > 20))
    relex_over = np.amin(np.where(time_arr > 110))
    stress_1_1_begin = np.amin(np.where(time_arr > 150))
    stress_1_1_over = np.amin(np.where(time_arr > 245))
    stress_1_2_begin = np.amin(np.where(time_arr > 290))
    stress_1_2_over = np.amin(np.where(time_arr > 384))
    stress_2_1_begin = np.amin(np.where(time_arr > 423))
    stress_2_1_over = np.amin(np.where(time_arr > 502))
    stress_2_2_begin = np.amin(np.where(time_arr > 544))
    stress_2_2_over = np.amin(np.where(time_arr > 618))
    relax = relex_over-50-relex_begin
    stress1 = stress_1_1_over-stress_1_1_begin+stress_1_2_over-50-stress_1_2_begin
    stress2 = stress_2_1_over-stress_2_1_begin+stress_2_2_over-50-stress_2_2_begin
    # x_train = np.concatenate((img_frames[:, :, relex_begin:relex_over-50],
    #                           img_frames[:, :, stress_1_1_begin:stress_1_1_over],
    #                           img_frames[:, :, stress_1_2_begin:stress_1_2_over-50],
    #                           img_frames[:, :, stress_2_1_begin:stress_2_1_over],
    #                           img_frames[:, :, stress_2_2_begin:stress_2_2_over-50]), axis=2)
    x_train = np.concatenate((img_frames[:, :, relex_begin:relex_over],
                              img_frames[:, :, stress_1_1_begin:stress_1_1_over],
                              img_frames[:, :, stress_1_2_begin:stress_1_2_over],
                              img_frames[:, :, stress_2_1_begin:stress_2_1_over],
                              img_frames[:, :, stress_2_2_begin:stress_2_2_over]), axis=2)
    # x_test = np.concatenate((img_frames[:, :, relex_over-50:relex_over],
    #                          img_frames[:, :, stress_1_2_over-50:stress_1_2_over],
    #                          img_frames[:, :, stress_2_2_over-50:stress_2_2_over]), axis=2)
    # for i_save in range(np.size(x_test, 2)):
    #     this_frame = x_test[:, :, i_save]
    #     plt.imsave('./data/test_ou_' + str(i_save) + '.png', this_frame)
    # apply labels to train & test set
    # y_train = np.zeros(np.size(x_train, 2))
    # y_train[0:relex_over-50-relex_begin] = 0
    # y_train[(relex_over-50-relex_begin):(relex_over-50-relex_begin) + (stress_1_1_over-stress_1_1_begin) + (stress_1_2_over-50-stress_1_2_begin)] = 1
    # y_train[(relex_over-50-relex_begin) + (stress_1_1_over-stress_1_1_begin) + (stress_1_2_over-50-stress_1_2_begin):
    #         (relex_over-50-relex_begin)+(stress_1_1_over-stress_1_1_begin)+(stress_1_2_over-50-stress_1_2_begin)+
    #         (stress_2_1_over - stress_2_1_begin) + (stress_2_2_over - 50 - stress_2_2_begin)] = 2
    """new version"""
    y_train = np.zeros(np.size(x_train, 2))
    y_train[0:relex_over-relex_begin] = 0
    y_train[(relex_over-relex_begin):(relex_over-relex_begin) + (stress_1_1_over-stress_1_1_begin) + (stress_1_2_over-stress_1_2_begin)] = 1
    y_train[(relex_over-relex_begin) + (stress_1_1_over-stress_1_1_begin) + (stress_1_2_over-stress_1_2_begin):
            (relex_over-relex_begin)+(stress_1_1_over-stress_1_1_begin)+(stress_1_2_over-stress_1_2_begin)+
            (stress_2_1_over - stress_2_1_begin) + (stress_2_2_over - stress_2_2_begin)] = 2
    # y_test = np.zeros(150)
    # y_test[0:50] = 0
    # y_test[50:100] = 1
    # y_test[100:150] = 2
    # return x_train, x_test, y_train, y_test
    return x_train, y_train

"""old version"""
# def extract_face(x_train, x_test):
#     # cut no-use portion & calculate mean
#     x_train = x_train[0:160, :, :]
#     x_train_mean = np.mean(x_train, 2)
#     plt.imsave('./data/faces/kun/x_mean.png', x_train_mean)
#     # get four lines to cut the face from data_frames
#     x_train_mean_2d = np.reshape(x_train_mean, (160*240))
#     top = int(np.floor(np.amin(np.where(x_train_mean_2d > 27))/240))
#     bottom = int(np.floor(np.amax(np.where(x_train_mean_2d > 27)) / 240))
#     x_train_mean_2d = np.reshape(np.transpose(x_train_mean), (160 * 240))
#     left = int(np.floor(np.amin(np.where(x_train_mean_2d > 26.5)) / 160))
#     right = int(np.floor(np.amax(np.where(x_train_mean_2d > 26.5)) / 160))
#     x_train_mean_cut = x_train_mean[top:bottom, left:right]
#     plt.imsave('./data/faces/kun/face_mean.png', x_train_mean_cut)
#     # cut train data_frames
#     x_train_cut = x_train[top:bottom, left:right, :]
#     # for i_save in range(np.size(x_train, 2)):
#     #     this_frame = x_train_cut[:, :, i_save]
#     #     plt.imsave('./data/faces/kun/train_' + str(i_save) + '.png', this_frame)
#     # cut test data_frames
#     x_test_cut = x_test[top:bottom, left:right, :]
#     # for i_save in range(np.size(x_test, 2)):
#     #     this_frame = x_test_cut[:, :, i_save]
#     #     plt.imsave('./data/faces/kun/test_' + str(i_save) + '.png', this_frame)
#     return x_train_cut, x_test_cut, abs(top-bottom), (right-left)


"""new version"""
def extract_face(x_train):
    # cut no-use portion & calculate mean
    x_train = x_train[0:160, :, :]
    x_train_mean = np.mean(x_train, 2)
    plt.imsave('./data/faces/kun/x_mean.png', x_train_mean)
    # get four lines to cut the face from data_frames
    x_train_mean_2d = np.reshape(x_train_mean, (160*240))
    top = int(np.floor(np.amin(np.where(x_train_mean_2d > 27))/240))
    bottom = int(np.floor(np.amax(np.where(x_train_mean_2d > 27)) / 240))
    x_train_mean_2d = np.reshape(np.transpose(x_train_mean), (160 * 240))
    left = int(np.floor(np.amin(np.where(x_train_mean_2d > 26.5)) / 160))
    right = int(np.floor(np.amax(np.where(x_train_mean_2d > 26.5)) / 160))
    x_train_mean_cut = x_train_mean[top:bottom, left:right]
    plt.imsave('./data/faces/kun/face_mean.png', x_train_mean_cut)
    # cut train data_frames
    x_train_cut = x_train[top:bottom, left:right, :]
    # for i_save in range(np.size(x_train, 2)):
    #     this_frame = x_train_cut[:, :, i_save]
    #     plt.imsave('./data/faces/kun/train_' + str(i_save) + '.png', this_frame)
    # cut test data_frames
    # x_test_cut = x_test[top:bottom, left:right, :]
    # for i_save in range(np.size(x_test, 2)):
    #     this_frame = x_test_cut[:, :, i_save]
    #     plt.imsave('./data/faces/kun/test_' + str(i_save) + '.png', this_frame)
    return x_train_cut, abs(top-bottom), (right-left)


def get_face_kun():
    # read img & prepossessing
    file = read_file(file_kun, 320, 240)
    img_frames = get_img_frames(file, 320, 240)
    # prepare face_data
    time_arr = get_time_arr(file)  #246.149s
    # x_train, x_test, y_train, y_test = prepare_data(img_frames, time_arr)
    x_train, y_train = prepare_data(img_frames, time_arr)
    # face_train, face_test, h, w = extract_face(x_train, x_test)
    face_train, h, w = extract_face(x_train)
    # # img_frames = img_frames/np.mean(img_frames)
    # eigen_faces, x_train_pca, x_test_pca, var_percent = pca(face_train, face_test, h, w)
    # for i_save in range(np.size(eigen_faces, 0)):
    #     this_eg = eigen_faces[i_save, :]
    #     plt.imsave('./data/eigen/kun/' + str(i_save) + '.png', (np.reshape(this_eg, [h, w])))
    # print(var_percent)
    # print(sum(var_percent))
    # classifier = LinearSVC()
    # classifier.fit(x_train_pca, y_train)
    # train_accuracy = classifier.score(x_train_pca, y_train)
    # test_accuracy = classifier.score(x_test_pca, y_test)
    # print(train_accuracy)
    # print(test_accuracy)
    # return face_train, face_test, y_train, y_test, h, w
    return face_train, y_train, h, w


if __name__ == '__main__':
    get_face_kun()



