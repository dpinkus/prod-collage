
import argparse
import os
from PIL import Image

def create_collage(
    output_width,
    output_height,
    hero_image_path,
    images_folder,
    collage_type='screenshots',
    padding_color=(0, 0, 0)  # black
):
    output_size = (output_width, output_height)
    margin = 2  # 2-pixel space between hero and other images

    # Load hero image
    hero_img = Image.open(hero_image_path).convert("RGB")
    hero_w, hero_h = hero_img.size

    if collage_type == 'single':
        # Scale hero image proportionally
        if hero_w > hero_h:
            scale_factor = output_width / hero_w
        else:
            scale_factor = output_height / hero_h
        new_w = int(hero_w * scale_factor)
        new_h = int(hero_h * scale_factor)
        hero_img_resized = hero_img.resize((new_w, new_h), Image.LANCZOS)

        # Pad hero image to center it in output size
        collage = Image.new("RGB", output_size, padding_color)
        pad_left = (output_width - new_w) // 2
        pad_top = (output_height - new_h) // 2
        collage.paste(hero_img_resized, (pad_left, pad_top))
        return collage

    elif collage_type == 'screenshots':
        # Determine orientation of hero image
        portrait = hero_h >= hero_w
        collage = Image.new("RGB", output_size, padding_color)

        if portrait:
            scale_factor = output_height / hero_h
            scaled_w = int(hero_w * scale_factor)
            scaled_h = output_height
            hero_resized = hero_img.resize((scaled_w, scaled_h), Image.LANCZOS)
            collage.paste(hero_resized, (0, 0))

            available_width = output_width - scaled_w - margin
            if available_width <= 0:
                return collage

            other_imgs = []
            for fname in os.listdir(images_folder):
                path = os.path.join(images_folder, fname)
                if os.path.abspath(path) != os.path.abspath(hero_image_path) and os.path.isfile(path):
                    try:
                        img = Image.open(path).convert("RGB")
                        other_imgs.append(img)
                    except:
                        continue

            resized_imgs = []
            for img in other_imgs:
                orig_w, orig_h = img.size
                scale = available_width / orig_w
                if scale > 2:
                    scale = 2
                new_w = int(orig_w * scale)
                new_h = int(orig_h * scale)
                resized = img.resize((new_w, new_h), Image.LANCZOS)
                resized_imgs.append(resized)

            y_offset = 0
            fitted_imgs = []
            for img in resized_imgs:
                if y_offset + img.height > output_height:
                    break
                fitted_imgs.append(img)
                y_offset += img.height

            remaining_space = output_height - sum(i.height for i in fitted_imgs)
            if len(fitted_imgs) > 1:
                v_spacing = remaining_space // (len(fitted_imgs) - 1)
            else:
                v_spacing = 0
            if v_spacing > 10:
                v_spacing = 10

            y_cursor = 0
            for img in fitted_imgs:
                x = scaled_w + margin
                collage.paste(img, (x, y_cursor))
                y_cursor += img.height + v_spacing

            return collage

        else:
            scale_factor = output_width / hero_w
            scaled_w = output_width
            scaled_h = int(hero_h * scale_factor)
            hero_resized = hero_img.resize((scaled_w, scaled_h), Image.LANCZOS)
            collage.paste(hero_resized, (0, 0))

            available_height = output_height - scaled_h - margin
            if available_height <= 0:
                return collage

            other_imgs = []
            for fname in os.listdir(images_folder):
                path = os.path.join(images_folder, fname)
                if os.path.abspath(path) != os.path.abspath(hero_image_path) and os.path.isfile(path):
                    try:
                        img = Image.open(path).convert("RGB")
                        other_imgs.append(img)
                    except:
                        continue

            resized_imgs = []
            for img in other_imgs:
                orig_w, orig_h = img.size
                scale = available_height / orig_h
                if scale > 2:
                    scale = 2
                new_w = int(orig_w * scale)
                new_h = int(orig_h * scale)
                resized = img.resize((new_w, new_h), Image.LANCZOS)
                resized_imgs.append(resized)

            x_offset = 0
            fitted_imgs = []
            for img in resized_imgs:
                if x_offset + img.width > output_width:
                    break
                fitted_imgs.append(img)
                x_offset += img.width

            remaining_space = output_width - sum(i.width for i in fitted_imgs)
            if len(fitted_imgs) > 1:
                h_spacing = remaining_space // (len(fitted_imgs) - 1)
            else:
                h_spacing = 0
            if h_spacing > 10:
                h_spacing = 10

            x_cursor = 0
            for img in fitted_imgs:
                y = scaled_h + margin
                collage.paste(img, (x_cursor, y))
                x_cursor += img.width + h_spacing

            return collage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a photo collage.")
    parser.add_argument("--width", type=int, required=True, help="Output width in pixels")
    parser.add_argument("--height", type=int, required=True, help="Output height in pixels")
    parser.add_argument("--hero", type=str, required=True, help="Path to the hero image")
    parser.add_argument("--folder", type=str, required=True, help="Folder containing additional images")
    parser.add_argument("--type", type=str, choices=["single", "screenshots"], default="screenshots", help="Collage type")
    parser.add_argument("--output", type=str, default="collage_output.jpg", help="Filename for the output image")
    args = parser.parse_args()

    collage = create_collage(
        args.width,
        args.height,
        args.hero,
        args.folder,
        collage_type=args.type
    )
    collage.save(args.output)
    print(f"Collage saved as {args.output}")
