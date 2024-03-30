from sklearn.model_selection import train_test_split
import shutil
import glob


def split_train_val_test(path: str):
    """
        function for creating training datat
    :param path:
    :param classes:
    :return:
    """
    images_ls: list = sorted(glob.glob(path + '*.png'))
    regs_ls: list = sorted(glob.glob(path + '*.reg'))
    mix: list = list(zip(images_ls, regs_ls))
    train_data, rest_data = train_test_split(mix, train_size=0.8, shuffle=True, random_state=42)  # type: (list, list)
    validation_data, test_data = train_test_split(rest_data, test_size=0.5, shuffle=False, random_state=42)
    return train_data, validation_data, test_data


train_data, validation_data, test_data = split_train_val_test('./MuestrasMaderas/')

print(train_data)
print(validation_data)
print(test_data)

files_dirs = [(train_data, 'train'), (validation_data, 'dev'), (test_data, 'test')]
for files, dir_ in files_dirs:
    for img, reg_file in files:
        print(img, reg_file)
        shutil.copy2(img, f'./splits/{dir_}/')
        shutil.copy2(reg_file, f'./splits/{dir_}/')
        try:
            shutil.copy2(reg_file.replace('.reg', '.txt'), f'./splits/{dir_}/')
        except:
            pass
