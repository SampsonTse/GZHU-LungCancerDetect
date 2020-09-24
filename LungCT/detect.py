import torch
from torch.autograd import Variable
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image

#root = "/home/xy/桌面/LungCT/"


# -----------------ready the dataset--------------------------
def default_loader(path):
    return Image.open(path).convert('L')

class MyDataset(Dataset):
    # 构造函数带有默认参数
    def __init__(self, txt, transform=None, target_transform=None, loader=default_loader):
        fh = open(txt, 'r')
        imgs = []
        i = 0
        for line in fh:
            # 移除字符串首尾的换行符
            # 删除末尾空
            # 以空格为分隔符 将字符串分成
            line = line.strip('\n')
            line = line.rstrip()
            words = line.split()
            imgs.append((words[0], int(words[1])))  # imgs中包含有图像路径和标签
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    def __getitem__(self, index):
        fn, label = self.imgs[index]
        # 调用定义的loader方法
        img = self.loader(fn)
        if self.transform is not None:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.imgs)

import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        #卷积->池化->卷积
        self.conv1 = nn.Conv2d(1,32,5)
        self.conv2 = nn.Conv2d(32,64,5)
        self.conv3 = nn.Conv2d(64,128,5)
        self.pool = nn.MaxPool2d(2,2)
        
        # 全连接层
        self.fc1 = nn.Linear(2 * 2 *128, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 36)
        self.fc4 = nn.Linear(36,2)

    def forward(self, x):
        #激活函数relu
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        # 展平
        x = x.view(-1, 128 * 2 * 2)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x



#net = Net()
#net.load_state_dict(torch.load('net_para.pkl'))

#x = net(images)
#_, predicted = torch.max(x, 1)
#print(predicted)
#print(classes[predicted])
#print(int(predicted))
