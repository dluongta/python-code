from realesrgan import RealESRGANer
from basicsr.archs.srvgg_arch import SRVGGNetCompact
import cv2

model = SRVGGNetCompact(
    num_in_ch=3,
    num_out_ch=3,
    num_feat=64,
    num_conv=32,
    upscale=4,
    act_type='prelu'
)

upsampler = RealESRGANer(
    scale=4,
    model_path='realesr-general-x4v3.pth',
    model=model,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False
)

img = cv2.imread('input_image.jpg')

output, _ = upsampler.enhance(img, outscale=4)

cv2.imwrite('output_image.png', output)