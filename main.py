import os
from PIL import Image, ImageDraw, ImageFont
import json


def image_add_text(
    img_path, text, left, top, text_color=(0, 0, 0), text_size=13, text_font="Times.ttc"
):
    img = Image.open(img_path)

    draw = ImageDraw.Draw(img)

    fontStyle = ImageFont.truetype(text_font, text_size, encoding="utf-8")

    draw.text((left, top), text, text_color, font=fontStyle)
    return img


def process_instructions(text_file, prefix, postfix, add_newline=False, lower=True):
    with open(text_file, "r") as f:
        lines = f.readlines()

    lines = lines[1:]

    insts = []
    for line in lines:
        if lower:
            temp_inst = prefix + line.split(",")[0].lower() + "."
        else:
            temp_inst = prefix + line.split(",")[0] + "."

        if add_newline:
            words = temp_inst.split(" ")
            inst = ""
            char_cnt = -1
            for word in words:
                if char_cnt + len(word) > 25:
                    inst += "\n"
                    char_cnt = -1
                else:
                    inst += " "
                inst += word
                char_cnt += len(word) + 1
            inst += "\n" + postfix
        else:
            inst = temp_inst + " " + postfix

        insts.append(inst)
    return insts


def generate_instruction_images(
    data_file_name: str,
    result_dir: str,
    prefix: str,
    postfix: str,
    background_img_path: str,
    lower: bool,
):
    """
    data_file_name: path to harmful instructions
    lower: lower case for instructions
    """
    insts = process_instructions(
        data_file_name, prefix, postfix, add_newline=True, lower=lower
    )

    for idx, inst in enumerate(insts):
        res_img = image_add_text(
            background_img_path, inst, 20, 60, text_color=(0, 0, 0), text_size=16
        )
        res_path = os.path.join(result_dir, str(idx) + ".jpg")
        res_img.save(res_path)


def generate_text_instruction(
    data_file_name: str, result_file_name: str, prefix: str, postfix: str, lower: bool
):
    """
    data_file_name: path to harmful instructions
    lower: lower case for instructions
    """

    insts = process_instructions(
        data_file_name, prefix, postfix, add_newline=False, lower=lower
    )

    with open(result_file_name, "w") as f:
        json.dump(insts, f)


if __name__ == "__main__":
    pass

    # An example for text:
    # data_file_name = "./harmful_behaviors.csv"
    # result_file_name = "instruction_text_baseline/text_instructions.json"
    # prefix = ""
    # postfix = ""
    # lower = False
    # generate_text_instruction(data_file_name, result_file_name, prefix, postfix, lower)

    # An example for image:
    # data_file_name = "./harmful_behaviors.csv"
    # result_dir = "instruction_images_baseline/images"
    # prefix = ""
    # postfix = ""
    # lower = False
    # generate_instruction_images(
    #     data_file_name,
    #     result_dir,
    #     prefix,
    #     postfix,
    #     background_img_path="background.jpg",
    #     lower=lower,
    # )
