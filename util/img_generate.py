from skimage.transform import warp, AffineTransform, ProjectiveTransform
from skimage.exposure import equalize_adapthist, equalize_hist, rescale_intensity, adjust_gamma, adjust_log, \
    adjust_sigmoid
from skimage.filters import gaussian
from skimage.util import random_noise
from util.photo_crop import crop_photo
import pylab as pl
import pandas as pd
import os
import uuid
import random

def randRange(a, b):
    '''
    a utility functio to generate random float values in desired range
    '''
    return pl.rand() * (b - a) + a


def randomAffine(im):
    '''
    wrapper of Affine transformation with random scale, rotation, shear and translation parameters
    '''
    tform = AffineTransform(scale=(randRange(0.75, 1.3), randRange(0.75, 1.3)),
                            rotation=randRange(-0.25, 0.25),
                            shear=randRange(-0.2, 0.2),
                            translation=(randRange(-im.shape[0] // 10, im.shape[0] // 10),
                                         randRange(-im.shape[1] // 10, im.shape[1] // 10)))
    return warp(im, tform.inverse, mode='reflect')


def randomPerspective(im):
    '''
    wrapper of Projective (or perspective) transform, from 4 random points selected from 4 corners of the image within a defined region.
    '''
    region = 1 / 4
    A = pl.array([[0, 0], [0, im.shape[0]], [im.shape[1], im.shape[0]], [im.shape[1], 0]])
    B = pl.array([[int(randRange(0, im.shape[1] * region)), int(randRange(0, im.shape[0] * region))],
                  [int(randRange(0, im.shape[1] * region)), int(randRange(im.shape[0] * (1 - region), im.shape[0]))],
                  [int(randRange(im.shape[1] * (1 - region), im.shape[1])),
                   int(randRange(im.shape[0] * (1 - region), im.shape[0]))],
                  [int(randRange(im.shape[1] * (1 - region), im.shape[1])), int(randRange(0, im.shape[0] * region))],
                  ])

    pt = ProjectiveTransform()
    pt.estimate(A, B)
    return warp(im, pt, output_shape=im.shape[:2])


def deep_crop(im):
    return crop_photo(im)


def randomIntensity(im):
    '''
    rescales the intesity of the image to random interval of image intensity distribution
    '''
    return rescale_intensity(im,
                             in_range=tuple(pl.percentile(im, (randRange(0, 10), randRange(90, 100)))),
                             out_range=tuple(pl.percentile(im, (randRange(0, 10), randRange(90, 100)))))


def randomGamma(im):
    '''
    Gamma filter for contrast adjustment with random gamma value.
    '''
    return adjust_gamma(im, gamma=randRange(0.5, 1.5))


def randomGaussian(im):
    '''
    Gaussian filter for bluring the image with random variance.
    '''
    return gaussian(im, sigma=randRange(0, 5))


def randomFilter(im):
    '''
    randomly selects an exposure filter from histogram equalizers, contrast adjustments, and intensity rescaler and applys it on the input image.
    filters include: equalize_adapthist, equalize_hist, rescale_intensity, adjust_gamma, adjust_log, adjust_sigmoid, gaussian
    '''
    Filters = [equalize_adapthist, equalize_hist, adjust_log, adjust_sigmoid, randomGamma, randomGaussian,
               randomIntensity]
    filt = random.choice(Filters)
    return filt(im)


def randomNoise(im):
    '''
    random gaussian noise with random variance.
    '''
    var = randRange(0.001, 0.01)
    return random_noise(im, var=var)


generation_policies = [randomNoise]  # randomNoise


def generate_sample(source_file, dst_file, pipeline):
    im = deep_crop(source_file)
    print(im.shape)
    for item in pipeline:
        im = item(im)
    pl.imsave(dst_file, arr=im)


def sample_generate(category, original_df, num_samples = 10):
    df = pd.DataFrame(columns=["Image", "SrcImage", "Id"])
    original_df_filtered = original_df[original_df["Id"] == category]
    for _ in range(0, num_samples):
        sample = original_df_filtered.sample(1).iloc[0]["Image"]
        sample_dst = sample[:-4] + '-' + str(uuid.uuid4()) + ".jpg"
        sample_file_path = os.path.join("../static/train", sample)
        sample_dst_file_path = os.path.join("../generated_train", sample_dst)

        # generate pipeline
        # num_policies = random.randint(1, len(generation_policies))
        # pipeline = generation_policies.copy()
        # random.shuffle(pipeline)
        # pipeline = pipeline[:num_policies]
        pipeline = generation_policies
        generate_sample(sample_file_path, sample_dst_file_path, pipeline)
        df.append([[sample_dst, sample, category]], ignore_index=True)
    return df


def main():
    df_train = pd.read_csv('../metadata/train.csv')
    df_sorted = df_train.groupby(['Id']).agg('count').sort_values("Image", ascending=False)
    print(df_sorted)
    result_df = pd.DataFrame(columns=["Image", "SrcImage", "Id"])
    for idx in df_sorted.index:
        df = sample_generate(idx, df_train)
        result_df.append(df)

    result_df.to_csv("generated_df.csv")

if __name__ == '__main__':
    main()
