from realesrgan import RealESRGANer
from basicsr.archs.srvgg_arch import SRVGGNetCompact
import cv2

def create_upsampler(scale, model_path):
    model = SRVGGNetCompact(
        num_in_ch=3,
        num_out_ch=3,
        num_feat=64,
        num_conv=32,
        upscale=scale,
        act_type='prelu'
    )
    upsampler = RealESRGANer(
        scale=scale,
        model_path=model_path,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=False
    )
    return upsampler

img = cv2.imread('input_image.jpg')

upsampler_x4 = create_upsampler(4, 'realesr-general-x4v3.pth')
output_x4, _ = upsampler_x4.enhance(img, outscale=4)
cv2.imwrite('output_x4.png', output_x4)

upsampler_x8 = create_upsampler(4, 'realesr-general-x4v3.pth')
temp_x8, _ = upsampler_x8.enhance(img, outscale=4)
output_x8, _ = upsampler_x8.enhance(temp_x8, outscale=4)
cv2.imwrite('output_x8.png', output_x8)