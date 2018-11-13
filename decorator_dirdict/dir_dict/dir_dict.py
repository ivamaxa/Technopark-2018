import os


class DirDict:
    def __init__(self, path):
        self.path = path

    def __len__(self):
        return len(os.listdir(self.path))

    def __getitem__(self, key):
        full_path = self.path + '/' + key
        f = open(full_path, 'r')
        content = f.read()
        f.close()
        return content

    def __setitem__(self, key, value):
        full_path = self.path + '/' + key
        f = open(full_path, 'w')
        f.write(value)
        f.close()

    def __delitem__(self, key):
        if key not in os.listdir(self.path):
            raise KeyError
        full_path = self.path + '/' + key
        os.remove(full_path)

    def __iter__(self):
        return iter(os.listdir(self.path))


#d = DirDict('/home/maha/python/dir_dict')
#d['lang'] = 'Python\n'
#del d['lang']