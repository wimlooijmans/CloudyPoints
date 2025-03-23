from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision.io import ImageReadMode

class CityscapesDataset(Dataset):
    def __init__(self, path_data, split, augmentation=None):
        self.path_data = path_data
        self.path_images = path_data / 'left_images' / split
        self.path_depth = path_data / 'depth' / split
        self.all_path_images = [img for img in self.path_images.iterdir() if img.suffix == ".png"]
        self.augmentation = augmentation
        #print('self.all_path_images: ', self.all_path_images)
        #print('type self.all_path_images: ', type(self.all_path_images))

    def __len__(self):
        return len(self.all_path_images)

    def __getitem__(self, idx):
        path_image_i = self.all_path_images[idx]
        name = path_image_i.stem[:-11] #discard last 11 letters because these are '_left_image'
        path_depth_i = self.path_depth / (name + '_depth_image.png')

        image = read_image(path_image_i)
        depth = read_image(path_depth_i, ImageReadMode.GRAY)

        if self.augmentation:
          image = self.augmentation(image)
          depth = self.augmentation(depth)

        image = image.float()
        depth = depth.float()

        return image, depth