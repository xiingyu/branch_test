import yaml
import glob

train_list = glob.glob('./train/images/*.jpg')
valid_list = glob.glob('./valid/images/*.jpg')
test_list = glob.glob('./test/images/*.jpg')

with open('/home/skh/testing_folder/trash_sort/deneme-3/train.txt', 'w') as f:
    f.write('\n'.join(train_list) + '\n')

with open('/home/skh/testing_folder/trash_sort/deneme-3/valid.txt', 'w') as f:
    f.write('\n'.join(valid_list) + '\n')
    
with open('/home/skh/testing_folder/trash_sort/deneme-3/test.txt', 'w') as f:
    f.write('\n'.join(test_list) + '\n')




with open('/home/skh/testing_folder/trash_sort/deneme-3/data.yaml', 'r') as f:
  data = yaml.load(f)

print(data)
data['train'] = '/home/skh/testing_folder/trash_sort/deneme-3/train.txt'
data['val'] = '/home/skh/testing_folder/trash_sort/deneme-3/val.txt'
data['test'] = '/home/skh/testing_folder/trash_sort/deneme-3/test.txt'

# dump means, python 객체를 yaml형태의 문자열로 반환하는 의미.
with open('/home/skh/testing_folder/trash_sort/deneme-3/data.yaml', 'w') as f:
  yaml.dump(data, f)

# print(data)